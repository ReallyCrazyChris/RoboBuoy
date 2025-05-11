from lib.events import on
from transport import server
from transport.storemessages import statemessage_chunk1,statemessage_chunk2,statemessage_chunk3,statemessage_chunk4,statemessage_chunk5,statemessage_chunk6,statemessage_chunk7
from transport.storemessages import pidsettingsmessage, motorsettingsmessage,alphasettingsmessage, holdsettingsmessage


def bind_requests_to_handlers():
    on('getState',getState)
    on('getHoldsettings', getHoldsettings)
    on('getPIDsettings', getPIDsettings)
    on('getMotorsettings', getMotorsettings)
    on('getAlphasettings', getAlphasettings)

def getState():
    ''' send the state to the RoboBouyApp in chunks '''
    # send state in chunks, so as not to overlaod the bluetoot communiction
    server.send('state',statemessage_chunk1())
    server.send('state',statemessage_chunk2())
    server.send('state',statemessage_chunk3())
    server.send('state',statemessage_chunk4())
    server.send('state',statemessage_chunk5())
    server.send('state',statemessage_chunk6())


def getHoldsettings(): 
    server.send('state',holdsettingsmessage())   
    
def getPIDsettings():
    server.send('state',pidsettingsmessage())

def getMotorsettings():
    server.send('state',motorsettingsmessage())        

def getAlphasettings():
    server.send('state',alphasettingsmessage())  



 


