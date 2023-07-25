import uasyncio as asyncio
from machine import UART

from drivers.i2c import i2c # I2C Communication with IMU, Compass and Thrusters
from drivers.imu import IMU
from drivers.bleuart import BLEUART # Bluetooth Low Energy UART for command and control

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
gps = GPS()

autopilot = AutoPilot( i2c )
#autopilot.armmotors()

async def read_gps_task():
    ''' reads gps sentence  '''
    try:
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

            if gps.waypoints[0] == None:
                continue

            autopilot.desiredcourse = gps.bearing(gps.position,gps.waypoints[0])
            autopilot.distance = gps.distance(gps.position,gps.waypoints[0])
            autopilot.surge = min(100,autopilot.distance * 20)


            # if the senthense is valid
            if gps.positionvalid :
                #print("timestamp", gps.timestamp )
                print("long", gps.position )
                print("speed", gps.speed )
                print("course", gps.course ) 
                print("desiredcourse", autopilot.desiredcourse ) 
                print("distance", autopilot.distance ) 
                print("surge", autopilot.surge ) 
                print("currentcourse",  autopilot.currentcourse )
                print("steer",  autopilot.steer )
             
    except asyncio.CancelledError:
        print( "read_gps_task stopped" )




async def maintainCourse():
    ''' reads compass and gyro data and estimates new heading using a complementary filter'''

    try:
        while True:

            # read gyro angualr velocities in deg_s and the time between readings deltaT
            gx,gy,gz,deltaT = imu.readCalibractedGyro()

            gyro_angle_deg = autopilot.integrate_gyro(gz,deltaT)

            desiredCourse = 0

            steering_angle = autopilot.steering_pid( desiredCourse, gyro_angle_deg, deltaT )

            print(desiredCourse, gyro_angle_deg,steering_angle)

            await asyncio.sleep_ms(50)  
    except asyncio.CancelledError:
        print( "maintainCourse_stopped" )
    













async def _maintainCourse():
    ''' reads compass and gyro data and estimates new heading using a complementary filter'''

    try:
        while True:

            # read gyro angualr velocities in deg_s and the time between readings deltaT
            gx,gy,gz,deltaT = imu.readCalibractedGyro()

            # read magnetic compass heading
            magcourse = imu.readMagHeading()
      
            # if the gps sentence is valid and the robot is moving include gps course in the fusion
            if gps.positionvalid and gps.speed > 1:                
                autopilot.fusecourse(gps.course, magcourse, gz, deltaT)
            else:
                autopilot.fusecourse(None, magcourse, gz, deltaT)

            # course pid loop
            if autopilot.autopilot:
                autopilot.motorsactive = True
                autopilot.course_pid( deltaT )
                print(autopilot.desiredcourse, autopilot.currentcourse,  autopilot.steer )
                autopilot.drive(autopilot.steer,autopilot.surge)
            else:
                autopilot.desiredcourse = autopilot.currentcourse #just go strait
                
            await asyncio.sleep_ms(50)  

    except asyncio.CancelledError:
        print( "maintainCourse_stopped" )
        autopilot.stopmotors()


async def receive_message ():
    ''' receives motor control actions via bluetooth '''
    try:
        while True:
            if bleuart.message != None:
                
                if "pause" == bleuart.message:
                    autopilot.motorsactive= not autopilot.motorsactive

            # clear processed message          
            bleuart.message = None
            await bleuart.received_event.wait()

    # when the task is cancelled stop motors
    except asyncio.CancelledError:
       pass 


         
async def main_task():
    ''' waits for ble connections and starts or stops related tasks'''
    while True:

        # wait for a connection
        #print('waiting for a ble client to connect...')
        #await bleuart.connect_event.wait()
        #print('connected to ble client')               
        #await bleuart.exchange_mtu_event.wait()
        #print('mtu esablished')
        #await asyncio.sleep(1) 
        
        # Start the Tasks
        read_gps_Task = asyncio.create_task( read_gps_task() ) 
        maintainCourse_Task = asyncio.create_task( maintainCourse() )
        #receive_message_Task = asyncio.create_task( receive_message() ) 
    
        # wait for a bluetooth disconnect
        await bleuart.disconnect_event.wait()
        print('disconnected')

        # Stop the Tasks
        maintainCourse_Task.cancel()
        receive_message_Task.cancel()
        read_gps_Task.cancel()
        

    

if __name__ == "__main__":
    print('robobuoy v0.1')
    asyncio.run( main_task() )

"""
async def send_gpsdata_ble_task():
    ''' reads gps sentences and send this via bluetooth '''
    while True:
        gpssentence = gpsuart.readline()
        if gpssentence != None:
            await bleuart.lock.acquire()
            await bleuart.notify( gpssentence )
            bleuart.lock.release()
        await asyncio.sleep_ms(0)  
"""       


#from wifimgr import WifiManager
import utime

#wm = WifiManager()
#wm.connect()

#while True:
#    if wm.is_connected():
#        print('Connected!')
#        break
#    else:
#        print('Disconnected!')
#    utime.sleep(10)

import machine
from ubinascii import hexlify
from mqtt import MQTTClient

#import json
import hx711

# ssid and password of your wifi router
wifi_ssid="ft2"
wifi_password="CFTyC96229"

# host,port,username and password of the mqtt broker
mqtt_hostname='cbb90cade46d4ff38fdf18a5dc12c4be.s2.eu.hivemq.cloud'
mqtt_port=8883 
mqtt_user="test1"
mqtt_password="TestPass"
mqtt_client_id = hexlify(machine.unique_id())

def connect_to_wifi(ssid=None, password=''):
    ''' connect to the wifi router'''
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to wifi network...')
        sta_if.active(True)
        # Please use your own Wifi Routers Credentials !!
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    
    print('successfull connection to ',ssid)
    print('network config:', sta_if.ifconfig())


def puback_cb(msg_id):
  print('PUBACK ID = %r' % msg_id)

def suback_cb(msg_id, qos):
  print('SUBACK ID = %r, Accepted QOS = %r' % (msg_id, qos))
  
def con_cb(connected):
  if connected:
    client.subscribe('subscribe/topic')

def msg_cb(topic, pay):
  print('Received %s: %s' % (topic.decode("utf-8"), pay.decode("utf-8")))


connect_to_wifi(wifi_ssid, wifi_password)  

# load the private key for TLS aka mqtts
with open('key.der','rb') as f:
    key = f.read()
# load the certificate for TLS aka mqtts
with open('cert.der','rb') as f:
    cert = f.read()

ssl_params={
    "key": key, 
    "cert": cert, 
    "server_hostname":mqtt_hostname
}    
  
client = MQTTClient(mqtt_hostname, port=mqtt_port, reconnect_retry_time=10, keep_alive=0 ,ssl=True, ssl_params=ssl_params )

client.set_connected_callback(con_cb)
client.set_puback_callback(puback_cb)
client.set_suback_callback(suback_cb)
client.set_message_callback(msg_cb)

client.connect(mqtt_client_id, user=mqtt_user, password=mqtt_password, clean_session=True, will_topic=None, will_qos=0, will_retain=False, will_payload=None)

weight = 0
while True:
  if client.isconnected():
    try:
      measurement = hx711.weight()
      if measurement != None and weight != measurement:
            weight = measurement        
            print("publish scale/value " + str(weight))
            pub_id = client.publish('scale/value', str(weight), False)

    except Exception as e:
      print(e)

    utime.sleep_ms(300)
    
  else:
    utime.sleep(2)
   

