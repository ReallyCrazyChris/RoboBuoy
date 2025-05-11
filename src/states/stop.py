import uasyncio as asyncio
from lib.statemachine import State 
from storage.store import Store


store = Store.instance()

class Stop(State):
    'RoboBuoy is Stopped'
    def __init__( self, sm ):
        self.name = 'stop'
        self.sm = sm #statemachine TODO find a way not not need this here !!

    def start(self):
        """Perform these actions when this state is first entered."""
        store.mode = self.name
        store.surge = 0

    def end(self):
        """Perform these actions when this state is exited."""
        print('exit: stop state')

    def validateTransition(self,statename):
        if (statename in ['manual','hold','auto','calibratemag','calibrateaccel','calibrategyro']): return statename 