import uasyncio as asyncio
from lib import server
from lib.store import Store
from lib.utils import normalize, constrain
from lib.imu import IMU
from lib.gps import GPS

imu = IMU()
gps = GPS()
store = Store()

########################
# Fuse Gyro Task
def startFuseGyroTask():
    fuseGyro = asyncio.create_task( fuseGyroTask() )
    server.addListener('stopFuseGyroTask', fuseGyro.cancel) 

server.addListener('startFuseGyroTask', startFuseGyroTask)   

async def fuseGyroTask():
    ''' 
    fuses the integrated gyro course with the currentcourse 
    performs the steering ang pid loop
    '''
    try: 
        print('starting fuseGyroTask')
        while True:

            # Integrate the gyro, update the current course
            _,_,gyro_z,deltaT = imu.readCalibractedGyro()
            currentcourse = ( store.currentcourse + gyro_z * deltaT )
            store.currentcourse = normalize(currentcourse,-180,180) # clamp to -180 ... 180 degrees TODO use a mutator ?

            # steering angle PID controller
            error_1 = store.desiredcourse - store.currentcourse
            error_2 = 360 + error_1
            if abs(error_1) > abs(error_2):
                store.error = error_2
            else:
                store.error = error_1

            #update the integral error
            store.errSum = store.errSum + (store.error * deltaT)
            #update the differential
            store.dErr = (store.error - store.lastErr) / deltaT
                
            store.steer = constrain((store.Kp * store.error) + (store.Ki * store.errSum) + (store.Kd * store.dErr))
            
            store.lastErr = store.error

            await asyncio.sleep_ms(50)  
    except asyncio.CancelledError:
        print( "stopping fuseGyroTask" )

########################
# Fuse Compass Task
def startFuseCompassTask():
    fuseCompass = asyncio.create_task( fuseCompassTask() )
    server.addListener('stopFuseCompassTask', fuseCompass.cancel)   

server.addListener('startFuseCompassTask', startFuseCompassTask) 

async def fuseCompassTask():
    '''fuses the compass course with the currentcourse using a complement filter, strongly weighted towards the current course'''
    try:
        print('starting fuseCompassTask')
        while True:

            # read magnetic compass heading
            compasscourse = imu.readMagHeading()
            currentcourse = (1.0 - store.compassalpha) * compasscourse + store.compassalpha * store.currentcourse
            store.currentcourse = normalize(currentcourse,-180,180) # clamp to -180 ... 180 degrees
            await asyncio.sleep_ms(100)  
    
    except asyncio.CancelledError:
        print( "stopping fuseCompassTask" )

########################
# Fuse GPS Task
def startFuseGpsTask():
    fuseGps = asyncio.create_task( fuseGpsTask() )
    server.addListener('stopFuseGpsTask', fuseGps.cancel) 

server.addListener('startFuseGpsTask', startFuseGpsTask)

async def fuseGpsTask():
    '''fuses the gps course with the currentcourse using a complement filter, strongly weighted towards the gps'''
    try:
        print('starting fuseGpsTask')
        while True:
            
            await gps.courseAvailable.wait()

            if store.gpsspeed >= 1:
                currentcourse = (1.0 - store.gpsalpha) * store.gpscourse + store.gpsalpha * store.currentcourse
                store.currentcourse = normalize(currentcourse,-180,180) # clamp to -180 ... 180 degrees
                    
    except asyncio.CancelledError:
        print( "stopping fuseGpsTask" )       
