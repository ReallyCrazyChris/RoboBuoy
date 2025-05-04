"""
Micropython driver for the I2C MPU9250 9-DOF Sensor
"""
import utime
from struct import pack, unpack
from math import atan2, degrees, sqrt, radians
from lib.i2c import i2c
from lib.store import Store
store = Store.instance() #singleton reference

class MagDataNotReady(Exception):
    "Possible race condition in reading magnetometer"
    pass

class IMU(object):
    '''
    Singleton Class provides 9-DOF IMU sensor information for the MPU9250
    North-East-Down(NED) as a fixed, parent coordinate system
    '''

    _instance = None # is a singleton
    
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__( self ):

        # Configure settings from the store 
        #self.accelbias =  tuple(store.accelbias)
        #self.gyrobias =   tuple(store.gyrobias)
        #self.magbias =    tuple(store.magbias)
        #self.tempoffset = store.tempoffset
        #self.tempsensitivity = store.tempsensitivity

        #AccelInit
        self.accel = (0,0,0) 
        self.accelSSF = 16384
        self.accelfullScaleRange(fullScaleRange=0)

        #GyroInit
        self.gyroSSF = 131
        self.gyrofullScaleRange(fullScaleRange = 0) #250_deg/s
        self.gyroLowPassFilter(bandwidth = 6) #5Hz

        #MagInit
        self.initMag()

        #DeltaT
        self.startTime = None


    #Accelerometer
    def accelfullScaleRange( self, fullScaleRange=0 ):
        '''
        Sets and reads the Accelerometers operating range and low pass filter frequencies
        fullScaleRange: 0,1,2,3 => +-2g,+-4g,+-8g,+-16g
        returns fullScaleRange
        ''' 
        if fullScaleRange != None and fullScaleRange in [0,1,2,3]:
            i2c.writeto_mem(0x69, 0x1C, pack('b',
            (i2c.readfrom_mem(0x69, 0x1C, 1)[0] & ~24) | fullScaleRange << 3
            ))

            # pick the accelerometer Sensitivity Scale Factor    
            self.accelSSF = 16834 #[16384,8192,4096,2048][fullScaleRange] 
    
        return (i2c.readfrom_mem(0x69, 0x1C, 1)[0] & 24) >> 3 

    def readAccel( self ):
        """
        return tuple of accelerations (x,y,z)
        North-East-Down(NED) as a fixed, parent coordinate system
        """

        y,x,z = unpack('>hhh',i2c.readfrom_mem(0x69, 0x3B, 6)) 

        x = x / self.accelSSF
        y = -1 * y / self.accelSSF
        z = -1 * z / self.accelSSF

        return x,y,z

    def readCalibratedAccel(self):
        ''' apply the calibrated accel bias to the raw accel values'''
        x,y,z = self.readAccel()
        xo, yo, zo = tuple(store.accelbias)
        return x-xo, y-yo, z-zo, self.deltat()  

    #Gyro
    def gyrofullScaleRange(self, fullScaleRange=None ):
        """    
        Sets and reads the Gyro full scal operting range
        fullScaleRange: 0,1,2,3 => +-250, +-500, +-1000, +-2000 degrees/second  
        """
        if fullScaleRange != None and fullScaleRange in [0,1,2,3]:
            i2c.writeto_mem(0x69, 0x1B, pack('b',
            (i2c.readfrom_mem(0x69, 0x1B, 1)[0] & ~24) | fullScaleRange << 3
            ))

            # pick the gyro Sensitivity Scale Factor    
            self.gyroSSF = 131 #[131,65.5,32.8,16.4][fullScaleRange] 

        return (i2c.readfrom_mem(0x69, 0x1B, 1)[0] & 24) >> 3 

    def gyroLowPassFilter(self, bandwidth=None ):
        """    
        Sets and reads the Gyro operating range and low pass filter frequencies
        bandwidth: 0,1,2,3,4,5,6,7 => 250Hz, 184Hz, 92Hz, 41Hz, 20Hz, 10Hz, 5Hz, 3600Hz
        """
        if bandwidth and bandwidth in [0,1,2,3,4,5,6,7]:
            i2c.writeto_mem(0x69, 0x1A, pack('b',
            (i2c.readfrom_mem(0x69, 0x1A, 1)[0] & ~7 ) | bandwidth
            ))

        return i2c.readfrom_mem(0x69, 0x1A, 1)[0] & 7  

    def readGyro( self ):
        """
        return tuple of degrees per second (x,y,z)
        North-East-Down(NED) as a fixed, parent coordinate system
        """
        y,x,z = unpack('>hhh',i2c.readfrom_mem(0x69, 0x43, 6)) 
        x = x / self.gyroSSF
        y = y / self.gyroSSF
        z = z / self.gyroSSF
        z = -1 * z

        return x,y,z         

    def readCalibratedGyro(self):
        ''' apply the calibrated accel bias to the raw accel values'''
        x,y,z = self.readGyro()
        xo, yo, zo = tuple(store.gyrobias)

        return x-xo, y-yo, z-zo, self.deltat()        

    #Magnetometer
    def initMag( self ):
        # Directly access the magnetomoeter via I2C BYPASS mode
        try:
            i2c.writeto_mem(0x69, 0x6B, b'\x80') #PWR_MGMT_1 = H_RESET # Rest the MPU6050 Magnetomoeter
            i2c.writeto_mem(0x69, 0x6A, b'\x00') #USER_CTRL_AD = I2C_MST = 0x00 disable i2c master
            i2c.writeto_mem(0x69, 0x37, b'\x02') #INT_PIN_CFG = BYPASS[1]
        except OSError as e:
            print('please check the MPU9250 I2C wiring ')

        # Read the Factory set Magntometer Sesetivity Adjustments
        i2c.writeto_mem(0x0C, 0x0A, b'\x1F') #CNTL1 Fuse ROM mode
        utime.sleep_ms(100) # Settle Time

        # Read factory calibrated sensitivity constants
        asax, asay, asaz = unpack('<bbb',i2c.readfrom_mem(0x0C, 0x10, 3)) 

        # Calculate the Magnetometer Sesetivity Adjustments
        self.asax = (((asax-128)*0.5)/128)+1
        self.asay = (((asay-128)*0.5)/128)+1
        self.asaz = (((asaz-128)*0.5)/128)+1

        # Set Register CNTL1 to 16-bit output, Continuous measurement mode 100Hz
        i2c.writeto_mem(0x0C, 0x0A, b'\x16') 

       
    def readMag( self, bias=(0,0,0,1,1,1,1,1,1) ):
        """
        return tuple of magnetometer measurements (x,y,z)
        North-East-Down(NED) as a fixed, parent coordinate system      
        """

        #Data Ready
        DRDY = i2c.readfrom_mem(0x0C, 0x02, 1)[0] & 0x01
 
        if DRDY != 0x01 : # Data is ready
            raise MagDataNotReady()

        x,y,z = unpack('<hhh',i2c.readfrom_mem(0x0C, 0x03, 6))  

        HOFL = i2c.readfrom_mem(0x0C, 0x09, 1)[0] & 0x08

        # apply the Factory Magentometer Sensetivity adjustment
        x,y,z = x * self.asax, y * self.asay , z * self.asaz

        # apply offset
        x,y,z = x - bias[0], y - bias[1], z - bias[2]

        # apply normalize
        x,y,z = x / bias[3], y / bias[4], z / bias[5]

        # apply scale
        x,y,z = x * bias[6], y * bias[7], z * bias[8]

        return x,y,z

    def readMagHeading(self):
        '''returns the magnetic heading in degrees:  -179 -> 180 degrees'''
        x,y,_ = self.readMag( tuple(store.magbias) )
        return int(degrees(atan2(x,y)))

    #Temperature Sensor
    def readTemp( self ):
        """
        return temperature in deg Celcius
        """
        temp = unpack('>h',i2c.readfrom_mem(0x69, 0x41, 2)) 
        temp = ((temp[0] - store.tempoffset) / store.tempsensitivity) + 21

        return temp

    #Helper Functions
    def deltat(self):
        '''
        To assist integration
        Calculates for the differince in time between updates 
        '''
        currentTime = utime.ticks_us()

        if self.startTime is None:
            self.startTime = currentTime
            return 0.0001  # 100μs notional delay. 1st reading is invalid in any case

        deltaT =  utime.ticks_diff(currentTime,self.startTime )/1000000
        self.startTime = currentTime
        return deltaT



