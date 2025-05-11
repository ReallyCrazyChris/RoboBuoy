import uasyncio as asyncio
from lib.statemachine import State 
from storage.store import Store

from storage.storepersistance import savesettings
from tasks.calibrateAccel import calibrateAccelTask


store = Store.instance()

   
class CalibrateAccel(State):
    ''' The Accelerometer is calibrating'''

    def __init__( self, sm ):
        self.name = 'calibrateaccel'
        self.sm = sm

    async def start(self):
        store.mode=self.name
        await calibrateAccelTask()
        savesettings()     
        self.transitionTo('stop')

    def validateTransition(self,statename):
        if (statename in ['stop']): return statename  