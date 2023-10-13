import uasyncio as asyncio
from lib.statemachine import State 
from lib.motors import driveTask
from lib.auto import autoTask
from lib.store import Store
store = Store()

class Stop(State):

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

    def transitionTo(self,statename):
        if (statename in ['manual','auto']): return statename        

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

    def transitionTo(self,statename):
        if (statename in ['stop','auto']): return statename

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

    def transitionTo(self,statename):
        if (statename in ['stop','manual']): return statename                 