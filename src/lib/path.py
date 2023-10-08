'''
    follows a path of waypoints
    holds the current station (position)
'''
import uasyncio as asyncio
from lib import server
from lib.utils import distance, bearing
from lib.imu import IMU
from lib.gps import GPS
from lib.store import Store

store = Store()
imu = IMU()
gps = GPS()

def startFollowPathTask():
    followPath = asyncio.create_task( followPathTask() )
    server.addListener('stopFollowPathTask', followPath.cancel) 

server.addListener('startFollowPathTask', startFollowPathTask)     

async def followPathTask():
    try: 
        print('starting followPathTask')
        while True:
                
            await gps.positionAvailable.wait()
            
            # go to the next waypoint 
            if len(store.waypoints) > 0:
                store.destination = store.waypoints[0]


            # course and distance to the next waypoint
            store.distance = distance(store.position,store.destination)
            store.desiredcourse = bearing(store.position,store.destination)

            # back off on the thruster surge speed as we approach the waypoint
            store.surge = min(store.vmax, 0.5 * store.distance * store.distance)

            # proceed to the next waypoint apon destination arrival
            if len(store.waypoints) > 1 and store.distance < store.waypointarrivedradius:
                print(' ... arrived waypoint',store.destination)
                store.waypoints.pop(0)
                
                #TODO notify RoboBuoyApp that the waypoins have changed

    except asyncio.CancelledError:
        print( "stopping followPathTask" )



def startHoldStationTask():
    holdStation = asyncio.create_task( holdStationTask() )
    server.addListener('stoptHoldStationTask', holdStation.cancel) 

server.addListener('startHoldStationTask', startHoldStationTask)  

async def holdStationTask():
    try: 
        print('starting holdStationTask')

        await gps.positionAvailable.wait()

        # set the hold position
        store.destination = store.position

        while True:
    
            # course and distance to the next waypoint
            store.distance = distance(store.position,store.destination)
            store.desiredcourse = bearing(store.position,store.destination)

            # back off on the thruster surge speed as we approach the waypoint
            store.surge = min(store.vmax, 0.5 * store.distance * store.distance)

            await gps.positionAvailable.wait()

    except asyncio.CancelledError:
        print( "stopping holdStationTask" )

            

