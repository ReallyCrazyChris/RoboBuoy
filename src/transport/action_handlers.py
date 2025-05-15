from math import radians
from lib.events import on
from storage.store import Store
store = Store.instance()

# bind action to handler
def bind_actions_to_handlers():
    on('number', set_number)
    on('type', set_type)
    on('name', set_name)
    on('color', set_color)
    on('battery', set_battery)
    on('positionvalid', set_positionvalid)
    on('position', set_position)
    on('gpscourse', set_gpscourse)
    on('gpsspeed', set_gpsspeed)
    on('magcourse', set_magcourse)
    on('magdeclination', set_magdeclination)
    on('currentcourse', set_currentcourse)
    on('destination', set_destination)
    on('distance', set_distance)
    on('dc', set_desiredcourse)
    on('wp', set_waypoints)
    on('wr', set_waypointarrivedradius)
    on('holdgain', set_holdgain)
    on('Kp', set_Kp)
    on('Ki', set_Ki)
    on('Kd', set_Kd)
    on('gpsalpha', set_gpsalpha)
    on('magalpha', set_magalpha)
    on('declinationalpha', set_declinationalpha)
    on('gyroalpha', set_gyroalpha)

    on('surge', set_surge)
    on('steer', set_steer)
    #on('steergain', set_steergain)
    on('vmin', set_vmin)
    on('vmax', set_vmax)
    on('minPwmLeft', set_mpl)
    on('minPwmRight', set_mpr)
    on('maxpwm', set_maxpwm)  

# action handlers
def set_number(value):
    store.number = int(value)            

def set_type(value):
    store.type = str(value)

def set_name(value):
    store.name = str(value)

def set_color(value):
    store.color = str(value)

def set_mode(value):
    store.mode = str(value)

def set_battery(value):
    store.battery = float(value)

def set_positionvalid(value):
    store.positionvalid = bool(value)

def set_position(value):
    store.position = tuple(value)

def set_gpscourse(value):
    store.gpscourse = float(radians(value))

def set_gpsspeed(value):
    store.gpsspeed = float(value)

def set_magcourse(value):
    store.magcourse = float(radians(value))

def set_magdeclination(value):
    store.magdeclination = float(radians(value))

def set_currentcourse(value):
    store.currentcourse = float(radians(value))

def set_destination(value):
    store.destination = str(value)

def set_distance(value):
    store.distance = float(value)

def set_desiredcourse(value):
    store.desiredcourse = float(radians(value))

def set_waypoints(value):
    store.waypoints = value

def set_waypointarrivedradius(value):
    store.waypointarrivedradius = float(value)

def set_holdgain(value):
    store.holdgain = float(value)        

def set_Kp(value):
    store.Kp = float(value)

def set_Ki(value):
    store.Ki = float(value)

def set_Kd(value):
    store.Kd = float(value)

def seterror(value):
    store.rror = float(value)

def seterrSum(value):
    store.rrSum = float(value)

def setdErr(value):
    store.Err = float(value)

def setlastErr(value):
    store.astErr = float(value)

def set_gpsalpha(value):
    store.gpsalpha = float(value)

def set_magalpha(value):
    store.magalpha = float(value)

def set_declinationalpha(value):
    store.declinationalpha = float(value)

def set_gyroalpha(value):
    store.gyroalpha = float(value)

def set_surge(value):
    store.surge = float(value)

def set_steer(value):
    ''' value in degrees converted to float radians '''
    store.steer = float(radians(value))

    
def set_vmin(value):
    ''' set vmin to a value between 0 and 1 '''
    store.vmin = max(min(float(value),1),0) 

def set_vmax(value):
    ''' set vmax to a value between 0 and 1 '''
    store.vmax = max(min(float(value),1),0) 

def set_mpl(value):
    ''' set minPwmLeft to a value between 0 and 65535 '''
    store.minPwmLeft = max(min(int(value),65535),0)

def set_mpr(value):
    ''' set minPwmRight to a value between 0 and 65535 '''
    store.minPwmRight = max(min(int(value),65535),0)

def set_maxpwm(value):
    ''' set maxpwm to a value between 0 and 65535 '''
    store.maxpwm = max(min(int(value),65535),0)


 