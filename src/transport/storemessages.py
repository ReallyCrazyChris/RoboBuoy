##################################################### 
# Messages that update RoboBuoyAPP State
#####################################################

from math import degrees
from storage.store import Store
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
        "gpsheading":int(degrees(store.gpsheading)),
        "gpsspeed":store.gpsspeed,
        "magheading":int(degrees(store.magheading)),
        "magdeclination":int(degrees(store.magdeclination)),
        "heading":int(degrees(store.heading)),
        "destination":store.destination,
        "distance":store.distance,
        "course":int(degrees(store.course)),
        "waypoints":store.waypoints,
        "waypointarrivedradius":store.waypointarrivedradius,
        "holdradius":store.holdradius,
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
        "gyroalpha":store.gyroalpha,
        "surge":store.surge,
        "steer":int(degrees(store.steer)),
        #"steergain":store.steergain,
        "vmin":store.vmin,
        "vmax":store.vmax,
        "minPwmLeft":store.minPwmLeft,
        "minPwmRight":store.minPwmRight,
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
        "gpsheading":int(degrees(store.gpsheading)),
        "gpsspeed":store.gpsspeed,
        "magheading":int(degrees(store.magheading)),
        "magdeclination":int(degrees(store.magdeclination)),
    }

def statemessage_chunk3():
    ''' state that changes when the robot is initalized '''
    return {
        "heading":int(degrees(store.heading)),
        "destination":store.destination,
        "distance":store.distance,
        "course":int(degrees(store.course)),
    }

def statemessage_chunk4():
    ''' state that changes when the robot is initalized '''
    return {
        "waypoints":store.waypoints,
        "waypointarrivedradius":store.waypointarrivedradius,
        "holdradius":store.holdradius,
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
        "gyroalpha":store.gyroalpha,
        "surge":store.surge,
        "steer":int(degrees(store.steer)),
        #"steergain":store.steergain,
    }

def statemessage_chunk7():
    ''' state that changes when the robot is initalized '''
    return {
        "vmin":store.vmin,
        "vmax":store.vmax,
        "minPwmLeft":store.minPwmLeft,
        "minPwmRight":store.minPwmRight,
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
        "gpsheading":int(degrees(store.gpsheading)),
        "gpsspeed":store.gpsspeed,
        "magheading":int(degrees(store.magheading)),
        "magdeclination":int(degrees(store.magdeclination)),
        "heading":int(degrees(store.heading)),
        #"destination":store.destination,
        #"distance":store.distance,
        "course":int(degrees(store.course)),
        #"waypoints":store.waypoints,
        #"waypointarrivedradius":store.waypointarrivedradius,
        #"holdradius":store.holdradius,
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
        #"steer":int(degrees(store.steer)),
        #"steergain":store.steergain,
        #"vmin":store.vmin,
        #"vmax":store.vmax,
        #"minPwmLeft":store.minPwmLeft,
        #"minPwmRight":store.minPwmRight,
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
        "gpsheading":int(degrees(store.gpsheading)),
        "gpsspeed":store.gpsspeed,
        "magheading":int(degrees(store.magheading)),
        "magdeclination":int(degrees(store.magdeclination)),
        "heading":int(degrees(store.heading)),
        #"destination":store.destination,
        #"distance":store.distance,
        "course":int(degrees(store.course)),
        #"waypoints":store.waypoints,
        #"waypointarrivedradius":store.waypointarrivedradius,
        #"holdradius":store.holdradius,
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
        #"minPwmLeft":store.minPwmLeft,
        #"minPwmRight":store.minPwmRight,
        #"maxpwm":store.maxpwm,
    }


def holdsettingsmessage():
    ''' configuraiton parameters for holding station'''
    return {
        "waypointarrivedradius":store.waypointarrivedradius,
        "holdradius":store.holdradius,
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
        #"steergain":store.steergain,
        "vmin":store.vmin,
        "vmax":store.vmax,
        "minPwmLeft":store.minPwmLeft,
        "minPwmRight":store.minPwmRight,
        "maxpwm":store.maxpwm,
    }

def alphasettingsmessage():
    ''' state that changes with the robots course settings '''
    return {
        "gpsalpha":store.gpsalpha,
        "magalpha":store.magalpha,
        "declinationalpha":store.declinationalpha,
        "gyroalpha":store.gyroalpha,
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