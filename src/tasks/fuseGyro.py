import uasyncio as asyncio
from driver.imu import IMU
from storage.store import Store
imu = IMU()
store = Store.instance()


async def fuseGyroTask():
    ''' 
    fuses the integrated gyro course with the currentcourse 
    performs the steering ang pid loop
    '''
    try: 
        print('starting fuseGyroTask')
        while True:

            # Integrate the gyro, update the current course
            _,_,gyro_z,deltaT = imu.readCalibratedGyro()

            store.currentcourse =  store.currentcourse + gyro_z * deltaT 

            #print a table of the current course, gyro course and deltaT
            #print("currentcourse: %5.2f gyro_z: %5.2f deltaT: %5.2f" % (store.currentcourse, gyro_z, deltaT))


            await asyncio.sleep_ms(20)  
    except asyncio.CancelledError:
        print( "stopping fuseGyroTask" )