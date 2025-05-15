import time
import uasyncio as asyncio
from math import radians
from lib.utils import convert_dm_dd, normalize
from driver.gpsuart import gpsuart
from storage.store import Store
store = Store.instance()

__HEMISPHERES = ('N', 'S', 'E', 'W')

class GPS(object):

    """GPS NMEA Sentence Parser. Creates object that stores all relevant GPS data and statistics.
    Parses sentences one character at a time using update(). """
    
    _instance = None # is a singleton
    
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self, local_offset=0):
        """Setup GPS Object Status Flags, Internal Data Registers, etc"""

        #####################
        # Object Status Flags
        self.sentence_active = False
        self.active_segment = 0
        self.process_crc = False
        self.gps_segments = []
        self.crc_xor = 0
        self.char_count = 0
        self.fix_time = 0

        #####################
        # Sentence Statistics
        self.crc_fails = 0
        self.clean_sentences = 0
        self.parsed_sentences = 0

        #####################
        # Data From Sentences
        # Time
        self.timestamp = (0, 0, 0)
        self.date = (0, 0, 0)
        self.local_offset = local_offset

        # UART readall
        self.oldstring = bytes()

        # Events
        self.positionAvailable =  asyncio.ThreadSafeFlag()
        self.speedAvailable =  asyncio.ThreadSafeFlag()
        self.courseAvailable =  asyncio.ThreadSafeFlag()

   

    ########################################
    # GPS Asyncronous Tasks
    ########################################

    async def readGpsTask(self):
        ''' read and parse the gps string and update gps state'''
        try:
            print('starting readGpsTask')
            while True:
               
                #read the gps sentense for the uart
                gpssentence = gpsuart.readline()
                
                if gpssentence != None:
                    self.parsesentence( gpssentence )

                await asyncio.sleep_ms(50)

        except asyncio.CancelledError:
            print( "stopping readGpsTask" )     
            
    ########################################
    # Sentence Parsers
    ########################################
    
    def gpgll(self):
        """Parse Geographic Latitude and Longitude (GLL)Sentence. Updates UTC timestamp, latitude,
        longitude, and fix status"""

        # UTC Timestamp
        try:
            utc_string = self.gps_segments[5]

            if utc_string:  # Possible timestamp found
                hours = int(utc_string[0:2]) + self.local_offset
                minutes = int(utc_string[2:4])
                seconds = float(utc_string[4:])
                self.timestamp = (hours, minutes, seconds)

            else:  # No Time stamp yet
                self.timestamp = (0, 0, 0)

        except ValueError:  # Bad Timestamp value present
            return False
        
        except IndexError:
            return False

        # Check Receiver Data Valid Flag
        if self.gps_segments[6] == 'A':  # Data from Receiver is Valid/Has Fix

            # Longitude / Latitude
            try:
                # Latitude
                l_string = self.gps_segments[1] #4941.66419
          
                lat_degs = l_string[0:2]
                lat_mins = l_string[2:]
                lat_hemi = self.gps_segments[2]

                # Longitude
                l_string = self.gps_segments[3] #01049.63852
                lon_degs = l_string[0:3] 
                lon_mins = l_string[3:]
                lon_hemi = self.gps_segments[4]

                if lat_hemi not in __HEMISPHERES:
                    raise ValueError()

                if lon_hemi not in __HEMISPHERES:
                    raise ValueError()                    

                latitude =  convert_dm_dd(lat_degs, lat_mins, lat_hemi)
                longitude = convert_dm_dd(lon_degs, lon_mins, lon_hemi)  

          

                store.position = (longitude,latitude)
                store.positionvalid = True

                # Notify other listening task that a new position is available
                # Only one other task can receive the notification flag :(
                self.positionAvailable.set()
                
            except ValueError:
                return False

            # Update Last Fix Time
            self.new_fix_time()

        else:  # Clear Position Data if Sentence is 'Invalid'
            store.positionvalid = False

        return True

    def gpvtg(self):
        """Parse Track Made Good and Ground Speed (VTG) Sentence. Updates speed and course"""
        try:
            course = float(self.gps_segments[1])
            spd_knt = float(self.gps_segments[5])
        except ValueError:
            return False
        except IndexError:
            return False

        store.gpsspeed = spd_knt
        store.gpscourse = normalize(radians(course))

        self.courseAvailable.set() # notifies course.fuseGPS 
        self.speedAvailable.set()

        return True

    ##########################################
    # Data Stream Handler Functions
    ##########################################

    def new_sentence(self):
        """Adjust Object Flags in Preparation for a New Sentence"""
        self.gps_segments = ['']
        self.active_segment = 0
        self.crc_xor = 0
        self.sentence_active = True
        self.process_crc = True
        self.char_count = 0

    def parsesentence(self, string):
        idx = 0        
        string_tmp = self.oldstring + string
        
        for c in string_tmp:            
            idx = idx + 1
            stat = self.update(chr(c))                        
            if(stat != None):                                                
                self.oldstring = string_tmp[idx:]
                return stat
            
    def stringclean(self):
        self.oldstring = bytes()        

    def update(self, new_char):
        """Process a new input char and updates GPS object if necessary based on special characters ('$', ',', '*')
        Function builds a list of received string that are validate by CRC prior to parsing by the  appropriate
        sentence function. Returns sentence type on successful parse, None otherwise"""

        valid_sentence = False

        # Validate new_char is a printable char        
        ascii_char = ord(new_char)

        if 10 <= ascii_char <= 126:
            self.char_count += 1

            # Check if a new string is starting ($)
            if new_char == '$':
                self.new_sentence()
                return None

            elif self.sentence_active:

                # Check if sentence is ending (*)
                if new_char == '*':
                    self.process_crc = False
                    self.active_segment += 1
                    self.gps_segments.append('')
                    return None

                # Check if a section is ended (,), Create a new substring to feed
                # characters to
                elif new_char == ',':
                    self.active_segment += 1
                    self.gps_segments.append('')

                # store All Other printable character and check CRC when ready
                else:
                    self.gps_segments[self.active_segment] += new_char

                    # When CRC input is disabled, sentence is nearly complete
                    if not self.process_crc:

                        if len(self.gps_segments[self.active_segment]) == 2:
                            try:
                                final_crc = int(self.gps_segments[self.active_segment], 16)
                                if self.crc_xor == final_crc:
                                    valid_sentence = True
                                else:
                                    self.crc_fails += 1
                            except ValueError:
                                pass  # CRC Value was deformed and could not have been correct

                # Update CRC
                if self.process_crc:
                    self.crc_xor ^= ascii_char

                # If a Valid Sentence Was received and it's a supported sentence, then parse it!!
                if valid_sentence:
                    self.clean_sentences += 1  # Increment clean sentences received
                    self.sentence_active = False  # Clear Active Processing Flag

                    if self.gps_segments[0][2:] in self.supported_sentences:
                        # parse the Sentence Based on the message type, return True if parse is clean                        
                        if self.supported_sentences[self.gps_segments[0][2:]](self):                        
                            # Let host know that the GPS object was updated by returning parsed sentence type
                            self.parsed_sentences += 1
                            return self.gps_segments[0]

                # Check that the sentence buffer isn't filling up with Garage waiting for the sentence to complete
                if self.char_count > 76:
                    self.sentence_active = False

        # Tell Host no new sentence was parsed
        return None

    def new_fix_time(self):
        """Updates a high resolution counter with current time when fix is updated. Currently only triggered from
        GGA, GSA and RMC sentences"""
        self.fix_time = time.time()
        return self.fix_time
    
    # The supported NMEA sentences    
    supported_sentences = { 'VTG': gpvtg,  'GLL': gpgll } # GPS + GLONASS