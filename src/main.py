import uasyncio as asyncio
from lib.storetasks import sendMotionMessageTask
from lib import server
from lib import course
from lib.gps import GPS
from lib.statemachine import StateMachine
from lib.states import Init, Stop, Manual, Hold, Auto, CalibrateMag, CalibrateAccel, CalibrateGyro

from lib.events import on

# use store and gps singleton instances
gps = GPS()

async def mainTaskLoop():

    # Start the Tasks that must always run
    asyncio.create_task( server.receiveTask() ) # listen for incoming messages
    asyncio.create_task( server.sendTask() )    # send messages to clients
    asyncio.create_task( server.advertiseTask() ) # announce our presence to the network
    asyncio.create_task( gps.readGpsTask() )
    asyncio.create_task( sendMotionMessageTask() )  # publich motion messages to clients

    # Start the Tasks that keep the Robot on course
    asyncio.create_task( course.fuseGyroTask() ) #
    asyncio.create_task( course.fuseCompassTask() ) # fuse compass data into the gyro data
    asyncio.create_task( course.fuseGpsTask() ) 
    
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
    sm.setState('init')
    # mode change listener 
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
            