import uasyncio as asyncio
from lib.store import Store
store = Store.instance()

from lib import motors

async def testmotors():
    
    # ARM
    print(' arm motors')
    await motors.armMotorsCoroutine()
    print(' arm motors done')

    await asyncio.sleep_ms(3000) 

    # Left Motor
    print(' drive left motor : minimum forward speed')
    motors.driveMotors(store.mpl,0)
    await asyncio.sleep_ms(3000) 
    print(' drive left motor : maximum forward speed')
    motors.driveMotors(store.maxpwm,0)
    await asyncio.sleep_ms(3000) 
    motors.stopMotors()
    print(' stop motors')

    await asyncio.sleep_ms(3000) 

    # Right Motor
    print(' drive right motor : minimum forward speed')
    motors.driveMotors(0,store.mpr)
    await asyncio.sleep_ms(3000) 
    print(' drive right motor : maximum forward speed')
    motors.driveMotors(0,store.maxpwm)
    await asyncio.sleep_ms(3000) 
    motors.stopMotors()
    print(' stop motors')
  
  