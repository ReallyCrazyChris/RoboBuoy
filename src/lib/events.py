#################################
# Central Event Instance
# all events dispatched from here
#################################

_callbacks = {}
    
def dispatch(event:str, data:object=None):

    if event in _callbacks.keys():
        if data != None:
            _callbacks[event](data)
        else:
            _callbacks[event]()
    else:
        raise Exception('no event',event) 

def on(event:str, callback:function):
    _callbacks[event] = callback

    
def un(event:str):
    del _callbacks[event]
