import uasyncio as asyncio
import gc
from driver.lora import lora
from lib.events import dispatch
from transport.action_handlers import bind_actions_to_handlers
from transport.request_handlers import bind_requests_to_handlers

lora = lora()
loraLock = asyncio.Lock() # async lock to prevent multiple communication actions at the same time

lorasendqueue = [] # of messages to be sent
lorareceivequeue = [] # of messages that have been received
    
def send(*packet):
    """sends commands to a host server"""
    if lora.is_connected:
        lorasendqueue.append(packet)

def receive(packet):
    """recives and queue's commands to be reacted apon"""
    lorareceivequeue.append(packet)

def react():
    """ processed the commands in the lorareceivequeue"""

    while len(lorareceivequeue):

        packet = lorareceivequeue.pop(0)
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
            if lora.message != None:
                receive(lora.message)
                gc.collect()
                react()  # TODO this may need its own async co-routine
            # clear processed message          
            lora.message = None
            await lora.received_flag.wait()
            
    except asyncio.CancelledError:
        print('stoping receiveTask') 

async def sendTask():
    ''' reads messages from the server send queue and sends them via bluetooth '''
    print('starting sendTask')
    try:

        while True:    
            if len(lorasendqueue) > 0:
                for packet in lorasendqueue:
                    await lora.lock.acquire()
                    await lora.notify( packet )
                    lora.lock.release()
                # clear processed message
                lorasendqueue.clear() 
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
            await lora.lock.acquire()
            lora.advertise()
            lora.lock.release()
    except asyncio.CancelledError:
        print('stopping advertiseTask')    
