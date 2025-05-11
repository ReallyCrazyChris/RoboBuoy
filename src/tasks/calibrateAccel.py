import uasyncio as asyncio
from driver.imu import IMU
from storage.store import Store

store = Store.instance() #singleton reference
imu = IMU()

async def calibrateAccelTask(samples:int=100,delay:int=10) -> tuple:
    ''' creates accelerometer averaged values for biasing the accelerometer at rest'''
        
    try:
        print('starting calibrateAccelTask')
        
        ox, oy, oz = 0.0, 0.0, 0.0
        samples = int(samples) 
        delay = int(delay) 
        n = int(samples) 

        while samples:
            await asyncio.sleep_ms(delay)
            gx, gy, gz = imu.readAccel()
            ox += gx
            oy += gy
            oz += gz
            samples -= 1

        # mean accel values
        ox,oy,oz = ox / n, oy / n, oz / n
        # update the accel bias
        store.accelbias = (ox,oy,oz)

        print("accel bias",store.accelbias)

        return (ox,oy,oz)

    except asyncio.CancelledError:
        print( "stopping calibrateAccelTask" )  