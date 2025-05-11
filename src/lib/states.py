import uasyncio as asyncio
from lib.statemachine import State 
from lib.motors import driveTask, pidTask
from lib.auto import autoTask, holdTask
from lib.store import Store

store = Store.instance()

class Init(State):
    # TODO: remove this state, it is not needed
    ''' Initial State'''
    def __init__( self, sm ):
        self.name = 'init'
        self.sm = sm #statemachine

    async def start(self):
        store.mode=self.name
       
        # then go to state
        self.transitionTo('stop')

    def validateTransition(self,statename):
        if (statename in ['stop']): return statename

class Stop(State):
    'RoboBuoy is Stopped'
    def __init__( self, sm ):
        self.name = 'stop'
        self.sm = sm #statemachine TODO find a way not not need this here !!

    def start(self):
        """Perform these actions when this state is first entered."""
        print('enter: stop state ')
        store.mode = self.name
        store.surge = 0

    def end(self):
        """Perform these actions when this state is exited."""
        print('exit: stop state')

    def validateTransition(self,statename):
        if (statename in ['manual','hold','auto','calibratemag','calibrateaccel','calibrategyro']): return statename        

class Auto(State):

    def __init__( self ,sm):
        self.name = 'auto'
        self.sm = sm #statemachine
        self.driveTask = None
        self.pidTask = None
        self.autoTask  = None
       
    def start(self):
        store.mode=self.name
        self.driveTask = asyncio.create_task( driveTask() )
        self.pidTask = asyncio.create_task( pidTask() )
        self.autoTask = asyncio.create_task( autoTask() )

    def end(self):
        self.autoTask.cancel()
        self.pidTask.cancel()
        self.driveTask.cancel()

    def validateTransition(self,statename):
        if (statename in ['stop','manual','hold']): return statename     

class Hold(State):

    def __init__( self ,sm ):
        self.name = 'hold'
        self.sm = sm #statemachine
        self.driveTask = None
        self.pidTask = None
        self.holdTask  = None
       
    def start(self):
        store.mode=self.name
        self.driveTask = asyncio.create_task( driveTask() )
        self.pidTask = asyncio.create_task( pidTask() )
        self.holdTask = asyncio.create_task( holdTask() )

    def end(self):
        self.holdTask.cancel()
        self.pidTask.cancel()
        self.driveTask.cancel()

    def validateTransition(self,statename):
        if (statename in ['stop','manual','auto']): return statename          

class Manual(State):

    def __init__( self ,sm ):
        self.name = 'manual'
        self.sm = sm #statemachine
        self.driveTask = None
        self.pidTask = None


    def start(self):
        store.mode=self.name
        store.desiredcourse = store.currentcourse
        self.driveTask = asyncio.create_task( driveTask() )
        self.pidTask = asyncio.create_task( pidTask() )

    def end(self):
        self.driveTask.cancel()  
        self.pidTask.cancel()

    def validateTransition(self,statename):
        if (statename in ['stop','hold','auto']): return statename

class CalibrateMag(State):
    ''' The Magnetic compass is calibrating'''

    def __init__( self, sm ):
        self.name = 'calibratemag'
        self.sm = sm #statemachine
        self.driveTask=None

    async def start(self):
        from lib.storepersistance import savesettings
        from lib.imutasks import calibrateMagTask
        from lib.motors import driveMotors
        store.mode=self.name
        
        driveMotors(0,0) # stop the motors
        await asyncio.sleep(1)
        driveMotors(0.1,0) # start the motors     
        await calibrateMagTask()
        savesettings()    
        driveMotors(0,0) 
        self.transitionTo('stop')

    def validateTransition(self,statename):
        if (statename in ['stop']): return statename

class CalibrateAccel(State):
    ''' The Accelerometer is calibrating'''

    def __init__( self, sm ):
        self.name = 'calibrateaccel'
        self.sm = sm

    async def start(self):
        from lib.storepersistance import savesettings
        from lib.imutasks import calibrateAccelTask
        store.mode=self.name
        await calibrateAccelTask()
        savesettings()     
        self.transitionTo('stop')

    def validateTransition(self,statename):
        if (statename in ['stop']): return statename    

class CalibrateGyro(State):
    ''' The Gyro is Calibrating '''

    def __init__( self, sm ):
        self.name = 'calibrategyro'
        self.sm = sm

    async def start(self):
        from lib.storepersistance import savesettings
        from lib.imutasks import calibrateGyroTask
        store.mode=self.name
        await calibrateGyroTask()
        savesettings()     
        self.transitionTo('stop')

    def validateTransition(self,statename):
        if (statename in ['stop']): return statename                

            