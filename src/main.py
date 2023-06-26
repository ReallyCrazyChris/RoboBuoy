import uasyncio as asyncio
from machine import UART

from math import atan2, sin, cos, radians, degrees

from drivers.i2c import i2c
from drivers.imu import IMU
from drivers.bleuart import BLEUART
from drivers.thruster import Thruster

from lib.gps import GPS
from lib.autopilot import AutoPilot


#Initilize 
imu = IMU( i2c )
imu.calibrateGyro()
imu.calibrateAccel()

bleuart = BLEUART('RoboBuoy')
bleuartLock = asyncio.Lock()


#Hardware serial port 2 for GPS sentences
gpsuart = UART(2, baudrate=9600, bits=8, parity=None, stop=1, tx=5, rx=13, rts=-1, cts=-1, txbuf=256, rxbuf=256, timeout=0, timeout_char=2)
gps = GPS(2)

#autopilot = AutoPilot()

thruster = Thruster()

#Tasks
async def steer():
    ''' reads compass and gyro data and estimates new heading using a complementary filter'''
    try:
        while True:

            # read gyro angualr velocities in deg_s and the time between readings deltaT
            gx,gy,gz,deltaT = imu.readCalibractedGyro()
            
            thruster.thetaPID( radians(45), radians(gz), deltaT )

            await asyncio.sleep_ms(50) 
    except asyncio.CancelledError:
        print("steer_task_stopped")
        thruster.active = False
              



async def estimate_heading():
    ''' reads compass and gyro data and estimates new heading using a complementary filter'''

    try:
        while True:

            # read gyro angualr velocities in deg_s and the time between readings deltaT
            gx,gy,gz,deltaT = imu.readCalibractedGyro()

            # read magnetic compass heading
            magHeading = imu.readMagHeading()
      
            # if the gps is valid and the robot is moving use gps course
            if gps.valid and gps.speed > 1:                
                autopilot.fuseHeading(gps.course, magHeading, gz, deltaT)
            else:
                autopilot.fuseHeading(None, magHeading, gz, deltaT)

            # headingPID loop
            autopilot.headingPID( deltaT )

            print(autopilot.currentHeading,  autopilot.rudder)

            mixer(autopilot.rudder,0)

            await asyncio.sleep_ms(50)  

    except asyncio.CancelledError:
        print( "estimate_heading_task_stopped" )
        mixer(0,0)

async def read_gps():
    ''' reads gps sentence  '''
    try:
        while True:

            await asyncio.sleep_ms(100) 

            #read the gps sentense for the uart
            gpssentence = gpsuart.readline()

            if gpssentence == None:
                continue
            #parse the gps sentence    
            gps.parsesentence( gpssentence )

            # if the senthense is valid
            if gps.valid :
                print("timestamp", gps.timestamp )
                print("lat", gps.latitude )
                print("long", gps.longitude )
                print("speed", gps.speed )
                print("course", gps.course ) 
                print("valid", gps.valid ) 
             
    except asyncio.CancelledError:
        print( "read_gps_task_stopped" )

async def send_gpsdata_ble():
    ''' reads gps sentences and send this via bluetooth '''
    while True:
        gpssentence = gpsuart.readline()
        if gpssentence != None:
            await bleuart.lock.acquire()
            await bleuart.notify( gpssentence )
            bleuart.lock.release()
        await asyncio.sleep_ms(0)  

async def receive_message ():
    ''' receives motor control actions via bluetooth '''
    try:
        while True:
            if bleuart.message != None:
                
                if "N" == bleuart.message:
                    #autopilot.desiredBearing = 0
                    pass

                elif "NE" == bleuart.message:
                    #autopilot.desiredBearing = 45
                    pass 

                elif "E" == bleuart.message:
                    #autopilot.desiredBearing = 90
                    pass
                elif "SE" == bleuart.message:
                    #autopilot.desiredBearing = 135
                    pass 
                
                elif "S" == bleuart.message:
                    #autopilot.desiredBearing = 180
                    pass

                elif "SW" == bleuart.message:
                    #autopilot.desiredBearing = 225 
                    pass       

                elif "W" == bleuart.message:
                    #autopilot.desiredBearing = 270
                    pass

                elif "NW" == bleuart.message:
                    #autopilot.desiredBearing = 315
                    pass

                elif "pause" == bleuart.message:
                     thruster.active = not thruster.active               
                else:  
                    thruster.active = False        

                bleuart.message = None
            await bleuart.received_event.wait()

    # when the task is cancelled stop motors
    except asyncio.CancelledError:
       thruster.active = False    


         
async def ble_uart_task():
    ''' waits for ble connections and starts or stops related tasks'''
    while True:

        # wait for a connection
        print('waiting for a ble client to connect...')
        await bleuart.connect_event.wait()
        print('connected to ble client')               
        await bleuart.exchange_mtu_event.wait()
        print('mtu esablished')
        
        #read_gps_Task = asyncio.create_task( read_gps() ) 
        #estimate_heading_Task = asyncio.create_task( estimate_heading() )
        receive_message_Task = asyncio.create_task( receive_message() ) 
        steer_Task = asyncio.create_task( steer() ) 

        # wait for a disconnect
        await bleuart.disconnect_event.wait()
        print('disconnected')
        steer_Task.cancel()
        #estimate_heading_Task.cancel()
        receive_message_Task.cancel()

    

if __name__ == "__main__":
    print('robobuoy')
    asyncio.run( ble_uart_task() )

    