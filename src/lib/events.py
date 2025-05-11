#################################
# Central Event Instance
# all events dispatched from here
#################################

_callbacks = {}

def dispatch(event:str, data:object=None):
    """ Dispatch an event to the registered callback(s) """

    if event in _callbacks.keys():
        if data != None:
            _callbacks[event](data)
        else:
            _callbacks[event]()
    else:
        raise Exception('no event',event) 

def on(event:str, callback:function):
    """ Register a callback for an event """
    _callbacks[event] = callback

    
def un(event:str):  
    """ Unregister a callback for an event """
    del _callbacks[event]
