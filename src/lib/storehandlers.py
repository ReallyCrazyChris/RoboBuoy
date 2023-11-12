##################################################### 
# RoboBouyAPP calls these update / action handlers 
#####################################################
from lib import server
from lib.storepersistance import savesettings, loadsettings
from lib.store import Store
store = Store()

# Actions Handlers
server.addListener('savesettings',savesettings)
server.addListener('loadsettings',loadsettings)

# Update Handlers
server.addListener('number', store.set_number)
server.addListener('type', store.set_type)
server.addListener('name', store.set_name)
server.addListener('color', store.set_color)
#server.addListener('mode', store.set_mode)
server.addListener('battery', store.set_battery)
server.addListener('positionvalid', store.set_positionvalid)
server.addListener('position', store.set_position)
server.addListener('gpscourse', store.set_gpscourse)
server.addListener('gpsspeed', store.set_gpsspeed)
server.addListener('magcourse', store.set_magcourse)
server.addListener('magdeclination', store.set_magdeclination)
server.addListener('currentcourse', store.set_currentcourse)
server.addListener('destination', store.set_destination)
server.addListener('distance', store.set_distance)
server.addListener('dc', store.set_desiredcourse)
server.addListener('wp', store.set_waypoints)
server.addListener('wr', store.set_waypointarrivedradius)
server.addListener('Kp', store.set_Kp)
server.addListener('Ki', store.set_Ki)
server.addListener('Kd', store.set_Kd)
#server.addListener('error', store.set_error)
#server.addListener('errSum', store.set_errSum)
#server.addListener('dErr', store.set_dErr)
#server.addListener('lastErr', store.set_lastErr)
server.addListener('gpsalpha', store.set_gpsalpha)
server.addListener('magalpha', store.set_magalpha)
server.addListener('declinationalpha', store.set_declinationalpha)
server.addListener('surge', store.set_surge)
server.addListener('steer', store.set_steer)
server.addListener('vmin', store.set_vmin)
server.addListener('vmax', store.set_vmax)
server.addListener('steergain', store.set_steergain)
server.addListener('mpl', store.set_mpl)
server.addListener('mpr', store.set_mpr)
server.addListener('maxpwm', store.set_maxpwm)