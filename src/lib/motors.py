import uasyncio as asyncio
from machine import PWM, Pin
from math import radians
from lib import server
from lib.store import Store
store = Store()

# PWM control of ESC motor controlers 
motorLeft = PWM(Pin(16))
motorRight = PWM(Pin(17))
motorLeft.freq(50)
motorRight.freq(50)
motorLeft.duty(0)
motorRight.duty(0)   
        
########################
# Arm Motors Task
def startArmMotorsTask():
    armmotors = asyncio.create_task( armMotorsTask() )
    server.addListener('stopArmMotorsTask', armmotors.cancel) 

server.addListener('startArmMotorsTask', startArmMotorsTask)

async def armMotorsTask():
    ''' arm esc motor controllers '''
    try:
        print('starting armMotorsTask')
            
        motorLeft.duty(40)
        motorRight.duty(40)
        await asyncio.sleep_ms(3000) 
        motorLeft.duty(115)
        motorRight.duty(115)
        await asyncio.sleep_ms(3000) 
        motorLeft.duty(0)
        motorRight.duty(0) 

    except asyncio.CancelledError:
        print( "stopping armMotorsTask") 

########################
# Drive Motors Task
def startDriveMotorsTask():
    drivemotors = asyncio.create_task( driveMotorsTask() )
    server.addListener('stopDriveMotorsTask', drivemotors.cancel) 

server.addListener('startDriveMotorsTask', startDriveMotorsTask)

async def driveMotorsTask():
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

            pwm_left = (vl - store.vmin) * (store.maxpwm - store.mpl) / (store.vmax - store.vmin) + store.mpl
            pwm_left = int(pwm_left)
            motorLeft.duty(pwm_left)
    
            pwm_right = (vr - store.vmin) * (store.maxpwm - store.mpr) / (store.vmax - store.vmin) + store.mpr
            pwm_right = int(pwm_right)
            motorRight.duty(pwm_right)

            await asyncio.sleep_ms(10) #Try without

    except asyncio.CancelledError:
            
            motorLeft.duty(0)
            motorRight.duty(0)  
            print( "stopping driveMotorsTask") 

        
          

     
