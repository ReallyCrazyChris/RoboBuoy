'''
    Autonomously
    follows a path of waypoints or
    holds the current station (position)
'''
import uasyncio as asyncio
from lib import server
from lib.utils import distancebearing, convert_dd_int
from lib.imu import IMU
from lib.gps import GPS
from lib.store import Store

store = Store()
imu = IMU()
gps = GPS()

async def autoTask():
    try: 
        print('starting autoTask')

        await gps.positionAvailable.wait()

        # set the hold position
        store.destination = store.position

        while True:
                
            # go to the next waypoint 
            if len(store.waypoints) > 0:
  
                store.destination = store.position

            # course and distance to the next waypoint
            store.distance, store.desiredcourse = distancebearing(store.position,store.destination)
            print('distance,bearing',store.distance, store.desiredcourse)
            # back off on the thruster surge speed as we approach the waypoint
            store.surge = min(store.vmax, 0.5 * store.distance * store.distance)

            # proceed to the next waypoint apon destination arrival
            if len(store.waypoints) and store.distance < store.waypointarrivedradius:
                print(' ... arrived waypoint',store.destination)
                store.waypoints.pop(0)

                if len(store.waypoints) == 0:
                    # set the hold position
                    store.destination = store.position
                
                store.sendWaypointsUpdate()

            await gps.positionAvailable.wait()

    except asyncio.CancelledError:
        print( "stopping autoTask" )

           

