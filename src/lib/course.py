import uasyncio as asyncio
from lib.store import Store
from lib.utils import normalize
from lib.imu import IMU, MagDataNotReady
from lib.gps import GPS

imu = IMU()
gps = GPS()
store = Store.instance()

########################
# Fuse Gyro Task
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
            store.currentcourse = normalize( store.currentcourse + gyro_z * deltaT )

            #print a table of the current course, gyro course and deltaT
            #print("currentcourse: %5.2f gyro_z: %5.2f deltaT: %5.2f" % (store.currentcourse, gyro_z, deltaT))


            await asyncio.sleep_ms(20)  
    except asyncio.CancelledError:
        print( "stopping fuseGyroTask" )

########################
# Fuse Compass Task

async def fuseCompassTask():
    '''fuses the compass course with the currentcourse using a complement filter, strongly weighted towards the current course'''
    try:
        print('starting fuseCompassTask')
        while True:
            try:
                await asyncio.sleep_ms(100)
                store.magcourse = imu.readMagHeading() + store.magdeclination
                
                if store.magalpha > 0:
                    # Apply a complementary filter to fuse the compass course with the current course
                    store.currentcourse = (1.0 - store.magalpha) * store.currentcourse +  store.magcourse * store.magalpha 

            except MagDataNotReady:
                # TODO, magnetometer is a resource that needs to be managed by a lock
                pass    
           
    except asyncio.CancelledError:
        print( "stopping fuseCompassTask" )

########################
# Fuse GPS Task
async def fuseGpsTask():
    '''fuses the gps course with the currentcourse '''
    try:
        print('starting fuseGpsTask')
        while True:
            
            await gps.courseAvailable.wait()
       
            # Fuse the GPS course with the current course using a complementary filter
            # This is only done if the GPS course is valid and the GPS speed is greater than 1 m/s
            if store.gpsalpha > 0 and store.gpsspeed >= 1:         
                store.currentcourse =  (1.0 - store.gpsalpha) * store.currentcourse + store.gpscourse * store.gpsalpha 


            # Fuse the Magnetic Declination with the GPS Declination using a complementary filter
            # This is only done if the Robot is moving (distance to go to waypoint > 10 m)
            if store.declinationalpha > 0 and store.distance > 10:  #and store.gpsspeed >= 1 
                store.magdeclination =  (1.0 - store.declinationalpha) * store.magdeclination + ( store.declinationalpha * (store.gpscourse - store.magcourse)  )
   

    except asyncio.CancelledError:
        print( "stopping fuseGpsTask" )       
