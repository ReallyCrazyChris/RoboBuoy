import uasyncio as asyncio

from driver.motors import armMotors, disarmMotors
from math import pi
from storage.store import Store
store = Store.instance()

async def armMotorsTask():
    '''' drive the motors with the given speed '''
    try:
        print('starting armMotorsTask')
        armMotors()
        await asyncio.sleep_ms(100)

    except asyncio.CancelledError:  
        disarmMotors()
            

