import uasyncio as asyncio
from lib.statemachine import State 
from storage.store import Store
from storage.storepersistance import savesettings
from tasks.calibrateMag import calibrateMagTask
from tasks.slowRightRotate import slowRightRotateTask

store = Store.instance()

class CalibrateMag(State):
    ''' The Magnetic compass is calibrating'''

    def __init__( self, sm ):
        self.name = 'calibratemag'
        self.sm = sm #statemachine
        self.slowRightRotate = None
   
    async def start(self):
        store.mode=self.name

        # rotate the buoy slowly to calibrate the magnetometer
        self.slowRightRotate = asyncio.create_task(slowRightRotateTask(0.1, 0))
        await calibrateMagTask()
        # save the calibration settings
        savesettings()    
        
        self.transitionTo('stop')

    def end(self):
        # stop the slow right rotation
        self.slowRightRotate.cancel()      

    def validateTransition(self,statename):
        if (statename in ['stop']): return statename