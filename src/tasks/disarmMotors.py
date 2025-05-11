import uasyncio as asyncio

from driver.motors import armMotors, disarmMotors
from math import pi
from storage.store import Store
store = Store.instance()

async def disarmMotorsTask():
    '''' drive the motors with the given speed '''
    try:
        print('starting disarmMotorsTask')
        disarmMotors()
        await asyncio.sleep_ms(100)
        print('disarmMotorsTask done')

    except asyncio.CancelledError:  
        disarmMotors()
            

