"""
Micropython driver for the I2C MPU9250 9-DOF Sensor
"""
import utime
import uasyncio as asyncio
from struct import pack, unpack


class MPU9250(object):
  
    def __init__( self, i2c ):

        self.i2c = i2c 

        self.startTime = None
        self.accel = (0,0,0)
        self.accelOffset = (0,0,0)
        self.gyro = (0,0,0)
        self.gyroOffset = (0,0,0)
        self.gyroSSF = 131
        self.mag = (0,0,0)
        self.tempOffset = 0
        self.tempSensetivity = 321
        
        self.initMag()
        self.initAccel(fullScaleRange=0)
        self.gyrofullScaleRange(fullScaleRange = 0)
        self.gyroLowPassFilter(bandwidth = 6)

        self.ticks = 0
        self.ticksMag = 0


    def initMag( self ):
        # Directly access the magnetomoeter via I2C BYPASS mode
        try:
            self.i2c.writeto_mem(0x69, 0x6B, b'\x80') #PWR_MGMT_1 = H_RESET # Rest the MPU6050
            self.i2c.writeto_mem(0x69, 0x6A, b'\x00') #USER_CTRL_AD = I2C_MST = 0x00 disable i2c master
            self.i2c.writeto_mem(0x69, 0x37, b'\x02') #INT_PIN_CFG = BYPASS[1]
        except OSError as e:
            print('please check the MPU9250 I2C wiring ')

        # Read the Factory set Magntometer Sesetivity Adjustments
        self.i2c.writeto_mem(0x0C, 0x0A, b'\x1F') #CNTL1 Fuse ROM mode
        utime.sleep_ms(100) # Settle Time

        # Read factory calibrated sensitivity constants
        msax, msay, msaz = unpack('<bbb',self.i2c.readfrom_mem(0x0C, 0x10, 3)) 

        # Calculate the Magnetometer Sesetivity Adjustments
        self.msax = (((msax-128)*0.5)/128)+1
        self.msay = (((msay-128)*0.5)/128)+1
        self.msaz = (((msaz-128)*0.5)/128)+1

        print('Magnetometer Sesetivity Adjustments', msax,msay,msaz )
        # Set Register CNTL1 to 16-bit output, Continuous measurement mode 100Hz
        self.i2c.writeto_mem(0x0C, 0x0A, b'\x16') 
        utime.sleep_ms(100) # Settle Time

    def initAccel( self, fullScaleRange=0 ):
        '''
        Sets and reads the Accelerometers operating range and low pass filter frequencies
        fullScaleRange: 0,1,2,3 => +-2g,+-4g,+-8g,+-16g
        returns fullScaleRange
        ''' 
        if fullScaleRange != None and fullScaleRange in [0,1,2,3]:
            self.i2c.writeto_mem(0x69, 0x1C, pack('b',
            (self.i2c.readfrom_mem(0x69, 0x1C, 1)[0] & ~24) | fullScaleRange << 3
            ))

            # pick the accelerometer Sensitivity Scale Factor    
            self.accelSSF = [16384,8192,4096,2048][fullScaleRange] 
    
        return (self.i2c.readfrom_mem(0x69, 0x1C, 1)[0] & 24) >> 3 

    def readAccel( self ):
        """
        return tuple of accelerations (x,y,z)
        """
        x,y,z = unpack('>hhh',self.i2c.readfrom_mem(0x69, 0x3B, 6)) 

        x = x / self.accelSSF
        y = y / self.accelSSF
        z = z / self.accelSSF

        return x,y,z
  

    def readGyro( self ):
        """
        return tuple of degrees per second (x,y,z)
        """
        x,y,z = unpack('>hhh',self.i2c.readfrom_mem(0x69, 0x43, 6)) 
        x = x / self.gyroSSF
        y = y / self.gyroSSF
        z = z / self.gyroSSF

        return x,y,z 

        
    def readTemp( self ):
        """
        return temperature in deg Celcius
        """
        temp = unpack('>h',self.i2c.readfrom_mem(0x69, 0x41, 2)) 
        temp = ((temp[0] - self.tempOffset) / self.tempSensetivity) + 21

        return temp

    
    def readAccelGyroTemp( self ):

        """
        reads Accel, Gyro and Temp in one Read Cycle
        """

        ax,ay,az, temp, gx,gy,gz = unpack('>hhhhhhh',self.i2c.readfrom_mem(0x69, 0x3B, 14)) 

        ax = ax / self.accelSSF
        ay = ay / self.accelSSF
        az = az / self.accelSSF

        gx = gx / self.gyroSSF
        gy = gy / self.gyroSSF
        gz = gz / self.gyroSSF

        # calibratre the temperature
        temp = ((temp - self.tempOffset) / self.tempSensetivity) + 21

        # calculate time delta
        ticks = utime.ticks_us()
        deltaT = utime.ticks_diff( ticks, self.ticks )
        self.ticks = ticks

        return  abs(ax),ay,az,gx,gy,gz,temp,deltaT


    def gyrofullScaleRange(self, fullScaleRange=None ):
        """    
        Sets and reads the Gyro full scal operting range
        fullScaleRange: 0,1,2,3 => +-250, +-500, +-1000, +-2000 degrees/second  
        """
        if fullScaleRange != None and fullScaleRange in [0,1,2,3]:
            self.i2c.writeto_mem(0x69, 0x1B, pack('b',
            (self.i2c.readfrom_mem(0x69, 0x1B, 1)[0] & ~24) | fullScaleRange << 3
            ))

            # pick the gyro Sensitivity Scale Factor    
            self.gyroSSF = [131,65.5,32.8,16.4][fullScaleRange] 

        return (self.i2c.readfrom_mem(0x69, 0x1B, 1)[0] & 24) >> 3 

    def gyroLowPassFilter(self, bandwidth=None ):
        """    
        Sets and reads the Gyro operating range and low pass filter frequencies
        bandwidth: 0,1,2,3,4,5,6,7 => 250Hz, 184Hz, 92Hz, 41Hz, 20Hz, 10Hz, 5Hz, 3600Hz
        """
        if bandwidth and bandwidth in [0,1,2,3,4,5,6,7]:
            self.i2c.writeto_mem(0x69, 0x1A, pack('b',
            (self.i2c.readfrom_mem(0x69, 0x1A, 1)[0] & ~7 ) | bandwidth
            ))

        return self.i2c.readfrom_mem(0x69, 0x1A, 1)[0] & 7   


    def readMag( self ):
        
        DRDY = self.i2c.readfrom_mem(0x0C, 0x02, 1)[0] & 0x01

        # Is data ready
        if DRDY != 0x01 : 
            raise Exception()

        # Correct the orentation of the magnetometer to align with the accelermeter and gyro
        my,mx,mz = unpack('<hhh',self.i2c.readfrom_mem(0x0C, 0x03, 6))  
        mz = -1 * mz

        # Magnetic sensor overflow occurred   
        HOFL = self.i2c.readfrom_mem(0x0C, 0x09, 1)[0] & 0x08

        # calculate time delta 
        ticks = utime.ticks_us()
        deltaT = utime.ticks_diff(ticks, self.ticksMag)
        self.ticksMag = ticks
  
        # apply the Factory Magentometer Sensetivity adjustment
        mx,my,mz = mx * self.msax, my * self.msay , mz * self.msaz

        return mx,my,mz, deltaT

    async def readAccelGyroTempTask( self ):
        while True:
            try:
                print(self.readAccelGyroTemp())
            except Exception:
                pass
            await asyncio.sleep_ms(0)

    async def readMagTask( self ):
        while True:
            try:
                print(self.readMag())
            except Exception:
                pass
            await asyncio.sleep_ms(0)            
