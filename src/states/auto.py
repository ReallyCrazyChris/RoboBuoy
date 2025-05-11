import uasyncio as asyncio
from lib.statemachine import State 
from storage.store import Store

from tasks.drive import driveTask
from tasks.steer import steerTask
from tasks.auto import autoTask

store = Store.instance()

class Auto(State):
    """ RoboBuoy is in Auto mode, it follows a paht of waypoints """
    def __init__( self ,sm):
        self.name = 'auto'
        self.sm = sm #statemachine
        self.driveTask = None
        self.steerTask = None
        self.autoTask  = None
       
    def start(self):
        store.mode=self.name
        self.driveTask = asyncio.create_task( driveTask() )
        self.steerTask = asyncio.create_task( steerTask() )
        self.autoTask = asyncio.create_task( autoTask() )

    def end(self):
        self.autoTask.cancel()
        self.steerTask.cancel()
        self.driveTask.cancel()

    def validateTransition(self,statename):
        if (statename in ['stop','manual','hold']): return statename   