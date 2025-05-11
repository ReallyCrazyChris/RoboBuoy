import uasyncio as asyncio
from lib.utils import translateValue
from driver.motors import driveMotors, stopMotors
from math import pi
from storage.store import Store
store = Store.instance()

async def driveTask():
    '''' drive the motors with the given speed '''
    try:
        print('starting driveMotorsTask')
        while 1:

            # steer is between -pi and pi radians and is translated to -1..1
            # surge is between 0 and 1
            #vl between 0 and 1
            #vr between 0 and 1
            # left and right motor speeds are calculated from surge and steer 

            vl = (store.surge + translateValue(store.steer,-pi,pi,-1,1)) / 2
            vr = (store.surge - translateValue(store.steer,-pi,pi,-1,1)) / 2
            
            driveMotors(vl,vr)

            await asyncio.sleep_ms(20) # TODO Try without this delay 

    except asyncio.CancelledError:  
            stopMotors()
            print( "stopping driveMotorsTask") 