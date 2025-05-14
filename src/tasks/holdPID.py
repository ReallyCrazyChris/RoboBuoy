import utime
import uasyncio as asyncio

from storage.store import Store
store = Store.instance()

async def holdPIDTask():
    ''' 
        a PID conttoller is used to dampen the respoinse of the RoboBouy to GPS gitter 
    '''
  
    from math import sqrt, atan2
    from lib.utils import positionDifference
    from driver.gps import GPS 
    gps = GPS()

    last_time = utime.ticks_us()

    kp = 1
    ki = 0
    kd = 0

    integral_error_x =0
    integral_error_y = 0

    last_error_x = 0
    last_error_y = 0

    # assume that we hold the current station     
    store.destination = store.position # TODO this needs to be part of the state control
    
    try: 
        print('starting holdPIDTask')

        # wait for a GPS position to be available
        await gps.positionAvailable.wait()

        while True:
            # Calculate position error in meters
            error_x, error_y = positionDifference(store.position,store.destination)
            
            current_time = utime.ticks_us()
            dt =  utime.ticks_diff(current_time,last_time )/1000000
            last_time = current_time
    
            # Calculate PID control values
            # Proportional term
            p_term_x = kp * error_x
            p_term_y = kp * error_y
            
            # Integral term
            integral_error_x += error_x * dt
            integral_error_y += error_y * dt
            i_term_x = ki * integral_error_x
            i_term_y = ki * integral_error_y
            
            # Derivative term
            derivative_x = (error_x - last_error_x) / dt if dt > 0 else 0
            derivative_y = (error_y - last_error_y) / dt if dt > 0 else 0
            d_term_x = kd * derivative_x
            d_term_y = kd * derivative_y
            
            # Calculate thrust commands
            thrust_x = p_term_x + i_term_x + d_term_x
            thrust_y = p_term_y + i_term_y + d_term_y
            
            # Store errors for next iteration
            last_error_x = error_x
            last_error_y = error_y
            
            distance_meters = round(sqrt(thrust_x**2 + thrust_y**2),1)   # distance in meters, limted to 1 decimal
            desiredcourse = round(atan2(thrust_x,thrust_y),3) # bearing in radians, limited to 3 decimals

            # Reduce the surge as the RoboBouy approached the waypoint
            surge = min(store.vmax, distance_meters**2 / store.waypointarrivedradius**2 )

            # Update the Store
            store.surge = surge
            store.desiredcourse = desiredcourse

            print(f"Position error: {error_x:.2f}m, {error_y:.2f}m, Distance: {distance_meters:.2f}m, Applying thrust: surge={surge:.2f}, desiredcourse={desiredcourse:.2f}")

            await gps.positionAvailable.wait() 

    except asyncio.CancelledError:
        print( "stopping holdPIDTask" )

