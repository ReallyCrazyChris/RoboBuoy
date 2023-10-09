import uasyncio as asyncio
from lib.store import Store
from lib import server
from lib import course
from lib import path
from lib import motors
from lib.gps import GPS

store = Store()
gps = GPS()

async def mainTaskLoop():

    # Start the Tasks that must always run
    asyncio.create_task( server.receiveMessageTask() )
    asyncio.create_task( server.sendMessageTask() )
    asyncio.create_task( server.bluetoothAdvertiseTask() )

    # Start the Tasks that keep the Robot in course
    course.startFuseGyroTask()
    #course.startFuseCompassTask()
    course.startFuseGpsTask()

    # Start the Task that hold station or follow a wapoint path
    gps.startReadGpsTask()
    path.startFollowPathTask()
    #path.startHoldStationTask()

    # Start Tasks the send state to the RoboBuoyApp
    store.startSendMotionStateTask()

    # Arm and Start the motors 
    await motors.armMotorsTask()
    motors.startDriveMotorsTask()

    # Keep the mainTaskLoop running forever    
    while 1:
        #TODO WDT?
        await asyncio.sleep(100000)  # Pause 1s    
  
if __name__ == "__main__": 
    print('robobuoy v0.1')
    asyncio.run( mainTaskLoop() )
 