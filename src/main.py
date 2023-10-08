import uasyncio as asyncio
from lib import server

from lib import course
from lib import path
from lib.gps import GPS
from lib.store import Store
store = Store()
gps = GPS()

async def mainTaskLoop():

    #await controller.armmotors()

    # Start the Tasks that must always run
    asyncio.create_task( server.receive_message() )
    asyncio.create_task( server.send_message() )
    asyncio.create_task( server.bluetooth_advertise() )

    # Start the Tasks that keep the Robot in course
    course.startFuseGyroTask()
    course.startFuseCompassTask()
    course.startFuseGpsTask()

    # Start the Task that hold station or follow a wapoint path
    gps.startReadGpsTask()
    path.startFollowPathTask()
    #path.startHoldStationTask()

    # Start Tasks the send state to the RoboBuoyApp
    store.startSendMotionStateTask()

    # Keep the mainTaskLoop running forever    
    while 1:
        await asyncio.sleep(100000)  # Pause 1s    
  
if __name__ == "__main__": 
    print('robobuoy v0.1')
    asyncio.run( mainTaskLoop() )
 