import time #TODO try to use asyncio on arm motors
import uasyncio as asyncio
from machine import PWM, Pin
from math import floor, ceil, radians, sin, cos, sqrt, degrees, atan2
from lib.server import Server

server = Server()

class Controller():
    def __init__(self):

        # Robot Information
        self.name = "Buoy 1"
        self.battery = 63 # % Capacity of Battery Remaining


        # Thruster Control
        self.active = False # enables / disbles the thrusters
        self.surge = 0 #  desired robot speed cm/s
        self.steer = 0 #  desired robot angualr rotation deg/s
        self.vmin = 0  #  minimum robot velocity cm/s
        self.vmax = 50 #  maximum robot velocity cm/s
        self.steergain = 100 # steering gain
        self.mpl = 53  #  left pwm value where the thruster start to turn
        self.mpr = 55  #  right pwm value where the thruster start to turn
        self.maxpwm = 110 # maximum pwm signal sent to the thrusters

        # Position/Motion
        self.positionvalid = False
        self.latitude = 0 # degree decimal north
        self.longitude = 0 # degree decimal east
        self.latitude_string = '' # degree decimal north 24 bit precision, 
        self.longitude_string = ''# degree decimal east 24 bit precision
        self.speed = 0.0  #meters per second

        # Pathfinding
        self.currentcourse = 0 # deg° of the current heading
        self.desiredcourse = 0 # deg° of the desired heading
        self.currentposition = (0,0) # degree decimal north, degree decimal east
        self.desiredposition = (0,0) # degree decimal north, degree decimal east
        self.distance = 0 # float meters : distance to desired posiiton
        self.waypoints = [] # array of positions
        self.waypointradius = 2 # the radial distance in meters of a waypoint

        
        # Steering
        # PID tuning gains to control the steering based on desiredcourse vs currentcourse
        self.Kp = 1
        self.Ki = 0 #.5
        self.Kd = 0.5 #.0001

        # PID variables to matintain course by steering
        self.error = 0
        self.errSum = 0
        self.dErr = 0      
        self.lastErr = 0  # Previous error

        # Complimentary Filter tunings
        self.compassalpha = 0.97  # compasComplemt filter weighted towards the gyro
        self.gpsalpha = 0.03      # gpsComplement  filter weighted towards the gps

        # PWM control of ESC motor controlers 
        self.motorLeft  = PWM(Pin(16))
        self.motorRight = PWM(Pin(17))
        self.motorLeft.freq(50)
        self.motorRight.freq(50)

        # Communication with RoboBuoyApp
        # add commands and their handlers to the server
        server.addListener('state',self.sendstate)
        server.addListener('motion',self.sendmotionstate)

        #thruster parameters 
        server.addListener('arm',self.armmotors)
        server.addListener('active',self.setactive)
        server.addListener('surge',self.setsurge)
        server.addListener('steer',self.setsteer)
        server.addListener('stop',self.stop)
        server.addListener('vmin', self.setvmin)
        server.addListener('vmax', self.setvmax)
        server.addListener('sgain', self.setsteergain)
        server.addListener('mpl',self.setmpl)
        server.addListener('mpr',self.setmpr)

        #steering parameters    
        server.addListener('cc',self.setcurrentcourse)
        server.addListener('dc',self.setdesiredcourse)
        server.addListener('Kp',self.setKp)
        server.addListener('Ki',self.setKi)
        server.addListener('Kd',self.setKd)
        server.addListener('ca',self.setcompassalpha)
        server.addListener('ga',self.setgpsalpha)
        # save or load relevant state from file store

        # pathfinding
        server.addListener('wp',self.setwaypoints)
        server.addListener('reset',self.resetcourse)

        server.addListener('save',self.savestate)
        server.addListener('load',self.loadstate)

    def sendstate(self,_):
        ''' a request, that responds with the robot state'''
        state = {
            "name":self.name,
            "active":self.active, 
            "surge":self.surge, 
            "steer":self.steer, 
            "vmin":self.vmin, 
            "vmax":self.vmax, 
            "steergain":self.steergain, 
            "mpl":self.mpl, 
            "mpr":self.mpr, 
            "maxpwm":self.maxpwm, 
            "desiredcourse":self.desiredcourse, 
            "currentcourse":self.currentcourse, 
            "Kp":self.Kp, 
            "Ki":self.Ki, 
            "Kd":self.Kd, 
            "compassalpha":self.compassalpha, 
            "gpsalpha":self.gpsalpha, 
        }

        server.send('state',state)

    def sendmotionstate(self):
        ''' a request, that responds with the robot motion'''
        state = {
            #"battery":int(self.battery),
            #"positionvalid":self.positionvalid,
            #"active":self.active, 
            "speed":int(self.speed), 
            "currentcourse":int(self.currentcourse), 
            "desiredcourse":int(self.desiredcourse), 
            "currentposition":self.currentposition,
            #"waypoints":self.waypoints,
            "distance":self.distance,
            "surge":int(self.surge), 
            "steer":int(self.steer)
        }

        server.send('state',state)        

    def setactive(self, val):
        self.active = bool(val)  
        print('active',self.active) 
        self.drive()

    def setsurge(self, val):
        self.surge = int(val)
        self.drive() 
        print('surge',self.surge)
        
    def setsteer(self, val):
        self.steer = int(val)  
        self.drive()    
        print('steer',self.steer)
        

    def setvmin(self, val):
        self.vmin = int(val)
        print('vmin (cm/s)',self.vmin)

    def setvmax(self, val):
        self.vmax = int(val)
        self.drive() 
        print('vmax (cm/s)',self.vmax) 

    def setsteergain(self, val):
        self.steergain = int(val)
        self.drive()
        print('steergain',self.steergain)

    def setmpl(self, val):
        self.mpl = int(val)  
        self.surge = 1
        self.steer = 0
        self.drive()
        print('mpl',self.mpl)

    def setmpr(self, val):
        self.mpr = int(val)  
        self.surge = 1
        self.steer = 0
        self.drive()
        print('mpr',self.mpr)    

    def setwaypoints(self,val):
        self.waypoints = val
        print('waypoints',self.waypoints)

    def setcurrentcourse(self, val):
        self.currentcourse = int(val) 
        print('currentcourse',self.currentcourse)
    
    def setdesiredcourse (self,val):
        self.desiredcourse = int(val) 
        print('desiredcourse',self.desiredcourse)

    def setKp (self,Kp):
        self.Kp = float(Kp) 
        print('Kp',self.Kp)

    def setKi (self,Ki):
        self.Ki = float(Ki) 
        print('Ki',self.Ki)

    def setKd (self,Kd):
        self.Kd = float(Kd) 
        print('Kd',self.Kd)       
        
    def setcompassalpha (self,val):
        self.compassalpha = float(val) 
        print('compassalpha',self.compassalpha)

    def setgpsalpha (self,val):
        self.gpsalpha = float(val) 
        print('gpsalpha',self.gpsalpha)


    # actual controller part

    def fusegyro(self,gyro_deg_s,deltaT ):
        '''integrates the gyro rate of yaw (deg_s) into a course angle (deg)'''
        currentcourse = ( self.currentcourse + gyro_deg_s * deltaT )
        # clamp to -180 ... 180 degrees
        self.currentcourse = normalize(currentcourse,-180,180)
        
        return self.currentcourse

    def fusecompass(self, compasscourse):
        '''fuses the compass course witht he current course using a complement filter, strongly weighted towards the gyro'''
        currentcourse = (1.0 - self.compassalpha) * compasscourse + self.compassalpha * self.currentcourse
        # clamp to -180 ... 180 degrees
        self.currentcourse = normalize(currentcourse,-180,180)

        return self.currentcourse

    def fusegps(self, gpscourse):
        '''fuses the gps course with the currentcourse using a complement filter, strongly weighted towards the gps'''
        currentcourse = (1.0 - self.gpsalpha) * gpscourse + self.gpsalpha * self.currentcourse
        # clamp to -180 ... 180 degrees
        self.currentcourse = normalize(currentcourse,-180,180)
        return self.currentcourse 

    def followpath(self):
        ''' drives robot towards towards a waypoint '''

        # is the gps position valid
        if self.positionvalid == False:
            return
        
        # are there waypoint(s) to follow
        if len(self.waypoints) == 0:
            return

        # calculate the desired course
        self.desiredposition = self.waypoints[0]
        self.distance = distance(self.currentposition,self.desiredposition)
        self.desiredcourse = bearing(self.currentposition,self.desiredposition)

        # back off on the motor speed as we approach the desiredposition
        self.surge = min(self.vmax, 0.5 * self.distance * self.distance)

        # if the waypoint radius has been achieved
        #if self.distance < self.waypointradius:
            # move onto the next waypoint
            #self.waypoints.pop(0)


    def pidloop(self, deltaT):
        ''' steering angle to the desired course'''

        # choose a rotation direction that has the 
        # least amount of rotation to the desired course        
        error_1 = self.desiredcourse - self.currentcourse
        error_2 = 360 + error_1
        if abs(error_1) > abs(error_2):
            self.error = error_2
        else:
            self.error = error_1

        #update the integral error
        self.errSum = self.errSum + (self.error * deltaT)
        #update the differential
        self.dErr = (self.error - self.lastErr) / deltaT
            
        self.steer = (self.Kp * self.error) + (self.Ki * self.errSum) + (self.Kd * self.dErr)
        
        self.lastErr = self.error

        return constrain(self.steer)



    async def armmotors(self):
        ''' arm esc motor controllers '''
        print('arm motors')
        self.motorLeft.duty(40)
        self.motorRight.duty(40)
        await asyncio.sleep_ms(3000) 
        self.motorLeft.duty(115)
        self.motorRight.duty(115)
        await asyncio.sleep_ms(3000) 
        self.motorLeft.duty(0)
        self.motorRight.duty(0)
        print('motors armed')

    def drive(self):
        ''' drive motors (steer in degrees -180..180 , surge in cm/s) '''

        vl = (2*self.surge + radians(self.steer)*self.steergain) / 2
        vr = (2*self.surge - radians(self.steer)*self.steergain) / 2

        # clamp max and min motor speeds  
        vl = min(self.vmax,vl)
        vl = max(self.vmin,vl)
        vr = min(self.vmax,vr)
        vr = max(self.vmin,vr)

        if self.active:

            pwm_left = (vl - self.vmin) * (self.maxpwm - self.mpl) / (self.vmax - self.vmin) + self.mpl
            pwm_left = int(pwm_left)
            self.motorLeft.duty(pwm_left)
    
            pwm_right = (vr - self.vmin) * (self.maxpwm - self.mpr) / (self.vmax - self.vmin) + self.mpr
            pwm_right = int(pwm_right)
            self.motorRight.duty(pwm_right)

        else:
            self.motorLeft.duty(0)
            self.motorRight.duty(0)   
          
    def stop(self):
        '''stops both motors'''
        self.motorLeft.duty(0)
        self.motorRight.duty(0)        

    def resetcourse(self):
        ''' resets desired course, current course, surge to 0 '''
        self.desiredcourse = 0
        self.currentcourse = 0
        self.surge = 0

    def savestate(self):
        """write state to flash"""
        import json
        print('save state to flash')
        with open('controller.json', 'w') as file:

            state = {
                "name":self.name,
                "active":self.active, 
                "surge":self.surge, 
                "steer":self.steer, 
                "vmin":self.vmin, 
                "vmax":self.vmax, 
                "steergain":self.steergain, 
                "mpl":self.mpl, 
                "mpr":self.mpr, 
                "maxpwm":self.maxpwm, 
                "desiredcourse":self.desiredcourse, 
                "currentcourse":self.currentcourse, 
                "Kp":self.Kp, 
                "Ki":self.Ki, 
                "Kd":self.Kd, 
                "compassalpha":self.compassalpha, 
                "gpsalpha":self.gpsalpha, 
            }

            json.dump(state, file)

    def loadstate(self):
        """load state from flash"""
        import json
        print('load state from flash') 
        try:
            with open('controller.json', 'r') as file:
                state = json.load(file) 
                self.__dict__.update(state)
        except Exception :
            pass


def constrain(heading):
    '''heading is constrained to -180 to 180 degree range'''
    if (heading > 180):
        heading -= 360
    
    if (heading < -180):
        heading += 360
    return heading


def constrain(course):
    '''heading is constrained to -180 to 180 degree range'''
    if (course > 180):
        course -= 360
    
    if (course < -180):
        course += 360
    return course    

def normalize(num, lower=0.0, upper=360.0, b=False):
    """ Got this code from : https://gist.github.com/phn/1111712/35e8883de01916f64f7f97da9434622000ac0390"""
   
    res = num
    if not b:
        if lower >= upper:
            raise ValueError("Invalid lower and upper limits: (%s, %s)" %
                             (lower, upper))

        res = num
        if num > upper or num == lower:
            num = lower + abs(num + upper) % (abs(lower) + abs(upper))
        if num < lower or num == upper:
            num = upper - abs(num - lower) % (abs(lower) + abs(upper))

        res = lower if res == upper else num
    else:
        total_length = abs(lower) + abs(upper)
        if num < -total_length:
            num += ceil(num / (-2 * total_length)) * 2 * total_length
        if num > total_length:
            num -= floor(num / (2 * total_length)) * 2 * total_length
        if num > upper:
            num = total_length - num
        if num < lower:
            num = -total_length - num

        res = num * 1.0  # Make all numbers float, to be consistent

    return res        


def distance(p1:tuple,p2:tuple) -> int:    
    """
    distance in meters between 2 position
    p1 = lat_dd,lon_dd degree decimal format
    p2 = lat_dd,lon_dd degree decimal format
    returns int distans in meters
    """
    
    R = 6373000        # Radius of the earth in m
    
    lat1_dd, lon1_dd = p1
    lat1_dd, long1_dd = radians(lat1_dd), radians(lon1_dd)

    lat2_dd, lon2_dd = p2
    lat2_dd, lon2_dd = radians(lat2_dd), radians(lon2_dd)
    
    deltaLat = lat2_dd - lat1_dd
    deltaLon = lon2_dd - long1_dd
    
    x = deltaLon * cos((lat1_dd+lat2_dd)/2)
    distance = sqrt(x**2 + deltaLat**2) * R
    
    return distance

def bearing(p1:tuple, p2:tuple) -> int:
    """
    provides a bearing between two positions
    p1 = (lat_dd, lon_dd) degree decimal format
    p2 = (lat_dd, lon_dd) degree decimal format
    """
    lat1_dd, lon1_dd = p1
    lat1_dd, lon1_dd = radians(lat1_dd), radians(lon1_dd)

    lat2_dd, lon2_dd = p2
    lat2_dd, lon2_dd = radians(lat2_dd), radians(lon2_dd)
    
    deltaLon = lon2_dd - lon1_dd
    
    y = sin(deltaLon) * cos(lat2_dd)
    x = cos(lat1_dd) * sin(lat2_dd) - sin(lat1_dd) * cos(lat2_dd) * cos(deltaLon)
    
    bearing = (degrees(atan2(y, x)) + 360) % 360
    return bearing

def convert_dm_dd(degree :str,minutes :str, hemi :str) -> tuple:
    """ 
    convert degree minutes format to degrees decimal format 
    eg 49 21.3454 S -> dd = -49.3557566
    returns float and string representations of degree decimal
    ISSUE# On small mcu's the float precision is low:
        eg. '49.3557566' -> 49.35575 
        this can cause the robot hunt or occilate around a waypoint
    """
    degree = int(degree)
    minuite, minuite_decimal = minutes.split('.')
    degree_decimal  = int(minuite + minuite_decimal) // 6

    if hemi in ['S','W']:
        degree=degree * -1

    dd_str = str(degree)+'.'+str(degree_decimal)
    dd_float = float(dd_str)

    return (dd_float, dd_str)

