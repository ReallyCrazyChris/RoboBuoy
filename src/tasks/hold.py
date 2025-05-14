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
  
        # assume that we hold the current station     
        store.destination = store.position

        while True:
            #  hold station


            distance, desiredcourse, dx_meters, dy_meters = distanceBearing(store.position,store.destination)
         
            store.distance = distance
          

            # Reduce the surge as the RoboBouy approached the waypoint
            store.surge = min(store.vmax, store.distance**2 / store.waypointarrivedradius**2 )

            # Reduce the desired course gitter with a complementary filter

            store.desiredcourse =  (1.0 - store.holdgain) * store.desiredcourse + desiredcourse * store.holdgain 



            print(f"Hold: Distance: {store.distance:.2f}m, Applying thrust: surge={store.surge:.2f}, desiredcourse={store.desiredcourse:.2f}  dx={dx_meters:.2f}, dy={dy_meters:.2f} ")


            await gps.positionAvailable.wait() 

    except asyncio.CancelledError:
        print( "stopping holdTask" )