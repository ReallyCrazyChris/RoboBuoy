##################################################### 
# RoboBouyAPP calls these update / action handlers 
#####################################################
from lib.events import on
from lib.store import Store
store = Store.instance()

# Update Handlers
on('number', store.set_number)
on('type', store.set_type)
on('name', store.set_name)
on('color', store.set_color)
#on('mode', store.set_mode) // handled in states
on('battery', store.set_battery)
on('positionvalid', store.set_positionvalid)
on('position', store.set_position)
on('gpscourse', store.set_gpscourse)
on('gpsspeed', store.set_gpsspeed)
on('magcourse', store.set_magcourse)
on('magdeclination', store.set_magdeclination)
on('currentcourse', store.set_currentcourse)
on('destination', store.set_destination)
on('distance', store.set_distance)
on('dc', store.set_desiredcourse)
on('wp', store.set_waypoints)
on('wr', store.set_waypointarrivedradius)
on('Kp', store.set_Kp)
on('Ki', store.set_Ki)
on('Kd', store.set_Kd)
on('gpsalpha', store.set_gpsalpha)
on('magalpha', store.set_magalpha)
on('declinationalpha', store.set_declinationalpha)
on('surge', store.set_surge)
on('steer', store.set_steer)
on('vmin', store.set_vmin)
on('vmax', store.set_vmax)
on('mpl', store.set_mpl)
on('mpr', store.set_mpr)
on('maxpwm', store.set_maxpwm)