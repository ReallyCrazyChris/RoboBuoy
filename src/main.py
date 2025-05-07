import uasyncio as asyncio

from lib.store import Store
from lib.storetasks import sendMotionMessageTask
from lib.events import on
from lib.gps import GPS
from lib.storepersistance import loadsettings

from lib import server
from lib import course

from lib.statemachine import StateMachine
from lib.states import Init, Stop, Manual, Hold, Auto, CalibrateMag, CalibrateAccel, CalibrateGyro

from lib.imutasks import calibrateGyroTask
from lib.motors import armMotorsCoroutine


store = Store.instance()
gps = GPS()

async def mainTaskLoop():

    #loadsettings() # load settings from the filesystem

    await calibrateGyroTask() # calibrate the gyro
    await armMotorsCoroutine() # arm the motors
    
    # Start the Tasks that must always run
    asyncio.create_task( server.receiveTask() ) # listen for incoming messages
    asyncio.create_task( server.sendTask() )    # send messages to clients
    asyncio.create_task( server.advertiseTask() ) # announce our presence to the network
    asyncio.create_task( gps.readGpsTask() )
    asyncio.create_task( sendMotionMessageTask() )  # publish motion messages to clients

    # Start the Tasks that keep the Robot on course
    asyncio.create_task( course.fuseGyroTask() ) #
    #asyncio.create_task( course.fuseCompassTask() ) # fuse compass data into the gyro data
    #asyncio.create_task( course.fuseGpsTask() ) 

 

    
    # Statemachine to manage the robots operational modes aka states
    sm = StateMachine()
    sm.addState(Init)
    sm.addState(Stop)
    sm.addState(Manual)
    sm.addState(Hold)
    sm.addState(Auto)
    sm.addState(CalibrateMag)
    sm.addState(CalibrateAccel)
    sm.addState(CalibrateGyro)
    sm.setState('manual')

    # bind actions to handlers
    on('number', store.set_number)
    on('type', store.set_type)
    on('name', store.set_name)
    on('color', store.set_color)
    on('battery', store.set_battery)
    on('positionvalid', store.set_positionvalid)
    on('position', store.set_position)
    on('gpscourse', store.set_gpscourse)
    on('gpsspeed', store.set_gpsspeed)
    on('magcourse', store.set_magcourse)
    on('magdeclination', store.set_magdeclination)
    on('currentcourse', store.set_currentcourse)
    on('destination', store.set_destination)
    on('distance', store.set_distance)
    on('dc', store.set_desiredcourse)
    on('wp', store.set_waypoints)
    on('wr', store.set_waypointarrivedradius)
    on('holdgain', store.set_holdgain)
    on('Kp', store.set_Kp)
    on('Ki', store.set_Ki)
    on('Kd', store.set_Kd)
    on('gpsalpha', store.set_gpsalpha)
    on('magalpha', store.set_magalpha)
    on('declinationalpha', store.set_declinationalpha)
    on('surge', store.set_surge)
    on('steer', store.set_steer)
    #on('steergain', store.set_steergain)
    on('vmin', store.set_vmin)
    on('vmax', store.set_vmax)
    on('minPwmLeft', store.set_mpl)
    on('minPwmRight', store.set_mpr)
    on('maxpwm', store.set_maxpwm)   
    on('mode',sm.transitionTo)



    #TODO I dont like this. it looks very pointless
    # Actually these need to go in the states they are used in
    import lib.storerequests

    # Keep the mainTaskLoop running forever    
    while 1:
        #TODO WDT?
        await asyncio.sleep(100000)  # Pause 1s    
  
if __name__ == "__main__": 
    print('robobuoy v0.1')
    asyncio.run( mainTaskLoop() )
            