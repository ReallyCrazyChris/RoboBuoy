import uasyncio as asyncio
from lib.statemachine import State 
from storage.store import Store

from storage.storepersistance import savesettings
from tasks.calibrateGyro import calibrateGyroTask

store = Store.instance()

class CalibrateGyro(State):
    ''' The Gyro is Calibrating '''

    def __init__( self, sm ):
        self.name = 'calibrategyro'
        self.sm = sm

    async def start(self):
        store.mode=self.name
        await calibrateGyroTask()
        savesettings()     
        self.transitionTo('stop')

    def validateTransition(self,statename):
        if (statename in ['stop']): return statename                
