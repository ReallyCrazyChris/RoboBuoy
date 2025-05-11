import uasyncio as asyncio
from driver.bleuart import BLEUART
from lib.events import dispatch
from transport.action_handlers import bind_actions_to_handlers
from transport.request_handlers import bind_requests_to_handlers

bleuart = BLEUART()
bleuartLock = asyncio.Lock() # async lock to prevent multiple communication actions at the same time

sendqueue = [] # of messages to be sent
receivequeue = [] # of messages that have been received
    
def send(*packet):
    """sends commands to a host server"""
    if bleuart.is_connected:
        sendqueue.append(packet)

def receive(packet):
    """recives and queue's commands to be reacted apon"""
    receivequeue.append(packet)

def react():
    """ processed the commands in the receivequeue"""

    while len(receivequeue):

        packet = receivequeue.pop(0)
        action = packet.pop(0)

        try:
            if len(packet) > 0: 
                dispatch(action,*packet)
            else:
                dispatch(action)
        except TypeError as e:
            raise TypeError(str(e), ' while processing to', action, packet)


async def receiveTask():
    ''' receives messages via bluetooth and adds them to the receive queue '''
    print('starting receiveTask')
    
    try:

        # bind actions to handlers
        bind_actions_to_handlers()
        # bind requests to handlers
        bind_requests_to_handlers()

        while True:
            if bleuart.message != None:
                receive(bleuart.message)
                react()  # TODO this may need its own async co-routine
            # clear processed message          
            bleuart.message = None
            await bleuart.received_flag.wait()
            
    except asyncio.CancelledError:
        print('stoping receiveTask') 

async def sendTask():
    ''' reads messages from the server send queue and sends them via bluetooth '''
    print('starting sendTask')
    try:

        while True:    
            if len(sendqueue) > 0:
                for packet in sendqueue:
                    await bleuart.lock.acquire()
                    await bleuart.notify( packet )
                    bleuart.lock.release()
                # clear processed message
                sendqueue.clear() 
            else:
                await asyncio.sleep_ms(200)          

    except asyncio.CancelledError:
        print('stopping sendTask')     


async def advertiseTask():
    ''' sends robobouy advertisement via via bluetooth every 2 seconds'''
    ''' allows auto reconnect'''
    print('starting advertiseTask')
    try:
        while True:    
            await asyncio.sleep_ms(2000) 
            await bleuart.lock.acquire()
            bleuart.advertise()
            bleuart.lock.release()
    except asyncio.CancelledError:
        print('stopping advertiseTask')    
