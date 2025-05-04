import uasyncio as asyncio
from lib.store import Store
from lib.utils import normalize, constrain
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

            gyroAdjustedCourse = ( store.currentcourse + gyro_z * deltaT )

            store.currentcourse = normalize(gyroAdjustedCourse,-180,180) # clamp to -180 ... 180 degrees TODO use a mutator ?
            
            

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
                    # read magnetic compass heading
                    compassAdjustedCourse = (1.0 - store.magalpha) * store.currentcourse + store.magalpha * (store.magcourse )
                    #print('compassAdjustedCourse',compassAdjustedCourse)
                    store.currentcourse = normalize(compassAdjustedCourse,-180,180) # clamp to -180 ... 180 degrees

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
       
            # update the currentcourse based on the latest gps cource
            if store.gpsalpha > 0 and store.gpsspeed >= 1:# must be moving for the gpscourse to be valid           
                # Complementary filter strongly weighted towards the gps
                gpsAdjustedCourse = (1.0 - store.gpsalpha) * store.currentcourse + store.gpsalpha * store.gpscourse
                store.currentcourse = normalize(gpsAdjustedCourse,-180,180) # clamp to -180 ... 180 degrees


            # update the compass declination based on the latest gps course
            if store.declinationalpha > 0 and store.distance > 10:  #and store.gpsspeed >= 1
                # Complementary filter strongly weighted towards the magdeclination
                declination =  (1.0 - store.declinationalpha) * store.magdeclination + ( store.declinationalpha * (store.gpscourse - store.magcourse)  )
                store.magdeclination = normalize(declination,-180,180)

    except asyncio.CancelledError:
        print( "stopping fuseGpsTask" )       
