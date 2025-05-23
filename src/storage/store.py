##################################################### 
# Singleton Store holding the RoboBuoy's state
#####################################################
from math import radians
from lib.utils import normalize

class Store(object):

    _instance = None # is a singleton

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Store()
            cls._instance._initialize()
        return cls._instance

    def _initialize( self ):    
        ####################
        # The RoboBuoy Store 
        ####################
            
        # Information
        self.mode = "init"      #Current operational mode of the RoboBouy  ['stop','manual','auto',...]
        
        # Battery
        self.battery = 35   # % Capacity of battery remaining

        # Position, Course & Speed
        self.positionvalid = False  # valid gps position
        self.position = ("10.825340","49.68630810" ) # tuple of strings (lon,lat) degree decimal 9 digit precision
    
        self.gpsheading = 0      # radians
        self.gpsspeed = 0.0     # knots
        self.magheading = 0      # magnetic compass cource -> radians -pi..pi
        self.magdeclination = 0 # magnetic compass declinaiton -> radians -pi..pi
        self.heading = 0  # deg° of the current heading -> radians -pi..pi
        
        # AutonomousPathfinding
        self.destination = ("10.825340","49.68630810" ) # tuple of strings (lon,lat) degree decimal 9 digit precision
        self.distance = 0        # float meters : distance to desired posiiton
        self.course = 0   # deg° of the desired course
        self.waypoints = []      # list of tuples of strings (lat,lon) degree decimal 9 digit precision
        self.waypointarrivedradius = 2 # waypoint arrived radius (meters)
        self.holdradius = 10      # controls the surge during holding station (meters)
        
        # Steering
        # PID tuning gains to control the steering based on course vs heading
        self.Kp = 1.0   # proportional gain
        self.Ki = 0     # integral gain
        self.Kd = 0   # derivative gain

        # PID variables to matintain course by steering
        self.error = 0      # error between desired course and current course
        self.errSum = 0     # accumulated error
        self.dErr = 0       # differential error
        self.lastErr = 0    # previous error
        
        # Complimentary Filter : How much trust is given in the GPS and Compass Readings 
        self.gpsalpha = 0.00  # % trust in the gps's course
        self.magalpha = 0.00  # % trust in the compass's course
        self.declinationalpha = 0.00 # % trust in the gps course to calculate the magnetic declination
        self.gyroalpha = 0.9 # % trust in the gyros correction to course

        # Motor State - never set these directly
        self.surge = 0 # desired robot speed 0..1
        self.steer = 0 # desired robot steering angle -pi..pi
 
        self.vmin = 0  #  minimum robot velocity , constrained to 0..1
        self.vmax = 1  #  maximum robot velocity , constrained to 0..1
        self.minPwmLeft = 3712  #  left pwm value where the motor starts to turn ,0.2ms pulse width (50Hz)
        self.minPwmRight = 3712  #  right pwm value where the motor starts to turn, 0.2ms pulse width (50Hz)      
        self.maxpwm = 6080 #95 # maximum pwm signal sent to the motors, 2.0ms pulse width (50Hz)

        # IMU Constants
        self.accelbias = (0,0,1) # (x,y,z) bias of the accelerometer in g's
        self.gyrobias = (0,0,0) # (x,y,z) bias of the gyroscope in degrees/sec
        self.magbias =  (0,0,0,1,1,1,1,1,1) 
        self.tempoffset = 0
        self.tempsensitivity = 321 # temperature sensitivity of the IMU in degrees C/LSB

    def update(self,dictionary):
        'utility tp update store values from dictionary'
        for key,value in dictionary.items():
            setattr(self,key,value)  


    # Getters and Setters for the Store variables
    # The getters and setters are used to enforce constraints on the values
 

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        ''' mode is a string, constrained to 20 characters '''
        self._mode = str(value)[:20]

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        ''' battery is a int, constrained to 0..100 '''
        self._battery = max(min(int(value),100),0) 

    @property
    def positionvalid(self):
        return self._positionvalid

    @positionvalid.setter
    def positionvalid(self, value):
        self._positionvalid = bool(value)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        ''' position is a tuple of strings (lon,lat) '''
        self._position = tuple(value)[:2]
                              

    @property
    def gpsheading(self):
        return self._gpsheading

    @gpsheading.setter
    def gpsheading(self, value):
        ''' gpsheading in radians, roamlized to -pi..pi '''
        self._gpsheading = normalize(float(value))

    @property
    def gpsspeed(self):
        return self._gpsspeed

    @gpsspeed.setter
    def gpsspeed(self, value):
        ''' gpsspeed in knots, with 2 decimals of precision, constrained to 0..10 '''
        self._gpsspeed =round(max(min(float(value),50),0),2) 

    @property
    def magheading(self):
        return self._magheading

    @magheading.setter
    def magheading(self, value):
        ''' magheading in radians, roamlized to -pi..pi '''
        self._magheading = normalize(float(value))

    @property
    def magdeclination(self):
        return self._magdeclination

    @magdeclination.setter
    def magdeclination(self, value):
        ''' magdeclination in radians, roamlized to -pi..pi '''
        self._magdeclination = normalize(float(value))

    @property
    def heading(self):
        return self._heading

    @heading.setter
    def heading(self, value):
        ''' heading in radians, roamlized to -pi..pi '''
        self._heading = normalize(float(value))

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        ''' destination is a tuple of strings (lat,lon) '''
        self._destination = tuple(value)[:2]

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        ''' distance in meters '''
        # limit the float to 2 decimal places
        self._distance = round(float(value),2)

    @property
    def course(self):
        return self._course

    @course.setter
    def course(self, value):
        ''' course in radians, normalized to -pi..pi '''
        self._course = normalize(float(value))

    @property
    def waypoints(self):
        return self._waypoints

    @waypoints.setter
    def waypoints(self, value):
        ''' waypoints is a list of tuples of strings (lat,lon), constrained to 100 waypoints '''
        self._waypoints = list(value)[:100]

    @property
    def waypointarrivedradius(self):
        return self._waypointarrivedradius

    @waypointarrivedradius.setter
    def waypointarrivedradius(self, value):
        ''' waypointarrivedradius in meters '''
        # limit the float to 2 decimal places
        self._waypointarrivedradius = round(float(value),2)

    @property
    def holdradius(self):
        return self._holdradius

    @holdradius.setter
    def holdradius(self, value):
        self._holdradius = value

    @property
    def Kp(self):
        return self._Kp

    @Kp.setter
    def Kp(self, value):
        #TODO apply constraints
        self._Kp = float(value)

    @property
    def Ki(self):
        return self._Ki

    @Ki.setter
    def Ki(self, value):
        #TODO apply constraints
        self._Ki = float(value)

    @property
    def Kd(self):
        return self._Kd

    @Kd.setter
    def Kd(self, value):
        #TODO apply constraints
        self._Kd = float(value)

    @property
    def gpsalpha(self):
        return self._gpsalpha

    @gpsalpha.setter
    def gpsalpha(self, value):
        self._gpsalpha = max(min(float(value),1),0)

    @property
    def magalpha(self):
        return self._magalpha

    @magalpha.setter
    def magalpha(self, value):
        self._magalpha = max(min(float(value),1),0)

    @property
    def declinationalpha(self):
        return self._declinationalpha

    @declinationalpha.setter
    def declinationalpha(self, value):
        self._declinationalpha = max(min(float(value),1),0)


    @property
    def gyroalpha(self):
        return self._gyroalpha

    @gyroalpha.setter
    def gyroalpha(self, value):
        self._gyroalpha = max(min(float(value),1),0)

    @property
    def surge(self):
        return self._surge

    @surge.setter
    def surge(self, value):     
        # constrain value range to 0..1
        self._surge = max(min(float(value),1),0) 

    @property
    def steer(self):
        return self._steer

    @steer.setter
    def steer(self, value):
        ''' steer in radians, normalized to -pi..pi '''
        self._steer = normalize(float(value))


    @property
    def vmin(self):
        return self._vmin

    @vmin.setter
    def vmin(self, value):
        self._vmin = int(value)


    @property
    def vmax(self):
        return self._vmax

    @vmax.setter
    def vmax(self, value):
        self._vmax = int(value)

    @property
    def minPwmLeft(self):
        return self._mpl

    @minPwmLeft.setter
    def minPwmLeft(self, value):
        self._mpl = int(value)

    @property
    def minPwmRight(self):
        return self._mpr

    @minPwmRight.setter
    def minPwmRight(self, value):
        self._mpr = int(value)

    @property
    def maxpwm(self):
        return self._maxpwm

    @maxpwm.setter
    def maxpwm(self, value):
        self._maxpwm = int(value)

