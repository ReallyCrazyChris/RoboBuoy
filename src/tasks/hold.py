import uasyncio as asyncio
from lib.utils import distancebearing
from driver.gps import GPS 
from storage.store import Store

store = Store.instance()
gps = GPS()

async def holdTask():
    '''
    Holds the current station (position)
    '''
    try: 
        print('starting holdTask')

        # wait for a GPS position to be available
        await gps.positionAvailable.wait()
  
        # assume that we hold the current station     
        store.destination = store.position

        while True:
            #  hold station
            store.distance, store.desiredcourse = distancebearing(store.position,store.destination)
            # TODO: this will need to be revisited
            store.surge = min(store.vmax, store.holdgain * store.distance * store.distance)

            print("auto-hold: distance: %5.2f desiredcourse: %5.2f surge: %5.2f " % (store.distance, store.desiredcourse, store.surge ))

            # wait for th enext GPS position to be available
            await gps.positionAvailable.wait() 

    except asyncio.CancelledError:
        print( "stopping holdTask" )