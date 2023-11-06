import uasyncio as asyncio
from lib.statemachine import State 
from lib.motors import driveTask
from lib.auto import autoTask, holdTask

from lib.store import Store
store = Store()

# Unused Movement States : Adrift, underWay, afloat, aground, obstacle ahead, ahoy, alongside, anchored, ashore, capsize,
# Unused Indication States : beaconing, bell
# Events: collusion


class Stop(State):
    'RoboBuoy is Stopped'
    def __init__( self ):
        self.name = 'stop'

    def start(self):
        """Perform these actions when this state is first entered."""
        print('stop state entry')
        store.mode=self.name
        store.setsurge(0)

    def end(self):
        """Perform these actions when this state is exited."""
        print('stop state exit')

    def canTransitionTo(self,statename):
        if (statename in ['manual','hold','auto','calibratemag']): return statename        


class Auto(State):

    def __init__( self ):
        self.name = 'auto'
        self.driveTask = None
        self.autoTask  = None
       
    def start(self):
        store.mode=self.name
        self.driveTask = asyncio.create_task( driveTask() )
        self.autoTask = asyncio.create_task( autoTask() )

    def end(self):
        self.autoTask.cancel()
        self.driveTask.cancel()

    def canTransitionTo(self,statename):
        if (statename in ['stop','manual','hold']): return statename     

class Hold(State):

    def __init__( self ):
        self.name = 'hold'
        self.driveTask = None
        self.holdTask  = None
       
    def start(self):
        store.mode=self.name
        self.driveTask = asyncio.create_task( driveTask() )
        self.holdTask = asyncio.create_task( holdTask() )

    def end(self):
        self.holdTask.cancel()
        self.driveTask.cancel()

    def canTransitionTo(self,statename):
        if (statename in ['stop','manual','auto']): return statename          

class Manual(State):

    def __init__( self ):
        self.name = 'manual'
        self.driveTask=None

    def start(self):
        store.mode=self.name
        store.desiredcourse = store.currentcourse
        self.driveTask = asyncio.create_task( driveTask() )

    def end(self):
        self.driveTask.cancel()  

    def canTransitionTo(self,statename):
        if (statename in ['stop','hold','auto']): return statename


class CalibrateMag(State):
    ''' The Magnetic compass is calibrating'''

    def __init__( self ):
        self.name = 'calibratemag'
        self.driveTask=None

    def start(self):
        store.mode=self.name
        self.driveTask = asyncio.create_task( driveTask() )
        # slow rotation on the robots axis
        store.setsurge(0)  
        store.setsteer(20) 
        self.transitionTo('stop')

    def action(self,statename):
        ''' Calibrate the Magnetometer'''
        #from lib.imu import IMU
        #imu = IMU()
        #imu.calibrateMag(800,10)


    def end(self):
        self.driveTask.cancel()  

    def canTransitionTo(self,statename):
        if (statename in ['stop']): return statename

            