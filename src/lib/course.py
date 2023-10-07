
import uasyncio as asyncio
from lib.server import Server

server = Server()

class Course(object):
    '''
        provides tasks to calculate a relaible course
    '''

    def __init__( self ): 
        server.addListener('FGT', self.startFuseGyroTask) 

    def startFuseGyroTask(self):
        fuseGyro = asyncio.create_task( self.fuseGyroTask() )
        server.addListener('sFGT', fuseGyro.cancel)

    async def fuseGyroTask():
        try: 
            print('starting fuseGyroTask')
            while True:

                _,_,gyro_z,deltaT = imu.readCalibractedGyro()
                controller.fusegyro(gyro_z,deltaT)
                controller.pidloop( deltaT )
                controller.drive()

                await asyncio.sleep_ms(200)  
        except asyncio.CancelledError:
            controller.stop()
            print( "stopping fuseGyroTask" )



              



        
    async def fuseGpsTask():
        try:
            print('fuseGps Task started')
            while True:
                
                await asyncio.sleep_ms(20)  
                
                #read the gps sentense for the uart
                gpssentence = gpsuart.readline()
        
                if gpssentence == None:
                    continue
                #print(gpssentence)

                #parse the gps sentence    
                gps.parsesentence( gpssentence )

                controller.positionvalid = gps.positionvalid

                if gps.positionvalid == False:
                    continue

                controller.latitude = gps.latitude # degree decimal north
                controller.longitude = gps.longitude # degree decimal east
                controller.latitude_string = gps.latitude_string # degree decimal north 24 bit precision, 
                controller.longitude_string = gps.longitude_string # degree decimal east 24 bit precision
                controller.speed = gps.speed  #meters per second
                controller.currentposition = gps.position 

                #the course is valid if the robot is moving
                if gps.speed < 1:
                    continue
    
                controller.fusegps( gps.course )
            
        except asyncio.CancelledError:
            print( "fuseGpsTask Stopped" )

    def startFuseGpsTask():
        fuseGps = asyncio.create_task( fuseGpsTask() )
        server.addListener('sGT', fuseGps.cancel)

    server.addListener('GT', startFuseGpsTask) 

    async def fuseCompassTask():
        try:
            print('fuseCompassTask started')
            while True:

                # read magnetic compass heading
                compasscourse = imu.readMagHeading()
                controller.fusecompass(compasscourse)
                await asyncio.sleep_ms(100)  
        
        except asyncio.CancelledError:
            print( "fuseCompassTask Stopped" )

    def startFuseCompassTask():
        fuseCompass = asyncio.create_task( fuseCompassTask() )
        server.addListener('sFCT', fuseCompass.cancel)

    server.addListener('FCT', startFuseCompassTask)        
