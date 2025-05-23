import uasyncio as asyncio
from driver.imu import IMU
from storage.store import Store
imu = IMU()
store = Store.instance()


async def fuseGyroTask():
    ''' 
    fuses the integrated gyro course with the heading 
    performs the steering ang pid loop
    '''
    try: 
        print('starting fuseGyroTask')
        while True:

            # Integrate the gyro, update the current course
            _,_,gyro_z,deltaT = imu.readCalibratedGyro()

            # integrate the course with the gyro_z
            # use a complementary filter to set the level of trust in the gyro
            store.heading = store.gyroalpha * (store.heading + gyro_z * deltaT ) + (1 - store.gyroalpha) * store.heading

            #print a table of the current course, gyro course and deltaT
            #print("heading: %5.2f gyro_z: %5.2f deltaT: %5.2f" % (store.heading, gyro_z, deltaT))

            await asyncio.sleep_ms(20)  
    except asyncio.CancelledError:
        print( "stopping fuseGyroTask" )