import uasyncio as asyncio
from machine import PWM, Pin
from math import radians
from lib.store import Store
store = Store()

# PWM control of ESC motor controlers 
motorLeft = PWM(Pin(2))
motorRight = PWM(Pin(13))

#motorLeft = PWM(Pin(16))
#motorRight = PWM(Pin(17))

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

async def driveTask():
    ''' drive motors (steer in degrees -180..180 , surge in cm/s) '''
    try:
        print('starting driveMotorsTask')
        while 1:

            vl = (2*store.surge + radians(store.steer)) / 2
            vr = (2*store.surge - radians(store.steer)) / 2

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

            await asyncio.sleep_ms(10) #Try without

    except asyncio.CancelledError:  
            motorLeft.duty(0)
            motorRight.duty(0)  
            print( "stopping driveMotorsTask") 

        
          

     
