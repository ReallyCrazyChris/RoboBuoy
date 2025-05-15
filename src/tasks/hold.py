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

        p = 0
        i = 0
        d = 0



        errSum = 0
        dErr = 0
        startTime = utime.ticks_us()


        # wait for a GPS position to be available
        await gps.positionAvailable.wait()
  
        # assume that we hold the current station     
        store.destination = store.position

        while True:
            
            currentTime = utime.ticks_us()
            deltaT =  utime.ticks_diff(currentTime,startTime )/1000000
            startTime = currentTime

            distance, desiredcourse, dx_meters, dy_meters = distanceBearing(store.position,store.destination)
        
            Kp = store.holdgain
            Ki = 0
            Kd = 0

            
            error =  distance - store.waypointarrivedradius #meters

            # update the proportional error
            p = Kp * error

            # update the integral error
            if Ki > 0:
                errSum = errSum + (error * deltaT) # s/radians
                i = Ki * errSum
            
            # update the differential error
            if Kd > 0:
                dErr = (error - lastErr) / deltaT #radians/s
                lastErr = error
                d = Kd * dErr

  
            # surge between 0..vmax
            store.surge = min(store.vmax, max(0,p+i+d))
        
            print(f"Hold: Distance: {distance:.2f}m, error={error:.2f}, surge={store.surge:.2f}, ")


            await gps.positionAvailable.wait() 

    except asyncio.CancelledError:
        print( "stopping holdTask" )