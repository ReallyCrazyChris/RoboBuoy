import uasyncio as asyncio
from driver.motors import driveMotors, stopMotors

async def slowRightRotateTask():
    '''' drive the motors with the given speed '''
    try:
        print('starting slowRightRotateTask')
        while 1:
            
            driveMotors(0.1,0) # slow right rotate
            await asyncio.sleep_ms(20) # TODO Try without this delay 

    except asyncio.CancelledError:  
            stopMotors()
            print( "stopping slowRightRotateTask") 