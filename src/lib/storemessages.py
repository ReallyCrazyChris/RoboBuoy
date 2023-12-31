##################################################### 
# Messages that update RoboBuoyAPP State
#####################################################

from lib.store import Store
store = Store.instance()

def statemessage():
    ''' state that changes when the robot is initalized '''
    return {
        "number":store.number,
        "type":store.type,
        "name":store.name,
        "color":store.color,
        "mode":store.mode,
        "battery":store.battery,
        "positionvalid":store.positionvalid,
        "position":store.position,
        "gpscourse":store.gpscourse,
        "gpsspeed":store.gpsspeed,
        "magcourse":store.magcourse,
        "magdeclination":store.magdeclination,
        "currentcourse":int(store.currentcourse),
        "destination":store.destination,
        "distance":store.distance,
        "desiredcourse":store.desiredcourse,
        "waypoints":store.waypoints,
        "waypointarrivedradius":store.waypointarrivedradius,
        "holdgain":store.holdgain,
        "Kp":store.Kp,
        "Ki":store.Ki,
        "Kd":store.Kd,
        "error":store.error,
        "errSum":store.errSum,
        "dErr":store.dErr,
        "lastErr":store.lastErr,
        "gpsalpha":store.gpsalpha,
        "magalpha":store.magalpha,
        "declinationalpha":store.declinationalpha,
        "surge":store.surge,
        "steer":store.steer,
        "steergain":store.steergain,
        "vmin":store.vmin,
        "vmax":store.vmax,
        "mpl":store.mpl,
        "mpr":store.mpr,
        "maxpwm":store.maxpwm,
    }


##################################################### 
# The state is chunked to fit the radio modems MTU

def statemessage_chunk1():
    ''' state that changes when the robot is initalized '''
    return {
        "number":store.number,
        "type":store.type,
        "name":store.name,
        "color":store.color,
        "mode":store.mode,
        "battery":store.battery,
    }

def statemessage_chunk2():
    ''' state that changes when the robot is initalized '''
    return {
        "positionvalid":store.positionvalid,
        "position":store.position,
        "gpscourse":store.gpscourse,
        "gpsspeed":store.gpsspeed,
        "magcourse":store.magcourse,
        "magdeclination":store.magdeclination,
    }

def statemessage_chunk3():
    ''' state that changes when the robot is initalized '''
    return {
        "currentcourse":int(store.currentcourse),
        "destination":store.destination,
        "distance":store.distance,
        "desiredcourse":store.desiredcourse,
    }

def statemessage_chunk4():
    ''' state that changes when the robot is initalized '''
    return {
        "waypoints":store.waypoints,
        "waypointarrivedradius":store.waypointarrivedradius,
        "holdgain":store.holdgain,
    }

def statemessage_chunk5():
    ''' state that changes when the robot is initalized '''
    return {
        "Kp":store.Kp,
        "Ki":store.Ki,
        "Kd":store.Kd,
        "error":store.error,
        "errSum":store.errSum,
        "dErr":store.dErr,
        "lastErr":store.lastErr,
    }

def statemessage_chunk6():
    ''' state that changes when the robot is initalized '''
    return {
        "gpsalpha":store.gpsalpha,
        "magalpha":store.magalpha,
        "declinationalpha":store.declinationalpha,
        "surge":store.surge,
        "steer":store.steer,
        "steergain":store.steergain,
    }

def statemessage_chunk7():
    ''' state that changes when the robot is initalized '''
    return {
        "vmin":store.vmin,
        "vmax":store.vmax,
        "mpl":store.mpl,
        "mpr":store.mpr,
        "maxpwm":store.maxpwm,
    }


def motionmessage():
    ''' state that changes when the robot moves '''
    return {
        #"number":store.number,
        #"type":store.type,
        #"name":store.name,
        #"color":store.color,
        "mode":store.mode,
        #"battery":store.battery,
        "positionvalid":store.positionvalid,
        "position":store.position,
        "gpscourse":store.gpscourse,
        "gpsspeed":store.gpsspeed,
        "magcourse":store.magcourse,
        "magdeclination":store.magdeclination,
        "currentcourse":int(store.currentcourse),
        #"destination":store.destination,
        #"distance":store.distance,
        "desiredcourse":store.desiredcourse,
        #"waypoints":store.waypoints,
        #"waypointarrivedradius":store.waypointarrivedradius,
        #"holdgain":store.holdgain,
        #"Kp":store.Kp,
        #"Ki":store.Ki,
        #"Kd":store.Kd,
        #"error":store.error,
        #"errSum":store.errSum,
        #"dErr":store.dErr,
        #"lastErr":store.lastErr,
        #"gpsalpha":store.gpsalpha,
        #"magalpha":store.magalpha,
        #"declinationalpha":store.declinationalpha,
        "surge":store.surge,
        #"steer":store.steer,
        #"steergain":store.steergain,
        #"vmin":store.vmin,
        #"vmax":store.vmax,
        #"mpl":store.mpl,
        #"mpr":store.mpr,
        #"maxpwm":store.maxpwm,
    }

def waypointmessage():
    ''' state that changes when the robot reaches a waypoint '''
    return {
        "waypoints":store.waypoints,
    }



def coursesettingsmessage():
    ''' state that changes with the robots course settings '''
    return {
        #"number":store.number,
        #"type":store.type,
        #"name":store.name,
        #"color":store.color,
        #"mode":store.mode,
        #"battery":store.battery,
        #"positionvalid":store.positionvalid,
        #"position":store.position,
        "gpscourse":store.gpscourse,
        "gpsspeed":store.gpsspeed,
        "magcourse":store.magcourse,
        "magdeclination":store.magdeclination,
        "currentcourse":int(store.currentcourse),
        #"destination":store.destination,
        #"distance":store.distance,
        "desiredcourse":store.desiredcourse,
        #"waypoints":store.waypoints,
        #"waypointarrivedradius":store.waypointarrivedradius,
        #"holdgain":store.holdgain,
        #"Kp":store.Kp,
        #"Ki":store.Ki,
        #"Kd":store.Kd,
        #"error":store.error,
        #"errSum":store.errSum,
        #"dErr":store.dErr,
        #"lastErr":store.lastErr,
        #"gpsalpha":store.gpsalpha,
        #"magalpha":store.magalpha,
        #"declinationalpha":store.declinationalpha,
        "surge":store.surge,
        #"steer":store.steer,
        #"steergain":store.steergain,
        #"vmin":store.vmin,
        #"vmax":store.vmax,
        #"mpl":store.mpl,
        #"mpr":store.mpr,
        #"maxpwm":store.maxpwm,
    }


def holdsettingsmessage():
    ''' configuraiton parameters for holding station'''
    return {
        "waypointarrivedradius":store.waypointarrivedradius,
        "holdgain":store.holdgain,
    }

def pidsettingsmessage():
    ''' state that changes when the robot steering setting change '''
    return {
        "Kp":store.Kp,
        "Ki":store.Ki,
        "Kd":store.Kd,
   
    }

def motorsettingsmessage():
    ''' state that changes when the robot steering setting change '''
    return {
        "steergain":store.steergain,
        "vmin":store.vmin,
        "vmax":store.vmax,
        "mpl":store.mpl,
        "mpr":store.mpr,
        "maxpwm":store.maxpwm,
    }

def alphasettingsmessage():
    ''' state that changes with the robots course settings '''
    return {
        "gpsalpha":store.gpsalpha,
        "magalpha":store.magalpha,
        "declinationalpha":store.declinationalpha,
    }





def magnetometermessage():
    ''' state that changes with the robots course settings '''
    return {
        "magbias":store.magbias,
    }

def accelerometermessage():
    ''' state that changes with the robots course settings '''
    return {
        "accelbias":store.accelbias,
    }

def gyromessage():
    ''' state that changes with the robots course settings '''
    return {
        "gyrobias":store.gyrobias,
    }

def temperaturemessage():
    ''' state that changes with the robots course settings '''
    return {
        "tempoffset":store.tempoffset,
        "tempsensitivity":store.tempsensitivity,
    }