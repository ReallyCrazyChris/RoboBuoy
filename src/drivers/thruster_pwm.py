import machine

""" Provides Dual Thruster Style Motor Control """

# pwm motor outputs
rightfwd = machine.PWM(machine.Pin(5), freq=1000)   #D1
rightrev = machine.PWM(machine.Pin(4), freq=1000)   #D2
leftrev = machine.PWM(machine.Pin(0), freq=1000)    #D3
leftfwd = machine.PWM(machine.Pin(2), freq=1000)    #D4

# initialidze: stop motors
rightfwd.duty(1023)
rightrev.duty(1023)
leftfwd.duty(1023)
leftrev.duty(1023)


def mixer( rudderAngle, desiredPower ):
    
    """
    Mixes rudderAngle and desired speed
    to control the power and direction of the differntial thrusters

    rudder angle in radians
    power -1 .. 0 .. 1
    rudder -PI .. 0 .. PI
    """
    
    # calculate power to left and right motors
    powerleft = 0
    powerright = 0

    powerleft =   2/pi * rudderAngle + desiredPower
    powerright = -2/pi * rudderAngle + desiredPower

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
        leftrev.duty(1023)
        leftfwd.duty(1023-round(1023*power))
      
    elif power < 0:
        leftfwd.duty(1023)
        leftrev.duty(1023+round(1023*power))

    else:
        leftfwd.duty(1023)
        leftrev.duty(1023)


def right( power=0 ):
    """
    controls the speed and direction for the right thruster motor
    power -1 .. 0 .. 1
    """
    
    if power > 0:
        rightrev.duty(1023)
        rightfwd.duty(1023-round(1023*power))
      
    elif power < 0:
        rightfwd.duty(1023)
        rightrev.duty(1023+round(1023*power))

    else:
        rightfwd.duty(1023)
        rightrev.duty(1023)
