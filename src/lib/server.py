import uasyncio as asyncio
from lib.bleuart import BLEUART

bleuart = BLEUART()
bleuartLock = asyncio.Lock() # async lock to prevent multiple communication actions at the same time

listeners = {}
sendqueue = []
receivequeue = []
    
def messageHandler(message):

    if not len( message ) >= 1: return
    
    name = str(message[0])

    if name in listeners.keys():
        listeners[name](message[1])
    else:
        raise Exception('no listener for event',name) 

def addListener(name, handler):
    listeners[name] = handler
    
def removeListener(name):
    del listeners[name]

def send(*packet):
    """sends commands to a host server"""
    if bleuart.is_connected:
        sendqueue.append(packet)

def receive(packet):
    """recives and queue's commands to be reacted apon"""
    receivequeue.append(packet)

def react():
    """ processed the commands in the receivequeue as a task in the asyncio loop"""

    while len(receivequeue):

        packet = receivequeue.pop(0)
        action = packet.pop(0)

        if not action in listeners:
            # not a known reaction
            print(action, 'unknown')
            return  
        if len(packet) > 0: 
            # action has parameters
            listeners[action](*packet)
        else:
            listeners[action]()

async def receive_message():
    ''' receives messages via bluetooth and adds them to the receive queue '''
    print('starting server receive Task')
    try:
        while True:
            if bleuart.message != None:
                receive( bleuart.message )
                react() #TODO this may need its own async co-routine
            # clear processed message          
            bleuart.message = None
            await bleuart.received_flag.wait()
            
    except asyncio.CancelledError:
        pass 

async def send_message():
    ''' reads messages from the server send queue and sends them via bluetooth '''
    print('starting server send Task')
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
        pass     


async def bluetooth_advertise():
    ''' sends robobouy advertisement via via bluetooth every 2 seconds'''
    ''' allows auto reconnect'''
    print('starting Bluetooth advertise Task')
    try:
        while True:    
            await asyncio.sleep_ms(2000) 
            await bleuart.lock.acquire()
            bleuart.advertise()
            bleuart.lock.release()
    except asyncio.CancelledError:
        pass    
