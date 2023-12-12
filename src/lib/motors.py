import uasyncio as asyncio
from machine import PWM, Pin
from math import radians
from lib.store import Store
store = Store.instance()

# PWM control of ESC motor controlers 
motorLeft = PWM(Pin(2))
motorRight = PWM(Pin(13))

motorLeft.freq(50)
motorRight.freq(50)
motorLeft.duty(0)
motorRight.duty(0)   
        
async def armMotorsCoroutine():
    ''' arm esc motor controllers '''     
    motorLeft.duty(40)
    motorRight.duty(40)
    await asyncio.sleep_ms(1000) 
    motorLeft.duty(115)
    motorRight.duty(115)
    await asyncio.sleep_ms(1000) 
    motorLeft.duty(0)
    motorRight.duty(0) 

def driveMotors(pwmleft=0,pwmright=0):
    motorLeft.duty(pwmleft)
    motorRight.duty(pwmright)  
     
def stopMotors():
    motorLeft.duty(0)
    motorRight.duty(0)  


########################
# Steering PID Controller
async def pidTask():
    ''' 
    The goal of the PID controller is to get the robot to follow 
    the desired course, considering the current course
    '''
    import utime
    from lib.utils import constrain
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
            error = store.desiredcourse - store.currentcourse
            
            if abs(error) <= 180:
               store.error = error
               #print("_cw",store.error)
            else:
               store.error = error - 360
               #print("ccw",store.error)

            # update the integral error
            if store.Ki > 0 :
                store.errSum = store.errSum + (store.error * deltaT)
            
            # update the differential error
            if store.Kd > 0:
                store.dErr = (store.error - store.lastErr) / deltaT

            # summate the PID and drive the output steering value    
            store.steer = constrain((store.Kp * store.error) + (store.Ki * store.errSum) + (store.Kd * store.dErr))
            
            #print(store.error, store.steer, deltaT)

            # keep current error for the next PID cycle
            store.lastErr = store.error
  
    except asyncio.CancelledError:
        print( "stopping pidTask" )


async def driveTask():
    ''' drive motors (steer in degrees -180..180 , surge in cm/s) '''
    try:
        print('starting driveMotorsTask')
        while 1:

            vl = (2*store.surge + radians(store.steer)*store.steergain) / 2
            vr = (2*store.surge - radians(store.steer)*store.steergain) / 2

            # clamp max and min motor speeds  
            vl = min(store.vmax,vl)
            vl = max(store.vmin,vl)
            vr = min(store.vmax,vr)
            vr = max(store.vmin,vr)

            pwm_left = (vl - store.vmin) * (store.maxpwm - store.mpl) / (100 - store.vmin) + store.mpl
            pwm_left = int(pwm_left)
            motorLeft.duty(pwm_left)
    
            pwm_right = (vr - store.vmin) * (store.maxpwm - store.mpr) / (100 - store.vmin) + store.mpr
            pwm_right = int(pwm_right)
            motorRight.duty(pwm_right)

            #print('s',store.surge,' r',store.steer,' vl',vl,' vr',vr,' pl',pwm_left,' pr',pwm_right)

            await asyncio.sleep_ms(20) #Try without

    except asyncio.CancelledError:  
            motorLeft.duty(0)
            motorRight.duty(0)  
            print( "stopping driveMotorsTask") 

        
          

     
