##################################################### 
# Singleton Store holing the  RoboBuoy's State
#####################################################

class Store(object):

    _instance = None # is a singleton
    
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__( self ):
        
        ####################
        # The RoboBuoy Store 
        ####################
            
        # Information
        self.number = 1     #Mark Number
        self.type = "mark"
        self.name = "Einstein"  #Name of the RoboBupy in the APP
        self.color= "green-13" #Primary Color of the Mark Chartreuse
        self.mode = "stop"  #Current operational mode of the RoboBouy  ['stop','manual','auto',...]
        # Battery
        self.battery = 35   # % Capacity of battery remaining
        # Position, Course & Speed
        self.positionvalid = False  # valid gps position
        self.position = ("49.68630810", "10.825340") # string degree decimal 
    
        self.gpscourse = 0      # degrees
        self.gpsspeed = 0.0     # knots
        self.magcourse = 0      # magnetic compass cource
        self.magdeclination = 0 # magnetic compass declinaiton
        self.currentcourse = 0  # deg° of the current heading
        # AutonomousPathfinding
        self.destination = ("49.68580458", "10.82547235") # (str,str) degree decimal 9 digit precision
        self.distance = 0        # float meters : distance to desired posiiton
        self.desiredcourse = 0   # deg° of the desired heading
        self.waypoints = []      # [(str,str)] degree decimal 9 digit precision
        self.waypointarrivedradius = 2 # waypoint arrived radius (meters)
        # Steering
        # PID tuning gains to control the steering based on desiredcourse vs currentcourse
        self.Kp = 1
        self.Ki = 0 
        self.Kd = 0.5 
        # PID variables to matintain course by steering
        self.error = 0
        self.errSum = 0
        self.dErr = 0      
        self.lastErr = 0  # Previous error
        
        # Complimentary Filter : How much trust is given in the GPS and Compass Readings 
        self.gpsalpha = 0.97  # % trust in the gps course
        self.magalpha = 0.00  # % trust in the compass course
        self.declinationalpha = 0.00 # % we trust in the gps to calculate the magnetic declination
        # Motor State - never set these directly
        self.surge = 0 #  desired robot speed cm/s
        self.steer = 0 #  desired robot angualr rotation deg/s
        self.vmin = 0  #  minimum robot velocity cm/s
        self.vmax = 20 #  maximum robot velocity cm/s
        self.mpl = 53  #  left pwm value where the motor starts to turn
        self.mpr = 55  #  right pwm value where the motor starts to turn
        self.maxpwm = 110 # maximum pwm signal sent to the motors

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = int(value)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = str(value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = str(value)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = str(value)

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        self._battery = int(value)

    @property
    def positionvalid(self):
        return self._positionvalid

    @positionvalid.setter
    def positionvalid(self, value):
        self._positionvalid = bool(value)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = tuple(value)
                              

    @property
    def gpscourse(self):
        return self._gpscourse

    @gpscourse.setter
    def gpscourse(self, value):
        self._gpscourse = int(value)

    @property
    def gpsspeed(self):
        return self._gpsspeed

    @gpsspeed.setter
    def gpsspeed(self, value):
        # limit the float to 2 decimal places
        # its easier to present and higher precisio is not required
        self._gpsspeed = round(float(value),2)

    @property
    def magcourse(self):
        return self._magcourse

    @magcourse.setter
    def magcourse(self, value):
        self._magcourse = int(value)

    @property
    def magdeclination(self):
        return self._magdeclination

    @magdeclination.setter
    def magdeclination(self, value):
        self._magdeclination = int(value)

    @property
    def currentcourse(self):
        return self._currentcourse

    @currentcourse.setter
    def currentcourse(self, value):
        self._currentcourse = int(value)

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = tuple(value)

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        self._distance = float(value)

    @property
    def desiredcourse(self):
        return self._desiredcourse

    @desiredcourse.setter
    def desiredcourse(self, value):
        self._desiredcourse = int(value)

    @property
    def waypoints(self):
        return self._waypoints

    @waypoints.setter
    def waypoints(self, value):
        self._waypoints = list(value)

    @property
    def waypointarrivedradius(self):
        return self._waypointarrivedradius

    @waypointarrivedradius.setter
    def waypointarrivedradius(self, value):
        self._waypointarrivedradius = int(value)

    @property
    def Kp(self):
        return self._Kp

    @Kp.setter
    def Kp(self, value):
        self._Kp = float(value)

    @property
    def Ki(self):
        return self._Ki

    @Ki.setter
    def Ki(self, value):
        self._Ki = float(value)

    @property
    def Kd(self):
        return self._Kd

    @Kd.setter
    def Kd(self, value):
        self._Kd = float(value)

    @property
    def gpsalpha(self):
        return self._gpsalpha

    @gpsalpha.setter
    def gpsalpha(self, value):
        self._gpsalpha = float(value)

    @property
    def magalpha(self):
        return self._magalpha

    @magalpha.setter
    def magalpha(self, value):
        self._magalpha = float(value)

    @property
    def declinationalpha(self):
        return self._declinationalpha

    @declinationalpha.setter
    def declinationalpha(self, value):
        self._declinationalpha = float(value)

    @property
    def surge(self):
        return self._surge

    @surge.setter
    def surge(self, value):
        self._surge = int(value)

    @property
    def steer(self):
        return self._steer

    @steer.setter
    def steer(self, value):
        self._steer = int(value)


    @property
    def vmin(self):
        return self._vmin

    @vmin.setter
    def vmin(self, value):
        self._vmin = int(value)


    @property
    def vmax(self):
        return self._vmax

    @vmax.setter
    def vmax(self, value):
        self._vmax = int(value)

    @property
    def steergain(self):
        return self._steergain

    @steergain.setter
    def steergain(self, value):
        self._steergain = int(value)

    @property
    def mpl(self):
        return self._mpl

    @mpl.setter
    def mpl(self, value):
        self._mpl = int(value)

    @property
    def mpr(self):
        return self._mpr

    @mpr.setter
    def mpr(self, value):
        self._mpr = int(value)

    @property
    def maxpwm(self):
        return self._maxpwm

    @maxpwm.setter
    def maxpwm(self, value):
        self._maxpwm = int(value)


    def set_number(self, value):
        self.number = value

    def set_type(self, value):
        self.type = value

    def set_name(self, value):
        self.name = value

    def set_color(self, value):
        self.color = value

    def set_mode(self, value):
        self.mode = value

    def set_battery(self, value):
        self.battery = value

    def set_positionvalid(self, value):
        self.positionvalid = value

    def set_position(self, value):
        self.position = value

    def set_gpscourse(self, value):
        self.gpscourse = value

    def set_gpsspeed(self, value):
        self.gpsspeed = value

    def set_magcourse(self, value):
        self.magcourse = value

    def set_magdeclination(self, value):
        self.magdeclination = value

    def set_currentcourse(self, value):
        self.currentcourse = value

    def set_destination(self, value):
        self.destination = value

    def set_distance(self, value):
        self.distance = value

    def set_desiredcourse(self, value):
        self.desiredcourse = value

    def set_waypoints(self, value):
        self.waypoints = value

    def set_waypointarrivedradius(self, value):
        self.waypointarrivedradius = value

    def set_Kp(self, value):
        self.Kp = value

    def set_Ki(self, value):
        self.Ki = value

    def set_Kd(self, value):
        self.Kd = value

    def seterror(self, value):
        self.rror = value

    def seterrSum(self, value):
        self.rrSum = value

    def setdErr(self, value):
        self.Err = value

    def setlastErr(self, value):
        self.astErr = value

    def set_gpsalpha(self, value):
        self.gpsalpha = value

    def set_magalpha(self, value):
        self.magalpha = value

    def set_declinationalpha(self, value):
        self.declinationalpha = value

    def set_surge(self, value):
        self.surge = value

    def set_steer(self, value):
        self.steer = value

    def set_vmin(self, value):
        self.vmin = value

    def set_vmax(self, value):
        self.vmax = value

    def set_steergain(self, value):
        self.steergain = value

    def set_mpl(self, value):
        self.mpl = value

    def set_mpr(self, value):
        self.mpr = value

    def set_maxpwm(self, value):
        self.maxpwm = value