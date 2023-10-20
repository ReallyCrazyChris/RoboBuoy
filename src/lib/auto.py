'''
    Autonomously
    follows a path of waypoints or
    holds the current station (position)
'''
import uasyncio as asyncio
from lib import server
from lib.utils import distancebearing
from lib.imu import IMU
from lib.gps import GPS
from lib.store import Store

store = Store()
imu = IMU()
gps = GPS()

async def autoTask():
    try: 
        print('starting autoTask')

        #await gps.positionAvailable.wait()
  
        # assume tht we hold station first    
        store.destination = store.position

        while True:
            if(len(store.waypoints)): #follow the waypoints
                store.destination = store.waypoints[0]
                store.distance, store.desiredcourse = distancebearing(store.position,store.destination)
                store.surge = store.vmax
                print('auto: distance, bearing, surge, waypoints',store.distance, store.desiredcourse, store.surge, len(store.waypoints))

                if len(store.waypoints) > 0 and store.distance < store.waypointarrivedradius:
                    print(' ... arrived waypoint',store.destination)
                    store.waypoints.pop(0)
                    store.sendWaypointsUpdate()
            
            else: # hold station
                store.distance, store.desiredcourse = distancebearing(store.position,store.destination)
                store.surge = min(store.vmax, 0.5 * store.distance * store.distance)
                print('hold: distance, bearing, surge, waypoints',store.distance, store.desiredcourse, store.surge, len(store.waypoints))
                
            #await gps.positionAvailable.wait()
            await asyncio.sleep(2)
                    
    except asyncio.CancelledError:
        print( "stopping autoTask" )
