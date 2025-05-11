import uasyncio as asyncio
from transport import server
from transport.storemessages import motionmessage    

async def sendMotionMessageTask():
    ''' continously sends the motion informaiton to the RoboBouyApp '''
    try:
        print('starting sendMotionMessageTask')
        while True:
            await asyncio.sleep_ms(1000)  
            server.send('state',motionmessage())

    except asyncio.CancelledError:
        print( "stopping sendMotionMessageTask")