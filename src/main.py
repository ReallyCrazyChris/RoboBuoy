import uasyncio as asyncio
from machine import UART

from lib.i2c import i2c # I2C Communication with IMU
from lib.imu import IMU
from lib.bleuart import BLEUART

from lib.gpsparse import GPS
from lib.controller import Controller
from lib.server import Server

#Initilize 
imu = IMU( i2c )        
imu.calibrateGyro()
#imu.calibrateAccel()

server = Server()
bleuart = BLEUART()
bleuartLock = asyncio.Lock()


#Hardware serial port 2 for GPS sentences
#gpsuart = UART(2, baudrate=9600, bits=8, parity=None, stop=1, tx=5, rx=13, rts=-1, cts=-1, txbuf=256, rxbuf=256, timeout=0, timeout_char=2)
#gps = GPS()

controller = Controller()

async def fuseGps():
    try:
        print('fuseGps started')
        while True:
            
            await asyncio.sleep_ms(1000)  
            
            #read the gps sentense for the uart
            gpssentence = gpsuart.readline()

            if gpssentence == None:
                continue

            #parse the gps sentence    
            gps.parsesentence( gpssentence )

            if gps.positionvalid == False:
                continue

            #the course is valid if the robot is moving
            if gps.speed < 1.5:
                continue
   
            steeringPID.fusegps( gps.course )
        
    except asyncio.CancelledError:
        print( "fuseGps Stopped" )



async def fuseCompass():
    try:
        print('fuseCompass started')
        while True:

            # read magnetic compass heading
            compasscourse = imu.readMagHeading()
            steeringPID.fusecompass(compasscourse)
            await asyncio.sleep_ms(500)  
    
    except asyncio.CancelledError:
        print( "fuseCompass Stopped" )


async def steerCourse():
    try:
        
        print('steerCourse started')
        while True:

            _,_,gyro_z,deltaT = imu.readCalibractedGyro()
            controller.fusegyro(gyro_z,deltaT)
            controller.pidloop( deltaT )
            controller.drive()

            #print(steeringPID.desiredcourse, steeringPID.currentcourse, steeringPID.steer)

            await asyncio.sleep_ms(200)  
    except asyncio.CancelledError:
        controller.stop()
        print( "steerCourse Stopped" )

async def receive_message():
    ''' receives messages via bluetooth '''
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
    ''' sends messages via bluetooth '''
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


async def main_task():

    await controller.armmotors()

    # Start the Tasks
    steerCourse_Task = asyncio.create_task( steerCourse() )
    #fuseCompass_Task = asyncio.create_task( fuseCompass() )
    #fuseGps_Task     = asyncio.create_task( fuseGps() )
    receive_message_Task = asyncio.create_task( receive_message() )
    send_message_Task = asyncio.create_task( send_message() )
    await asyncio.sleep(100000)  # Pause 1s    
    # Stop the Tasks
    #fuseGps_Task.cancel()
    #fuseCompass_Task.cancel()
    steerCourse_Task.cancel()
    receive_message_Task.cancel()
    send_message_Task.cancel()
    
        
if __name__ == "__main__": 
    print('robobuoy v0.1')
    asyncio.run( main_task() )
 