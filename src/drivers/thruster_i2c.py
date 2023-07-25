import struct
from math import sin, radians

class Thruster(  ):
    def __init__( self, i2c ):
        
        self.i2c = i2c
  

    def drive(self,steer,surge):
        """
        from steer in rad/s and surge in meters/s
        determin the needed left and right motor speeds in rad/s
        """
        if self.motorsactive:
            speedleft = round(255 * steer) + surge
            speedright = round(-255 * steer) + surge

            # clamp the speed in range -254..254
            speedleft = min(254,speedleft)
            speedleft = max(speedleft,-254)
            # clamp the speed in range -254..254
            speedright = min(254,speedright)
            speedright = max(speedright,-254)
            
            self.drivemotors(speedleft,speedright)
        else:
            self.stopmotors()


    def drivemotors(self,speedleft,speedright):
        """
        drives the motor right and left speeds in rad/s
        """      

        self.speedleft = speedleft
        self.speedright = speedright

        #Left Motor
        if speedleft > 0:
            self.i2c.writeto(0x14, struct.pack('bbb',0x02,0,speedleft))
        
        elif speedleft < 0:
            self.i2c.writeto(0x14, struct.pack('bbb',0x03,0,speedleft*-1))

        else:
            self.i2c.writeto(0x14, struct.pack('bb',0x01,0))

        #Right Motor
        if speedright > 0:
            self.i2c.writeto(0x14, struct.pack('bbb',0x02,1,speedright))
        
        elif speedright < 0:
            self.i2c.writeto(0x14, struct.pack('bbb',0x03,1,speedright*-1))

        else:
            self.i2c.writeto(0x14, struct.pack('bb',0x01,1))

    def stopmotors(self):
        """
        stops both motors
        """
        self.i2c.writeto(0x14, struct.pack('bb',0x01,1)) # Stop Left
        self.i2c.writeto(0x14, struct.pack('bb',0x01,0)) # Stop Right
