import uasyncio as asyncio
from lib.events import on
from lib.statemachine import StateMachine

from states.init import Init
from states.stop import Stop
from states.manual import Manual
from states.hold import Hold
from states.auto import Auto
from states.calibrateAccel import CalibrateAccel
from states.calibrateGyro import CalibrateGyro
from states.calibrateMag import CalibrateMag

async def mainTaskLoop():

    # Statemachine to manage the robots operational modes aka states
    sm = StateMachine()
    sm.addState(Init)
    sm.addState(Stop)
    sm.addState(Manual)
    sm.addState(Hold)
    sm.addState(Auto)
    sm.addState(CalibrateMag)
    sm.addState(CalibrateAccel)
    sm.addState(CalibrateGyro)
    # set the initial state to manual
    sm.setState('init')
    # bind action to handler
    on('mode',sm.transitionTo)

    # Keep the mainTaskLoop running forever    
    while 1:
        #TODO WDT?
        await asyncio.sleep(100000)  # Pause 1s    
  
if __name__ == "__main__": 
    print('RoboBouy v0.2')
    asyncio.run( mainTaskLoop() )
            