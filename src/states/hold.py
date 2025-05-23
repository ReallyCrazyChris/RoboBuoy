import uasyncio as asyncio
from lib.statemachine import State 
from storage.store import Store
store = Store.instance()

class Hold(State):
    """ RoboBuoy is in Hold mode, it holds its current position and heading """     
    def __init__( self ,sm ):
        self.name = 'hold'
        self.sm = sm #statemachine
        self.driveTask = None
        self.steerTask = None
        self.holdTask  = None

    def start(self):
        from tasks.drive import driveTask
        from tasks.steer import steerTask
        from tasks.hold import holdTask

        print('start: hold state')
        store.mode=self.name
        self.driveTask = asyncio.create_task( driveTask() )
        self.steerTask = asyncio.create_task( steerTask() )
        self.holdTask = asyncio.create_task( holdTask() )

    def end(self):
        print('stop: hold state')
        self.holdTask.cancel()
        self.steerTask.cancel()
        self.driveTask.cancel()
 
    def validateTransition(self,statename):
        if (statename in ['stop','manual','auto']): return statename   