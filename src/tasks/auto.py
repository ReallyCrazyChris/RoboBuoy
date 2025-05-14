'''
    Autonomously follows a path of waypoints or
    holds the current station (position) when no waypoints are set.
'''
import uasyncio as asyncio
from lib.utils import distanceBearing
from driver.gps import GPS
from transport import server
from transport.storemessages import  waypointmessage    
from storage.store import Store

store = Store.instance()
gps = GPS()

async def autoTask():
    ''' 
    Automatically follows a waypoints
    '''
    try: 
        print('starting autoTask')

        await gps.positionAvailable.wait()
  
        # assume tht we hold station first    
        store.destination = store.position

        while True:
            # follow the waypoints by being underway
            if(len(store.waypoints) > 0): 
                store.destination = store.waypoints[0]
                store.distance, store.desiredcourse = distanceBearing(store.position,store.destination)
                store.surge = store.vmax
                print('auto: distance, bearing, surge, waypoints',store.distance, store.desiredcourse, store.surge, len(store.waypoints))

                if len(store.waypoints) > 0 and store.distance < store.waypointarrivedradius:
                    print(' ... arrived waypoint',store.destination)
                    store.waypoints.pop(0)
                    # send updated waypoints to the RoboBouyApp
                    server.send('state',waypointmessage())
            
            else: # when there are no more waypoint to follow : hold station
                store.distance, store.desiredcourse = distanceBearing(store.position,store.destination)
                store.surge = min(store.vmax, store.holdgain * store.distance * store.distance)
                
              

                
                print('auto-hold: distance, bearing, surge, waypoints',store.distance, store.desiredcourse, store.surge, len(store.waypoints))
                
            await gps.positionAvailable.wait()
                    
    except asyncio.CancelledError:
        print( "stopping autoTask" )


