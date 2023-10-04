import uasyncio as asyncio
from machine import UART

from lib.i2c import i2c # I2C Communication with IMU
from lib.imu import IMU
from lib.bleuart import BLEUART

from lib.gpsparse import GPS
from lib.controller import Controller
from lib.server import Server

#Initilize IMU
imu = IMU( i2c )        
#imu.calibrateGyro()
#imu.calibrateAccel()


server = Server() # Server Singleton
#External Commands
server.addListener('calibrateMag',imu.calibrateMag)


bleuart = BLEUART()
# async lock to prevent multiple communication actions at the same time
bleuartLock = asyncio.Lock()


#Hardware serial port 2 for GPS sentences
gpsuart = UART(2, baudrate=9600, bits=8, parity=None, stop=1, tx=5, rx=13, rts=-1, cts=-1, txbuf=256, rxbuf=256, timeout=0, timeout_char=2)
#gpsuart = UART(2, baudrate=9600, bits=8, parity=None, stop=1, tx=12, rx=34, rts=-1, cts=-1, txbuf=256, rxbuf=256, timeout=0, timeout_char=2)
gps = GPS()

controller = Controller()

async def followpathTask():
    try:
        print('followpath Task started')
        while True:
            await asyncio.sleep_ms(1000)
            controller.followpath()  

    except asyncio.CancelledError:
        print( "followpath Stopped" )

def startFollowpathTask():
    followPath = asyncio.create_task( followpathTask() )
    server.addListener('sFP', followPath.cancel)

server.addListener('FP', startFollowpathTask)         

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

def startFuseGyroTask():
    fuseGyro = asyncio.create_task( fuseGyroTask() )
    server.addListener('sFGT', fuseGyro.cancel)

server.addListener('FGT', startFuseGyroTask)           


async def sendMotionStateTask():
    ''' sends a message to the client containg the motion parameters '''
    try:
        print('sendMotionStateTask started')
        while True:
            controller.sendmotionstate()
            await asyncio.sleep_ms(500)  
    except asyncio.CancelledError:
        print( "sendMotionStateTask Stopped" )

def startSendMotionStateTask():
    motionStateTask = asyncio.create_task( sendMotionStateTask() )
    server.addListener('sSMT', motionStateTask.cancel)

server.addListener('SMT', startSendMotionStateTask)        


async def receive_message():
    ''' receives messages via bluetooth and adds them to the receive queue '''
    print('starting server receive Task')
    try:
        while True:
            if bleuart.message != None:
                server.receive( bleuart.message )
                server.react() #TODO this may need its own async co-routine
            # clear processed message          
            bleuart.message = None
            await bleuart.received_event.wait()
    except asyncio.CancelledError:
       pass 

async def send_message():
    ''' reads messages from the server send queue and sends them via bluetooth '''
    print('starting server send Task')
    try:
        # after connection try sending
        await bleuart.connect_event.wait()

        while True:    
            if len(server.sendqueue) > 0:
                for packet in server.sendqueue:
                    await bleuart.lock.acquire()
                    await bleuart.notify( packet )
                    bleuart.lock.release()
                # clear processed message
                server.sendqueue.clear() 
            else:
                await asyncio.sleep_ms(200)          

    except asyncio.CancelledError:
       pass     


async def bluetooth_advertise():
    ''' sends robobouy advertisement via via bluetooth every 2 seconds'''
    ''' allows auto reconnect'''
    print('starting Bluetooth advertise Task')
    try:
        while True:    
            await asyncio.sleep_ms(2000) 
            await bleuart.lock.acquire()
            bleuart.advertise()
            bleuart.lock.release()
    except asyncio.CancelledError:
       pass    


async def mainTaskLoop():

    await controller.armmotors()

    # Start the Tasks that must always run
    asyncio.create_task( receive_message() )
    asyncio.create_task( send_message() )
    asyncio.create_task( bluetooth_advertise() )

    #Start Tasks than can be stopped, and started
    #startFuseCompassTask()
    #startFuseGyroTask()
    startFuseGpsTask()
    startFollowpathTask()

    # Keep the mainTaskLoop running forever    
    while 1:
        await asyncio.sleep(100000)  # Pause 1s    
  
    
        
if __name__ == "__main__": 
    print('robobuoy v0.1')
    asyncio.run( mainTaskLoop() )
 