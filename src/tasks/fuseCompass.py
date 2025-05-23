import uasyncio as asyncio
from driver.imu import IMU, MagDataNotReady
from storage.store import Store
imu = IMU()
store = Store.instance()

async def fuseCompassTask():
    '''fuses the compass course with the heading using a complement filter, strongly weighted towards the current course'''
    try:
        print('starting fuseCompassTask')
        while True:
            try:
                await asyncio.sleep_ms(100)

                store.magheading = imu.readMagHeading()
                
                if store.magalpha > 0:
                    # Apply a complementary filter to fuse the compass course with the current course
                    store.heading =   (store.magheading + store.magdeclination) * store.magalpha  + (1.0 - store.magalpha) * store.heading

            except MagDataNotReady:
                # TODO, magnetometer is a resource that needs to be managed by a lock
                pass    
           
    except asyncio.CancelledError:
        print( "stopping fuseCompassTask" )