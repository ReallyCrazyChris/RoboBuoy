import uasyncio as asyncio
from lib.store import Store
store = Store.instance()

from lib import motors

async def testmotors():
    
    # ARM
    print(' arm motors')
    motors.armMotors()
    await asyncio.sleep_ms(1000) # wait for the motors to be armed
    print(' arm motors done')


    # Left Motor
    print(' drive left motor : minimum forward speed',store.minPwmLeft)
    motors.driveMotors(store.minPwmLeft,0)
    await asyncio.sleep_ms(3000) 
    print(' drive left motor : maximum forward speed',store.maxpwm)
    motors.driveMotors(store.maxpwm,0)
    await asyncio.sleep_ms(3000) 
    motors.stopMotors()
    print(' stop motors')



    # Right Motor
    print(' drive right motor : minimum forward speed',store.minPwmRight)
    motors.driveMotors(0,store.minPwmRight)
    await asyncio.sleep_ms(3000) 
    print(' drive right motor : maximum forward speed',store.maxpwm)
    motors.driveMotors(0,store.maxpwm)
    await asyncio.sleep_ms(3000) 
    motors.stopMotors()
    print(' stop motors')
  
    print(' disarm motors')
    motors.disarmMotors()
    print(' disarm motors done')