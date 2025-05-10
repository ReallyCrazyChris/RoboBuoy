##################################################### 
# Singleton Store holding the RoboBuoy's state
#####################################################
from math import radians
from lib.utils import normalize

class Store(object):

    _instance = None # is a singleton

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Store()
            cls._instance._initialize()
        return cls._instance

    def _initialize( self ):    
        ####################
        # The RoboBuoy Store 
        ####################
            
        # Information
        self.number = 1         #Mark Number -> 0..255
        self.type = "mark"      #Type of the RoboBupy ['mark','buoy','boat',...]
        self.name = "Einstein"  #Name of the RoboBuoy
        self.color= "green-13"  #Color of the RoboBuoy ['green-13','red-13',...]
        self.mode = "init"      #Current operational mode of the RoboBouy  ['stop','manual','auto',...]
        
        # Battery
        self.battery = 35   # % Capacity of battery remaining

        # Position, Course & Speed
        self.positionvalid = False  # valid gps position
        self.position = ("49.68630810", "10.825340") # tuple of strings (lat,lon) degree decimal 9 digit precision
    
        self.gpscourse = 0      # radians
        self.gpsspeed = 0.0     # knots
        self.magcourse = 0      # magnetic compass cource -> radians -pi..pi
        self.magdeclination = 0 # magnetic compass declinaiton -> radians -pi..pi
        self.currentcourse = 0  # deg° of the current heading -> radians -pi..pi
        
        # AutonomousPathfinding
        self.destination = ("49.68580458", "10.82547235") # (str,str) degree decimal 9 digit precision
        self.distance = 0        # float meters : distance to desired posiiton
        self.desiredcourse = 0   # deg° of the desired heading
        self.waypoints = []      # list of tuples of strings (lat,lon) degree decimal 9 digit precision
        self.waypointarrivedradius = 2 # waypoint arrived radius (meters)
        self.holdgain = 0.5      # This effects the robots speed to a hold waypoint 
        
        # Steering
        # PID tuning gains to control the steering based on desiredcourse vs currentcourse
        self.Kp = 1.0   # proportional gain
        self.Ki = 0     # integral gain
        self.Kd = 0   # derivative gain

        # PID variables to matintain course by steering
        self.error = 0      # error between desired course and current course
        self.errSum = 0     # accumulated error
        self.dErr = 0       # differential error
        self.lastErr = 0    # previous error
        
        # Complimentary Filter : How much trust is given in the GPS and Compass Readings 
        self.gpsalpha = 0.97  # % trust in the gps's course
        self.magalpha = 0.00  # % trust in the compass's course
        self.declinationalpha = 0.00 # % trust in the gps course to calculate the magnetic declination

        # Motor State - never set these directly
        self.surge = 0 # desired robot speed 0..1
        self.steer = 0 # desired robot steering angle -pi..pi
 
        self.vmin = 0  #  minimum robot velocity , constrined to 0..1
        self.vmax = 1  #  maximum robot velocity , constrined to 0..1
        self.minPwmLeft = 3712  #  left pwm value where the motor starts to turn ,0.2ms pulse width (50Hz)
        self.minPwmRight = 3712  #  right pwm value where the motor starts to turn, 0.2ms pulse width (50Hz)      
        self.maxpwm = 6080 #95 # maximum pwm signal sent to the motors, 2.0ms pulse width (50Hz)

        # IMU Constants
        self.accelbias = (0,0,1) # (x,y,z) bias of the accelerometer in g's
        self.gyrobias = (0,0,0) # (x,y,z) bias of the gyroscope in degrees/sec
        self.magbias =  (20.03906, -23.30859, 17.7207, 48.9375, 54.10547, 36.19727, 0.9484222, 0.8578321, 1.282235) 
        self.tempoffset = 0
        self.tempsensitivity = 321 # temperature sensitivity of the IMU in degrees C/LSB

    def update(self,dictionary):
        'utility tp update store values from dictionary'
        for key,value in dictionary.items():
            setattr(self,key,value)  


    # Getters and Setters for the Store variables
    # The getters and setters are used to enforce constraints on the values
    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        ''' number is an integer , constrained  range 0..255'''
        self._number = max(min(int(value),255),0) 

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        ''' type is a string, constrained to 20 characters '''
        self._type = str(value)[:20]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        ''' type is a string, constrained to 50 characters '''
        self._name = str(value)[:50]

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        ''' color is a string, constrained to 20 characters '''
        self._color = str(value)[:20]

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        ''' mode is a string, constrained to 20 characters '''
        self._mode = str(value)[:20]

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        ''' battery is a int, constrained to 0..100 '''
        self._battery = max(min(int(value),100),0) 

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
        ''' position is a tuple of strings (lat,lon) '''
        self._position = tuple(value)[:2]
                              

    @property
    def gpscourse(self):
        return self._gpscourse

    @gpscourse.setter
    def gpscourse(self, value):
        ''' gpscourse in radians, roamlized to -pi..pi '''
        self._gpscourse = normalize(float(value))

    @property
    def gpsspeed(self):
        return self._gpsspeed

    @gpsspeed.setter
    def gpsspeed(self, value):
        ''' gpsspeed in knots, with 2 decimals of precision, constrained to 0..10 '''
        self._gpsspeed =round(max(min(float(value),50),0),2) 

    @property
    def magcourse(self):
        return self._magcourse

    @magcourse.setter
    def magcourse(self, value):
        ''' magcourse in radians, roamlized to -pi..pi '''
        self._magcourse = normalize(float(value))

    @property
    def magdeclination(self):
        return self._magdeclination

    @magdeclination.setter
    def magdeclination(self, value):
        ''' magdeclination in radians, roamlized to -pi..pi '''
        self._magdeclination = normalize(float(value))

    @property
    def currentcourse(self):
        return self._currentcourse

    @currentcourse.setter
    def currentcourse(self, value):
        ''' currentcourse in radians, roamlized to -pi..pi '''
        self._currentcourse = normalize(float(value))

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        ''' destination is a tuple of strings (lat,lon) '''
        self._destination = tuple(value)[:2]

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        ''' distance in meters '''
        # limit the float to 2 decimal places
        self._distance = round(float(value),2)

    @property
    def desiredcourse(self):
        return self._desiredcourse

    @desiredcourse.setter
    def desiredcourse(self, value):
        ''' desiredcourse in radians, normalized to -pi..pi '''
        self._desiredcourse = normalize(float(value))

    @property
    def waypoints(self):
        return self._waypoints

    @waypoints.setter
    def waypoints(self, value):
        ''' waypoints is a list of tuples of strings (lat,lon), constrained to 100 waypoints '''
        self._waypoints = list(value)[:100]

    @property
    def waypointarrivedradius(self):
        return self._waypointarrivedradius

    @waypointarrivedradius.setter
    def waypointarrivedradius(self, value):
        ''' waypointarrivedradius in meters '''
        # limit the float to 2 decimal places
        self._waypointarrivedradius = round(float(value),2)

    @property
    def holdgain(self):
        return self._holdgain

    @holdgain.setter
    def holdgain(self, value):
        ''' holdgain is a float, constrained to 0..1 '''
        self._holdgain = max(min(float(value),1),0)

    @property
    def Kp(self):
        return self._Kp

    @Kp.setter
    def Kp(self, value):
        #TODO apply constraints
        self._Kp = float(value)

    @property
    def Ki(self):
        return self._Ki

    @Ki.setter
    def Ki(self, value):
        #TODO apply constraints
        self._Ki = float(value)

    @property
    def Kd(self):
        return self._Kd

    @Kd.setter
    def Kd(self, value):
        #TODO apply constraints
        self._Kd = float(value)

    @property
    def gpsalpha(self):
        return self._gpsalpha

    @gpsalpha.setter
    def gpsalpha(self, value):
        self._gpsalpha = max(min(float(value),1),0)

    @property
    def magalpha(self):
        return self._magalpha

    @magalpha.setter
    def magalpha(self, value):
        self._magalpha = max(min(float(value),1),0)

    @property
    def declinationalpha(self):
        return self._declinationalpha

    @declinationalpha.setter
    def declinationalpha(self, value):
        self._declinationalpha = max(min(float(value),1),0)

    @property
    def surge(self):
        return self._surge

    @surge.setter
    def surge(self, value):     
        # constrain value range to 0..1
        self._surge = max(min(float(value),1),0) 

    @property
    def steer(self):
        return self._steer

    @steer.setter
    def steer(self, value):
        ''' steer in radians, normalized to -pi..pi '''
        self._steer = normalize(float(value))


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
    def minPwmLeft(self):
        return self._mpl

    @minPwmLeft.setter
    def minPwmLeft(self, value):
        self._mpl = int(value)

    @property
    def minPwmRight(self):
        return self._mpr

    @minPwmRight.setter
    def minPwmRight(self, value):
        self._mpr = int(value)

    @property
    def maxpwm(self):
        return self._maxpwm

    @maxpwm.setter
    def maxpwm(self, value):
        self._maxpwm = int(value)



    ''' set functions with values from an external application '''
    def set_number(self, value):
        self.number = int(value)

    def set_type(self, value):
        self.type = str(value)

    def set_name(self, value):
        self.name = str(value)

    def set_color(self, value):
        self.color = str(value)

    def set_mode(self, value):
        self.mode = str(value)

    def set_battery(self, value):
        self.battery = float(value)

    def set_positionvalid(self, value):
        self.positionvalid = bool(value)

    def set_position(self, value):
        self.position = tuple(value)

    def set_gpscourse(self, value):
        self.gpscourse = float(radians(value))

    def set_gpsspeed(self, value):
        self.gpsspeed = float(value)

    def set_magcourse(self, value):
        self.magcourse = float(radians(value))

    def set_magdeclination(self, value):
        self.magdeclination = float(radians(value))

    def set_currentcourse(self, value):
        self.currentcourse = float(radians(value))

    def set_destination(self, value):
        self.destination = str(value)

    def set_distance(self, value):
        self.distance = float(value)

    def set_desiredcourse(self, value):
        self.desiredcourse = float(radians(value))

    def set_waypoints(self, value):
        self.waypoints = value

    def set_waypointarrivedradius(self, value):
        self.waypointarrivedradius = float(value)

    def set_holdgain(self, value):
        self.holdgain = float(value)        

    def set_Kp(self, value):
        self.Kp = float(value)

    def set_Ki(self, value):
        self.Ki = float(value)

    def set_Kd(self, value):
        self.Kd = float(value)

    def seterror(self, value):
        self.rror = float(value)

    def seterrSum(self, value):
        self.rrSum = float(value)

    def setdErr(self, value):
        self.Err = float(value)

    def setlastErr(self, value):
        self.astErr = float(value)

    def set_gpsalpha(self, value):
        self.gpsalpha = float(value)

    def set_magalpha(self, value):
        self.magalpha = float(value)

    def set_declinationalpha(self, value):
        self.declinationalpha = float(value)

    def set_surge(self, value):
        self.surge = float(value)

    def set_steer(self, value):
        ''' value in degrees converted to float radians '''
        self.steer = float(radians(value))

        
    def set_vmin(self, value):
        ''' set vmin to a value between 0 and 1 '''
        self.vmin = max(min(float(value),1),0) 

    def set_vmax(self, value):
        ''' set vmax to a value between 0 and 1 '''
        self.vmax = max(min(float(value),1),0) 

    def set_mpl(self, value):
        ''' set minPwmLeft to a value between 0 and 65535 '''
        self.minPwmLeft = max(min(int(value),65535),0)

    def set_mpr(self, value):
        ''' set minPwmRight to a value between 0 and 65535 '''
        self.minPwmRight = max(min(int(value),65535),0)

    def set_maxpwm(self, value):
        ''' set maxpwm to a value between 0 and 65535 '''
        self.maxpwm = max(min(int(value),65535),0)