import uasyncio as asyncio
import utime
from math import pi
from lib.utils import normalize
from storage.store import Store
store = Store.instance()



async def steerTask():
    ''' 
    The steerTask is a PID controller that calculates the steering
    angle based on the current course and the desired course.
    The goal of the PID controller is to get the robot to follow 
    the desired course, considering the current course
    '''

    # clear the error accumulators
    store.errSum = 0
    store.dErr = 0
    startTime = utime.ticks_us()

    try: 
        print('starting steerTask')

        p = 0
        i = 0
        d = 0

        while True:

            await asyncio.sleep_ms(10)

            # calculate the timer derivative deltaT
            currentTime = utime.ticks_us()
            deltaT =  utime.ticks_diff(currentTime,startTime )/1000000
            startTime = currentTime

            # determine the path of least rotation
            rotationA = store.course - store.heading
            rotationB = (2*pi + rotationA) % (2*pi)

            # apply the path of least rotaiton
            if rotationA >= rotationB:
                store.error = normalize(rotationB)
            else:
                store.error = normalize(rotationA)

            #print("heading: %5.2f course: %5.2f error: %5.2f" % (store.heading ,store.course,store.error))

            # update the proportional error
            p = store.Kp * store.error

            # update the integral error
            if store.Ki > 0:
                store.errSum = store.errSum + (store.error * deltaT) # s/radians
            i = store.Ki * store.errSum
            
            # update the differential error
            if store.Kd > 0:
                store.dErr = (store.error - store.lastErr) / deltaT #radians/s
                store.lastErr = store.error
            
            d = store.Kd * store.dErr

            # steer is between -pi and pi radians
            store.steer = normalize(p + i + d) # radians
            
            #print table of the PID values
            #print("p: %5.2f i: %5.2f d: %5.2f steer: %5.2f" % (p, i, d, store.steer))

    except asyncio.CancelledError:
        print( "stopping steerTask" )