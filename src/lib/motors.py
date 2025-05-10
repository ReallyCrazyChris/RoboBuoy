import uasyncio as asyncio
from machine import PWM, Pin
from math import radians, pi
from lib.store import Store
from lib.utils import translateValue

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


def driveMotors(vl=0,vr=0):
    ''' drive the motors with the given speed '''
    # clamp max and min motor speeds 0..1 
    vleft = min(1, max(0, vl)) 
    vright = min(1, max(0, vr)) 

    # Translate the speed [0..1] to a PWM value 
    pwmLeft = int( translateValue(vleft,0,1,store.minPwmLeft,store.maxpwm))
    pwmRight = int( translateValue(vright,0,1,store.minPwmRight,store.maxpwm))

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

        p = 0
        i = 0
        d = 0

        while True:

            await asyncio.sleep_ms(10)
            currentTime = utime.ticks_us()
            deltaT =  utime.ticks_diff(currentTime,startTime )/1000000
            startTime = currentTime

            # update the proportional error
            store.error = store.desiredcourse - store.currentcourse # radians
            p = store.Kp * store.error

            # update the integral error
            if store.Ki > 0:
                store.errSum = store.errSum + (store.error * deltaT) # s/radians
            i = store.Ki * store.errSum
            
            # update the differential error
            if store.Kd > 0:
                store.dErr = (store.error - store.lastErr) / deltaT #radians/s
                store.lastErr = store.error
            
            d = store.Kd * store.dErr

            # steer is between -pi and pi radians
            store.steer = normalize(p + i + d) # radians
            
            #print table of the PID values, with fixed table widths
            #print("p: %5.2f i: %5.2f d: %5.2f steer: %5.2f" % (p, i, d, store.steer))

            #print t able of differential values
            #print("P: %5.2f dErr: %5.2f lastErr: %5.2f d %5.2f" % (p,store.dErr, store.lastErr, d)) 
   
    
          
            
  
    except asyncio.CancelledError:
        print( "stopping pidTask" )


async def driveTask():
    '''' drive the motors with the given speed '''
    try:
        print('starting driveMotorsTask')
        while 1:

            # surge is between 0 and 1
            # steer is between -pi and pi radians
            # steer is translated to a value between 0 and 1
            # vl is between 0 and 1
            # vr is between 0 and 1

            vl = (store.surge + translateValue(store.steer,-pi,pi,-1,1)) / 2
            vr = (store.surge - translateValue(store.steer,-pi,pi,-1,1)) / 2
            
            driveMotors(vl,vr)

            await asyncio.sleep_ms(20) # TODO Try without this delay 

    except asyncio.CancelledError:  
            stopMotors()
            print( "stopping driveMotorsTask") 

 