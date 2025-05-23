##################################################### 
# Persist and Hydrate the RobotBouys State from files
#####################################################
from lib.events import on
from storage.store import Store
store = Store.instance()

def persistedstate():
    ''' state that is to be persisted '''
    return {
        "accelbias": store.accelbias,
        "declinationalpha": store.declinationalpha,
        "gpsalpha": store.gpsalpha,
        "gyroalpha": store.gyroalpha,
        "gyrobias": store.gyrobias,
        "holdradius": store.holdradius,
        "Kd": store.Kd,
        "Ki": store.Ki,
        "Kp": store.Kp,
        "magalpha": store.magalpha,
        "magbias": store.magbias,
        "magdeclination": store.magdeclination,
        "maxpwm": store.maxpwm,
        "minPwmLeft": store.minPwmLeft,
        "minPwmRight": store.minPwmRight,
        "tempoffset": store.tempoffset,
        "tempsensitivity": store.tempsensitivity,
        "vmax": store.vmax,
        "vmin": store.vmin,
        "waypointarrivedradius": store.waypointarrivedradius,
        "waypoints": store.waypoints,
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
        print('settings.json not found')
        pass


on('savesettings',savesettings)
on('loadsettings',loadsettings)