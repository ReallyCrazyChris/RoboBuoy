##################################################### 
# Tasks and Actions that update the RoboBuoyAPP State
#####################################################
import uasyncio as asyncio
from lib import server
from lib.storemessages import motionmessage, waypointmessage    

def sendWaypointMessage():
    ''' send updated waypoints to the RoboBouyApp '''
    server.send('state',waypointmessage())

def sendMotionMessage():
    ''' send updated motion informaiton to the RoboBouyApp '''
    server.send('state',motionmessage())

async def sendMotionMessageTask():
    ''' continously sends the motion informaiton to the RoboBouyApp '''
    try:
        print('starting sendMotionMessageTask')
        while True:
            await asyncio.sleep_ms(1000)  
            sendMotionMessage()
    except asyncio.CancelledError:
        print( "stopping sendMotionMessageTask")