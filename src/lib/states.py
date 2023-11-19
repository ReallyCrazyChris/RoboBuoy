import uasyncio as asyncio
from lib.statemachine import State 
from lib.motors import armMotorsCoroutine,driveTask
from lib.auto import autoTask, holdTask

from lib.events import on
from lib.store import Store
from lib.storepersistance import loadsettings
store = Store.instance()

class Init(State):
    ''' Initial State'''
    def __init__( self, sm ):
        self.name = 'init'
        self.sm = sm #statemachine

    async def start(self):
        from lib.imupersistance import loadimuconfig
        store.mode=self.name
        
        loadimuconfig()
        loadsettings()

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
        on('Kp', store.set_Kp)
        on('Ki', store.set_Ki)
        on('Kd', store.set_Kd)
        on('gpsalpha', store.set_gpsalpha)
        on('magalpha', store.set_magalpha)
        on('declinationalpha', store.set_declinationalpha)
        on('surge', store.set_surge)
        on('steer', store.set_steer)
        on('vmin', store.set_vmin)
        on('vmax', store.set_vmax)
        on('mpl', store.set_mpl)
        on('mpr', store.set_mpr)
        on('maxpwm', store.set_maxpwm)  

        # arm the motors
        await armMotorsCoroutine()
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
        print('stop state entry')
        store.mode = self.name
        store.surge = 0

    def end(self):
        """Perform these actions when this state is exited."""
        print('stop state exit')

    def validateTransition(self,statename):
        if (statename in ['manual','hold','auto','calibratemag','calibrateaccel','calibrategyro']): return statename        


class Auto(State):

    def __init__( self ,sm):
        self.name = 'auto'
        self.sm = sm #statemachine
        self.driveTask = None
        self.autoTask  = None
       
    def start(self):
        store.mode=self.name
        self.driveTask = asyncio.create_task( driveTask() )
        self.autoTask = asyncio.create_task( autoTask() )

    def end(self):
        self.autoTask.cancel()
        self.driveTask.cancel()

    def validateTransition(self,statename):
        if (statename in ['stop','manual','hold']): return statename     

class Hold(State):

    def __init__( self ,sm ):
        self.name = 'hold'
        self.sm = sm #statemachine
        self.driveTask = None
        self.holdTask  = None
       
    def start(self):
        store.mode=self.name
        self.driveTask = asyncio.create_task( driveTask() )
        self.holdTask = asyncio.create_task( holdTask() )

    def end(self):
        self.holdTask.cancel()
        self.driveTask.cancel()

    def validateTransition(self,statename):
        if (statename in ['stop','manual','auto']): return statename          

class Manual(State):

    def __init__( self ,sm ):
        self.name = 'manual'
        self.sm = sm #statemachine
        self.driveTask=None

    def start(self):
        store.mode=self.name
        store.desiredcourse = store.currentcourse
        self.driveTask = asyncio.create_task( driveTask() )

    def end(self):
        self.driveTask.cancel()  

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
        from motors import driveMotors
        store.mode=self.name
        driveMotors(60,0)      
        await calibrateMagTask()
        savesettings()     
        self.transitionTo('stop')

    def end(self):
        from motors import stopMotors
        stopMotors()

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

            