import uasyncio as asyncio
from lib.utils import translateValue
from storage.store import Store
store = Store.instance()

# PWM control of ESC motor controlers 
motorLeft = None
motorRight = None

def armMotors():
    ''' arm the eft anf right motors '''
    from machine import PWM, Pin
    from constants.pins import PWM_left_pin, PWM_right_pin
    global motorLeft
    global motorRight

    if motorLeft is None and motorRight is None:
        # set the duty cycle to the minimum value
        store.minPwmLeft = store.minPwmLeft if store.minPwmLeft > 0 else 3712
        store.minPwmRight = store.minPwmRight if store.minPwmRight > 0 else 3712
        # create the PWM objects for the motors
        motorLeft = PWM(Pin(PWM_left_pin),  freq=50)
        motorRight = PWM(Pin(PWM_right_pin), freq=50)
        # set the duty cycle to the minimum value
        motorLeft.duty_u16(store.minPwmLeft)
        motorRight.duty_u16(store.minPwmRight)

def disarmMotors():
    ''' disarm the left and right motors '''
    global motorLeft
    global motorRight

    if motorLeft is not None and motorRight is not None:
        # set the duty cycle to the minimum value
        motorLeft.duty_u16(0)
        motorRight.duty_u16(0)
        motorLeft.deinit()
        motorRight.deinit()
        motorLeft = None
        motorRight = None        


def driveMotors(vl=0,vr=0):
    ''' drive the motors with the given speed '''

    # clamp max and min motor speeds 0..1 
    vleft = min(1, max(0, vl)) 
    vright = min(1, max(0, vr)) 

    # Translate the speed [0..1] to a PWM value 
    pwmLeft = int( translateValue(vleft,0,1,store.minPwmLeft,store.maxpwm))
    pwmRight = int( translateValue(vright,0,1,store.minPwmRight,store.maxpwm))

    # Drive the motors
    if motorLeft and motorRight: 
        motorLeft.duty_u16(pwmLeft)
        motorRight.duty_u16(pwmRight)

def stopMotors():
    ''' stop the motors by applying the minimum pwm duty cycle '''
    store.minPwmLeft = store.minPwmLeft if store.minPwmLeft > 0 else 3712
    store.minPwmRight = store.minPwmRight if store.minPwmRight > 0 else 3712
    motorLeft.duty_u16(store.minPwmLeft) 
    motorRight.duty_u16(store.minPwmRight)  
    #motorLeft.duty_u16(0)
    #motorRight.duty_u16(0)    









 