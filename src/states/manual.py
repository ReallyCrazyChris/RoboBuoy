import uasyncio as asyncio
from lib.statemachine import State 
from storage.store import Store

from tasks.drive import driveTask
from tasks.steer import steerTask


store = Store.instance()

class Manual(State):
    """ RoboBuoy is in Manual mode, it is controlled by the user via RoboBuoy app """
    def __init__( self ,sm ):
        self.name = 'manual'
        self.sm = sm #statemachine
        self.driveTask = None
        self.steerTask = None

    def start(self):
        store.mode=self.name
        store.desiredcourse = store.currentcourse
        self.driveTask = asyncio.create_task( driveTask() )
        self.steerTask = asyncio.create_task( steerTask() )

    def end(self):
        self.driveTask.cancel()  
        self.steerTask.cancel()

    def validateTransition(self,statename):
        if (statename in ['stop','hold','auto']): return statename