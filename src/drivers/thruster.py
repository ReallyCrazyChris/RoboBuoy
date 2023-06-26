import struct
from math import sin, radians
from drivers.i2c import i2c

class Thruster():
    def __init__( self ):
        
        self.active = False # If the thrusters my run or not
        self.currentTheta = 0 # current rate of rotation rad_s
        self.desiredTheta = 0 # desired rate of rotation rad_s

        #PID tuning gains
        self.Kp = 90
        self.Ki = 10
        self.Kd = 0

        #PID variables
        self.error = 0
        self.errSum = 0
        self.dErr = 0      
        self.lastErr = 0  # Previous error  


    def thetaPID( self, desiredTheta, currentTheta, deltaT ):
        ''' sets the angular rotation of the the robot '''
        
        if self.active:

            self.desiredTheta = desiredTheta
            self.currentTheta = currentTheta
            
            #PID error calculations
            self.error  = self.desiredTheta - self.currentTheta
            self.errSum = self.errSum + (self.error * deltaT)
            self.dErr = (self.error - self.lastErr) / deltaT
            
            #PID output w in rad_s
            w = (self.Kp * self.error) + (self.Ki * self.errSum) + (self.Kd * self.dErr)

            print((self.Kp * self.error), (self.Ki * self.errSum), (self.Kd * self.dErr), w)

            self.lastErr = self.error

            powerleft = round(w)
            powerright = round(-1 * w)

            # clamp the power 
            powerleft = min(254,powerleft)
            powerleft = max(powerleft,-254)
            # clamp the power 
            powerright = min(254,powerright)
            powerright = max(powerright,-254)

            #Left Motor
            if powerleft > 0:
                i2c.writeto(0x14, struct.pack('bbb',0x02,0,powerleft))
            
            elif powerleft < 0:
                i2c.writeto(0x14, struct.pack('bbb',0x03,0,powerleft*-1))

            else:
                i2c.writeto(0x14, struct.pack('bb',0x01,0))

            #Right Motor
            if powerright > 0:
                i2c.writeto(0x14, struct.pack('bbb',0x02,1,powerright))
            
            elif powerright < 0:
                i2c.writeto(0x14, struct.pack('bbb',0x03,1,powerright*-1))

            else:
                i2c.writeto(0x14, struct.pack('bb',0x01,1))

        else:
            #stop both motors
            i2c.writeto(0x14, struct.pack('bb',0x01,1)) # Stop Left
            i2c.writeto(0x14, struct.pack('bb',0x01,0)) # Stop Right

            

 