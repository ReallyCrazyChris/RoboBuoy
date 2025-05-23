from math import radians
from lib.events import on
from storage.store import Store
store = Store.instance()

def bind_actions_to_handlers():
    '''bind actions to handlers'''
    on('magdeclination', set_magdeclination)
    on('destination', set_destination)
    on('dc', set_course)
    on('wp', set_waypoints)
    on('wr', set_waypointarrivedradius)
    on('holdradius', set_holdradius)
    on('Kp', set_Kp)
    on('Ki', set_Ki)
    on('Kd', set_Kd)
    on('gpsalpha', set_gpsalpha)
    on('magalpha', set_magalpha)
    on('declinationalpha', set_declinationalpha)
    on('gyroalpha', set_gyroalpha)
    on('surge', set_surge)
    on('steer', set_steer)
    on('vmin', set_vmin)
    on('vmax', set_vmax)
    on('minPwmLeft', set_minpwmleft)
    on('minPwmRight', set_minpwmright)
    on('maxpwm', set_maxpwm)  

# action handlers
def set_mode(value):
    store.mode = str(value)



def set_magdeclination(value):
    store.magdeclination = float(radians(value))

def set_destination(value):
    store.destination = str(value)

def set_course(value):
    store.course = float(radians(value))

def set_waypoints(value):
    store.waypoints = value

def set_waypointarrivedradius(value):
    store.waypointarrivedradius = float(value)

def set_holdradius(value):
    store.holdradius = float(value)        

def set_Kp(value):
    store.Kp = float(value)

def set_Ki(value):
    store.Ki = float(value)

def set_Kd(value):
    store.Kd = float(value)

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

def set_minpwmleft(value):
    ''' set minPwmLeft to a value between 0 and 65535 '''
    store.minPwmLeft = max(min(int(value),65535),0)

def set_minpwmright(value):
    ''' set minPwmRight to a value between 0 and 65535 '''
    store.minPwmRight = max(min(int(value),65535),0)

def set_maxpwm(value):
    ''' set maxpwm to a value between 0 and 65535 '''
    store.maxpwm = max(min(int(value),65535),0)


 