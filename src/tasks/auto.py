import uasyncio as asyncio
from lib.utils import distanceBearing
from driver.gps import GPS
from transport import server
from transport.storemessages import  waypointmessage    
from storage.store import Store
store = Store.instance()
gps = GPS()
async def autoTask():
    try: 
        print('starting autoTask')
        await gps.positionAvailable.wait() 
        store.destination = store.position
        while True:
            if(len(store.waypoints) > 0): 
                store.destination = store.waypoints[0] 
                store.distance, store.course, dx,dy = distanceBearing(store.position,store.destination)         
                store.surge = store.vmax
                print(f"Auto: Distance: {store.distance:.2f}m, Course: {store.course:.2f} rad, surge={store.surge:.2f}, ")
                if len(store.waypoints) > 0 and store.distance < store.waypointarrivedradius:
                    print(' ... arrived waypoint',store.destination)
                    store.waypoints.pop(0)
                    server.send('state',waypointmessage())  
            else: 
                store.distance, store.course, dx_meters, dy_meters = distanceBearing(store.position,store.destination)  
                store.surge = store.vmax * min(1,(store.distance/store.holdradius)**2)
                print(f"Auto-Hold-Station: Distance: {store.distance:.2f}m, Course: {store.course:.2f} rad, surge={store.surge:.2f}, ")                          
            await gps.positionAvailable.wait()             
    except asyncio.CancelledError:
        print( "stopping autoTask" )


