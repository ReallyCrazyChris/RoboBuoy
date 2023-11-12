##################################################### 
# Persist and Hydrate the RobotBouys State from files
#####################################################
from lib.store import Store
store = Store()

def persistedstate():
    ''' state that is to be persisted '''
    return {
        "number":store.number,
        "type":store.type,
        "name":store.name,
        "color":store.color,
        #"mode":store.mode,
        #"battery":store.battery,
        #"positionvalid":store.positionvalid,
        #"position":store.position,
        #"gpscourse":store.gpscourse,
        #"gpsspeed":store.gpsspeed,
        #"magcourse":store.magcourse,
        "magdeclination":store.magdeclination,
        #"currentcourse":store.currentcourse,
        #"destination":store.destination,
        #"distance":store.distance,
        #"desiredcourse":store.desiredcourse,
        "waypoints":store.waypoints,
        "waypointarrivedradius":store.waypointarrivedradius,
        "Kp":store.Kp,
        "Ki":store.Ki,
        "Kd":store.Kd,
        #"error":store.error,
        #"errSum":store.errSum,
        #"Err":store.Err,
        #"lastErr":store.lastErr,
        "gpsalpha":store.gpsalpha,
        "magalpha":store.magalpha,
        "declinationalpha":store.declinationalpha,
        #"surge":store.surge,
        #"steer":store.steer,
        "vmin":store.vmin,
        "vmax":store.vmax,
        "steergain":store.steergain,
        "mpl":store.mpl,
        "mpr":store.mpr,
        "maxpwm":store.maxpwm,
    }

def savesettings():
    """write persistedstate to flash"""
    import json
    with open('settings.json', 'w') as file:
        json.dump(persistedstate(), file)

def loadsettings():
    """load persistedstate from flash"""
    import json
    try:
        with open('settings.json', 'r') as file:
            settings = json.load(file) 
            #TODO I am not sure this is working together with the @propery approach in the Store
            store.__dict__.update(settings)
    except Exception :
        pass