import uasyncio as asyncio
from lib.bleuart import BLEUART

bleuart = BLEUART()
bleuartLock = asyncio.Lock() # async lock to prevent multiple communication actions at the same time

class Server():

    _instance = None # Server is a singleton
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self) -> None:
        self.listeners = {}
        self.sendqueue = []
        self.receivequeue = []
        
    def messageHandler(self, message):

        print('messageHandler', message)

        if not len( message ) >= 1: return
        
        name = str(message[0])
        print('event',name,'data',message[1])
        if name in self.listeners.keys():
            self.listeners[name](message[1])
        else:
            raise Exception('no listener for event',name) 

    def addListener(self, name, handler):
        self.listeners[name] = handler
        
    def removeListener(self, name):
        del self.listeners[name]


    def send(self, *packet):
        """sends commands to a host server"""
        self.sendqueue.append(packet)


    def receive(self, packet):
        """recives and queue's commands to be reacted apon"""
        self.receivequeue.append(packet)


    def react(self):
        """ processed the commands in the receivequeue as a task in the asyncio loop"""

        while len(self.receivequeue):

            packet = self.receivequeue.pop(0)
            action = packet.pop(0)

            if not action in self.listeners:
                return  # not a known reaction
            if len(packet) > 0:
                # action has parameters
                print(packet)
                self.listeners[action](*packet)
            else:
                self.listeners[action]()


    async def receive_message(self):
        ''' receives messages via bluetooth and adds them to the receive queue '''
        print('starting server receive Task')
        try:
            while True:
                if bleuart.message != None:
                    self.receive( bleuart.message )
                    self.react() #TODO this may need its own async co-routine
                # clear processed message          
                bleuart.message = None
                await bleuart.received_event.wait()
        except asyncio.CancelledError:
            pass 

    async def send_message(self):
        ''' reads messages from the server send queue and sends them via bluetooth '''
        print('starting server send Task')
        try:
            # after connection try sending
            await bleuart.connect_event.wait()

            while True:    
                if len(self.sendqueue) > 0:
                    for packet in self.sendqueue:
                        await bleuart.lock.acquire()
                        await bleuart.notify( packet )
                        bleuart.lock.release()
                    # clear processed message
                    self.sendqueue.clear() 
                else:
                    await asyncio.sleep_ms(200)          

        except asyncio.CancelledError:
            pass     


    async def bluetooth_advertise(self):
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




