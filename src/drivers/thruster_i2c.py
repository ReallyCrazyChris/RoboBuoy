import struct
from math import sin, radians
from drivers.i2c import i2c

def mixer( rudder, power ):
    
    """
    Mixes rudder and desired speed
    to control the power and direction of the differntial thrusters
    power -1 .. 0 .. 1
    rudder -1 .. 0 .. 1
    """
    
    # calculate power to left and right motors
    powerleft = 0
    powerright = 0

    #rudder = sin( radians( rudder )) 

    powerleft =    power + rudder
    powerright =   power - rudder

    powerleft = min(1.0,powerleft)
    powerleft = max(powerleft,-1.0)

    powerright = min(1.0,powerright)
    powerright = max(powerright,-1.0)

    # apply power to motors
    left( powerleft )
    right( powerright )

    return powerleft, powerright

def left( power=0 ):
    """
    controls the speed and direction for the left thruster motor
    power -1 .. 0 .. 1
    """
    if power > 0:
        i2c.writeto(0x14, struct.pack('bbb',0x02,0,round(255*power)))
      
    elif power < 0:
        i2c.writeto(0x14, struct.pack('bbb',0x03,0,round(255*power*-1)))

    else:
        i2c.writeto(0x14, struct.pack('bb',0x01,0))

def right( power=0 ):
    """
    controls the speed and direction for the right thruster motor
    power -1 .. 0 .. 1
    """
    if power > 0:
        i2c.writeto(0x14, struct.pack('bbb',0x02,1,round(255*power)))
      
    elif power < 0:
        i2c.writeto(0x14, struct.pack('bbb',0x03,1,round(255*power*-1)))

    else:
        i2c.writeto(0x14, struct.pack('bb',0x01,1))