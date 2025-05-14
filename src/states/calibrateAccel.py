import uasyncio as asyncio
from lib.statemachine import State 
from storage.store import Store
store = Store.instance()

class CalibrateAccel(State):
    ''' The Accelerometer is calibrating'''

    def __init__( self, sm ):
        self.name = 'calibrateaccel'
        self.sm = sm

    async def start(self):
        from tasks.calibrateAccel import calibrateAccelTask
        from storage.storepersistance import savesettings

        store.mode=self.name
        await calibrateAccelTask()
        savesettings()     
        self.transitionTo('stop')

    def validateTransition(self,statename):
        if (statename in ['stop']): return statename  