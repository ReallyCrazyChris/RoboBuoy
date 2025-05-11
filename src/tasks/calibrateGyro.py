import uasyncio as asyncio
from driver.imu import IMU
from storage.store import Store

store = Store.instance() #singleton reference
imu = IMU()

async def calibrateGyroTask( samples:int=100, delay:int=10 ) -> tuple:
    ''' creates gyro averaged values for biasing the gyro at rest '''        
    try:
        print('starting calibrateGyroTask')        
        ox, oy, oz = 0.0, 0.0, 0.0
        samples = int(samples) 
        delay = int(delay) 
        n = int(samples)

        while samples:
            await asyncio.sleep_ms(delay)
            gx, gy, gz = imu.readGyro()
            ox += gx
            oy += gy
            oz += gz
            samples -= 1

        # mean gyro values
        ox,oy,oz = ox / n, oy / n, oz / n

        # update the gyro bias
        store.gyrobias = (ox,oy,oz)

        return ox,oy,oz  
    
    except asyncio.CancelledError:
        print( "stopping calibrateGyroTask" ) 