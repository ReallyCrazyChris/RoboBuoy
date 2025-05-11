import uasyncio as asyncio
from driver.gps import GPS
from storage.store import Store
gps = GPS()
store = Store.instance()

async def fuseGpsTask():
    '''fuses the gps course with the currentcourse '''
    try:
        print('starting fuseGpsTask')
        while True:
            
            await gps.courseAvailable.wait()
       
            # Fuse the GPS course with the current course using a complementary filter
            # This is only done if the GPS course is valid and the GPS speed is greater than 1 m/s
            if store.gpsalpha > 0 and store.gpsspeed >= 1:         
                store.currentcourse =  (1.0 - store.gpsalpha) * store.currentcourse + store.gpscourse * store.gpsalpha 


            # Fuse the Magnetic Declination with the GPS Declination using a complementary filter
            # This is only done if the Robot is moving (distance to go to waypoint > 10 m)
            if store.declinationalpha > 0 and store.distance > 10:  #and store.gpsspeed >= 1 
                store.magdeclination =  (1.0 - store.declinationalpha) * store.magdeclination + ( store.declinationalpha * (store.gpscourse - store.magcourse)  )
   

    except asyncio.CancelledError:
        print( "stopping fuseGpsTask" )    