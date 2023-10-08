import uasyncio as asyncio
from machine import PWM, Pin
from math import radians
from lib import server
from lib.store import Store
store = Store()

# PWM control of ESC motor controlers 
motorLeft  = PWM(Pin(16))
motorRight = PWM(Pin(17))
motorLeft.freq(50)
motorRight.freq(50)
        

async def armmotors():
    ''' arm esc motor controllers '''
    print('arm motors')
    motorLeft.duty(40)
    motorRight.duty(40)
    await asyncio.sleep_ms(3000) 
    motorLeft.duty(115)
    motorRight.duty(115)
    await asyncio.sleep_ms(3000) 
    motorLeft.duty(0)
    motorRight.duty(0)
    print('motors armed')

    def drive():
        ''' drive motors (steer in degrees -180..180 , surge in cm/s) '''

        vl = (2*store.surge + radians(store.steer)*store.steergain) / 2
        vr = (2*store.surge - radians(store.steer)*store.steergain) / 2

        # clamp max and min motor speeds  
        vl = min(store.vmax,vl)
        vl = max(store.vmin,vl)
        vr = min(store.vmax,vr)
        vr = max(store.vmin,vr)

        if store.active:

            pwm_left = (vl - store.vmin) * (store.maxpwm - store.mpl) / (store.vmax - store.vmin) + store.mpl
            pwm_left = int(pwm_left)
            motorLeft.duty(pwm_left)
    
            pwm_right = (vr - store.vmin) * (store.maxpwm - store.mpr) / (store.vmax - store.vmin) + store.mpr
            pwm_right = int(pwm_right)
            motorRight.duty(pwm_right)

        else:
            motorLeft.duty(0)
            motorRight.duty(0)   
          
    def stop():
        '''stops both motors'''
        motorLeft.duty(0)
        motorRight.duty(0)        
