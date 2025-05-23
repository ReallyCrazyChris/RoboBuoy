import utime
import uasyncio as asyncio

from storage.store import Store

store = Store.instance()

async def holdTask():
    '''
    Holds the current station (position)
    '''

    from lib.utils import distanceBearing
    from driver.gps import GPS 
    gps = GPS()


    try: 
        print('starting holdTask')

        # wait for a GPS position to be available
        await gps.positionAvailable.wait()
  
        # whe hold the current position    
        store.destination = store.position

        while True:
            
            store.distance, store.course, dx_meters, dy_meters = distanceBearing(store.position,store.destination)
            
            # reduce the surge exponentially as we enter the hold station radius
            store.surge = store.vmax * min(1,(store.distance/store.holdradius)**2)

            print(f"Hold-Station: Distance: {store.distance:.2f}m, Course: {store.course:.2f} rad, surge={store.surge:.2f}, ")                           

            await gps.positionAvailable.wait() 

    except asyncio.CancelledError:
        print( "stopping holdTask" )