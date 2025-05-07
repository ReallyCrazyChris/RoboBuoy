##################################################### 
# Persist and Hydrate the RobotBouys State from files
#####################################################
from lib.events import on
from lib.store import Store
store = Store.instance()

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
        "holdgain":store.holdgain,
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
        #"steergain":store.steergain,
        "vmin":store.vmin,
        "vmax":store.vmax,
        "minPwmLeft":store.minPwmLeft,
        "minPwmRight":store.minPwmRight,
        "maxpwm":store.maxpwm,
        "accelbias":store.accelbias, 
        "gyrobias":store.gyrobias,
        "magbias":store.magbias,
        "tempoffset":store.tempoffset, 
        "tempsensitivity":store.tempsensitivity,
    }

def savesettings():
    '''write persistedstate to flash'''
    import json
    with open('settings.json', 'w') as file:
        json.dump(persistedstate(), file)
        print('settings saved')

def loadsettings():
    '''load persistedstate from flash'''
    import json
    try:
        with open('settings.json', 'r') as file:
            settings = json.load(file) 
            store.update(settings)
            print('settings loaded')
    except Exception:
        pass


on('savesettings',savesettings)
on('loadsettings',loadsettings)