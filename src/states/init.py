import uasyncio as asyncio
from lib.statemachine import State 

from storage.storepersistance import loadsettings
from tasks.calibrateGyro import calibrateGyroTask
from tasks.armMotors import armMotorsTask
from tasks.fuseGyro import fuseGyroTask
from tasks.fuseCompass import fuseCompassTask
from tasks.fuseGPS import fuseGpsTask
from transport import server
from driver.gps import GPS
from tasks.sendMotionMessage import sendMotionMessageTask


from storage.store import Store
store = Store.instance()
gps = GPS()
class Init(State):

    ''' State for the initialization of the robot '''
    def __init__( self, sm ):
        self.name = 'init'
        self.sm = sm #statemachine

    async def start(self):
        store.mode=self.name
        # initialization of the robot goes here
        await calibrateGyroTask()
        loadsettings()  # load settings from the filesystem
        await armMotorsTask()

        # Start the Tasks that must always run
        asyncio.create_task( server.receiveTask() ) # receive ble messages from RoboBouyAPP
        asyncio.create_task( server.sendTask() )    # send ble messages to RoboBouyAPP
        asyncio.create_task( server.advertiseTask() ) # announce ble to RoboBouyAPP
        asyncio.create_task( gps.readGpsTask() )
        asyncio.create_task( sendMotionMessageTask() )  # publish motion messages to clients

        # Start the Tasks that keep the Robot on course
        asyncio.create_task( fuseGyroTask() ) # fuse the gyro heading with the current course
        asyncio.create_task( fuseCompassTask() ) # fuse compass heading with the current course
        asyncio.create_task( fuseGpsTask() ) # fuse the gps heading with the current course
        
        # then go to state
        self.transitionTo('manual')

    def validateTransition(self,statename):
        if (statename in ['stop','manual','hold']): return statename