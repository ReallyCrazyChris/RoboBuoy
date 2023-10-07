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



