import uasyncio as asyncio
from machine import PWM, Pin
from math import radians
from lib.store import Store

store = Store.instance()

# PWM control of ESC motor controlers 
motorLeft = None
motorRight = None

async def armMotorsCoroutine():
    armMotors()
    await asyncio.sleep_ms(1000) # wait for the motors to be armed
    # set the duty cycle to the minimum value

def armMotors():
    ''' arm the motors '''
    global motorLeft
    global motorRight

    if motorLeft is None and motorRight is None:
        print(' arm motors')
        # set the duty cycle to the minimum value
        store.minPwmLeft = store.minPwmLeft if store.minPwmLeft > 0 else 3712
        store.minPwmRight = store.minPwmRight if store.minPwmRight > 0 else 3712
        # create the PWM objects for the motors
        motorLeft = PWM(Pin(2),  freq=50)
        motorRight = PWM(Pin(13), freq=50)
        motorLeft.duty_u16(store.minPwmLeft)
        motorRight.duty_u16(store.minPwmRight)

def disarmMotors():
    ''' disarm the motors '''
    global motorLeft
    global motorRight

    if motorLeft is not None and motorRight is not None:
        print(' disarm motors')
        # set the duty cycle to the minimum value
        motorLeft.duty_u16(0)
        motorRight.duty_u16(0)
        motorLeft.deinit()
        motorRight.deinit()
        motorLeft = None
        motorRight = None        

def translateSpeedPWM(speed,minSpeed,maxSpeed,minPWM,maxPWM):
    ''' Translate speed to PWM value '''
    # motor speed is between 0 and 1
    # pwm is between minPWM and maxPWM
    speed = min(maxSpeed, max(minSpeed, speed)) # clamp to min and max speed

    # map speed to pwm
    pwm =(speed-minSpeed)/(maxSpeed-minSpeed)*(maxPWM-minPWM)+minPWM
    return int(pwm)




def driveMotors(vl=0,vr=0):
    ''' drive the motors with the given speed '''
    # clamp max and min motor speeds  
    _vl = min(store.vmax, max(store.vmin, vl)) 
    _vr = min(store.vmax, max(store.vmin, vr)) 

    # Translate the speed [0..1] to a PWM value 
    pwmLeft = translateSpeedPWM(_vl,store.vmin,store.vmax,store.minPwmLeft,store.maxpwm)
    pwmRight = translateSpeedPWM(_vr,store.vmin,store.vmax,store.minPwmRight,store.maxpwm)

    # Drive the motors
    motorLeft.duty_u16(pwmLeft)
    motorRight.duty_u16(pwmRight)

def stopMotors():
    motorLeft.duty_u16(0) 
    motorRight.duty_u16(0)  


########################
# Steering PID Controller
async def pidTask():
    ''' 
    The goal of the PID controller is to get the robot to follow 
    the desired course, considering the current course
    '''
    import utime
    from lib.utils import normalize
    # clear the error accumulators
    store.errSum = 0
    store.dErr = 0
    startTime = utime.ticks_us()

    try: 
        print('starting pidTask')
        while True:

            await asyncio.sleep_ms(10)
            currentTime = utime.ticks_us()
            deltaT =  utime.ticks_diff(currentTime,startTime )/1000000
            startTime = currentTime

            # Choose the shortest direction rotation
            store.error = store.desiredcourse - store.currentcourse
            

            # update the integral error
            if store.Ki > 0 :
                store.errSum = store.errSum + (store.error * deltaT)
                # constrain the integral error to prevent windup
                store.errSum = min(1.6, max(-1.6, store.errSum)) 

            # update the differential error
            if store.Kd > 0:
                store.dErr = (store.error - store.lastErr) / deltaT

            # calculate the PID output
            # steer is between -PI and PI radians
            # steer = Kp * error + Ki * errSum + Kd * dErr

            store.steer = normalize((store.Kp * store.error) + (store.Ki * store.errSum) + (store.Kd * store.dErr))
            
            #print table of the PID values, with fixed table widths
            #print("error: %5.2f Kp: %5.2f Ki: %5.2f Kd: %5.2f err: %5.2f errSum: %5.2f dErr: %5.2f steer: %5.2f" % (store.error, store.Kp, store.Ki, store.Kd, store.error, store.errSum, store.dErr, store.steer))

    
            # keep current error for the next PID cycle
            store.lastErr = store.error
  
    except asyncio.CancelledError:
        print( "stopping pidTask" )


async def driveTask():
    ''' drive motors (steer in degrees -180..180 , surge in cm/s) '''
    try:
        print('starting driveMotorsTask')
        while 1:

            #vl = (2*store.surge + radians(store.steer)*store.steergain) / 2
            #vr = (2*store.surge - radians(store.steer)*store.steergain) / 2

            vl = (2*store.surge + store.steer) / 2
            vr = (2*store.surge - store.steer) / 2

            driveMotors(vl,vr)
            await asyncio.sleep_ms(20) # TODO Try without this delay 

    except asyncio.CancelledError:  
            stopMotors()
            print( "stopping driveMotorsTask") 

 