import uasyncio as asyncio
from lib.store import Store
from lib import server
from lib import course
from lib.gps import GPS
from lib.motors import armMotorsCoroutine
from lib.statemachine import StateMachine
from lib.states import Stop, Manual, Auto

# use store and gps singleton instances
store = Store()
gps = GPS()


async def mainTaskLoop():

    # Start the Tasks that must always run
    asyncio.create_task( server.receiveTask() )
    asyncio.create_task( server.sendTask() )
    asyncio.create_task( server.advertiseTask() )
    asyncio.create_task( gps.readGpsTask() )
    asyncio.create_task( store.sendMotionStateTask() )

    # Start the Tasks that keep the Robot on course
    asyncio.create_task( course.fuseGyroTask() )
    asyncio.create_task( course.fuseCompassTask() )
    asyncio.create_task( course.fuseGpsTask() )
    
    # Statemachine to manage the robots operational modes aka transition states
    sm = StateMachine()
    sm.addState(Stop())
    sm.addState(Manual())
    sm.addState(Auto())
    sm.setState('stop')
    server.addListener('mode',sm.transitionTo)

     # Arm the motors 
    await armMotorsCoroutine()

    # Keep the mainTaskLoop running forever    
    while 1:
        #TODO WDT?
        await asyncio.sleep(100000)  # Pause 1s    
  
if __name__ == "__main__": 
    print('robobuoy v0.1')
    asyncio.run( mainTaskLoop() )
 