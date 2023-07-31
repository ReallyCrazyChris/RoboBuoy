import time #TODO try to use asyncio on arm motors
import uasyncio as asyncio
from machine import PWM, Pin
from math import floor, ceil, radians
from lib.server import Server

server = Server()

class Controller():
    def __init__(self):

        self.name = "RoboBuoy 1"

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

        # Pathfinding
        self.desiredcourse = 0 # deg°
        self.currentcourse = 0 # deg°

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


        # add commands and their handlers to the server
        server.addListener('state',self.requeststate)

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

        server.addListener('reset',self.resetcourse)

        server.addListener('save',self.savestate)
        server.addListener('load',self.loadstate)

    def requeststate(self,_):
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
        print('response',state)
        server.send('state',state)


    def setactive(self, active):
        print('active',active)
        self.active = bool(active)   
        self.drive()

    def setsurge(self, surge):
        self.surge = int(surge) 
        print('surge',self.surge)
        self.drive()

    def setsteer(self, steer):
        self.steer = int(steer)     
        print('steer',self.steer)
        self.drive() 

    def setvmin(self, vmin):
        print('vmin (cm/s)',vmin)
        self.vmin = int(vmin)

    def setvmax(self, vmax):
        print('vmax (cm/s)',vmax)
        self.vmax = int(vmax)
        self.drive()  

    def setsteergain(self, steergain):
        print('steergain',steergain)
        self.steergain = int(steergain)
        self.drive()

    def setmpl(self, mpl):
        print('mpl',mpl)
        self.mpl = int(mpl)  
        self.surge = 1
        self.steer = 0
        self.drive()

    def setmpr(self, mpr):
        print('mpr',mpr)
        self.mpr = int(mpr)  
        self.surge = 1
        self.steer = 0
        self.drive()    

    def setcurrentcourse(self, currentcourse):
        self.currentcourse = int(currentcourse) 
        print('currentcourse',self.currentcourse)
    
    def setdesiredcourse (self,desiredcourse):
        self.desiredcourse = int(desiredcourse) 
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
        
    def setcompassalpha (self,compassalpha):
        self.compassalpha = float(compassalpha) 
        print('compassalpha',self.compassalpha)

    def setgpsalpha (self,gpsalpha):
        self.gpsalpha = float(gpsalpha) 
        print('gpsalpha',self.gpsalpha)


    # actual controller part

    def fusegyro(self,gyro_deg_s,deltaT ):
        '''integrates the gyro rate of yaw (deg_s) into angle (deg)'''
        self.currentcourse =  ( self.currentcourse + gyro_deg_s * deltaT )
        # clamp to -80 ... 180 degrees
        self.currentcourse = normalize(self.currentcourse,-180,180)
        return self.currentcourse

    def fusecompass(self, compasscourse):
        '''fuses the compas course witht he current course using a complement filter, strongly weighted towards the gyro'''
        self.currentcourse = (1.0 - self.compassalpha) * normalize(compasscourse,-180,180) + self.compassalpha * self.currentcourse
        self.currentcourse = normalize(self.currentcourse,-180,180)
        return self.currentcourse

    def fusegps(self, gpscourse):
        '''fuses the gps course with the currentcourse using a complement filter, strongly weighted towards the gps'''
        #TODO do we need normalize gps course
        self.currentcourse = (1.0 - self.gpsalpha) * normalize(gpscourse,-180,180) + self.gpsalpha * self.currentcourse
        self.currentcourse = normalize(self.currentcourse,-180,180)
        return self.currentcourse    

    def pidloop(self, deltaT):
        ''' steering angle to maintain the desired course'''
        self.error  = self.desiredcourse - self.currentcourse
        self.errSum = self.errSum + (self.error * deltaT)
        self.dErr = (self.error - self.lastErr) / deltaT
    
        self.steer = (self.Kp * self.error) + (self.Ki * self.errSum) + (self.Kd * self.dErr)
        
        self.lastErr = self.error

        return self.steer 

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

    def resetcourse(self, _):
        ''' resets desired course, current course, surge to 0 '''
        self.desiredcourse = 0
        self.currentcourse = 0
        self.surge = 0

    def savestate(self, _ ):
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

    def loadstate(self, _ ):
        """load state from flash"""
        import json
        print('load state from flash') 
        try:
            with open('controller.json', 'r') as file:
                state = json.load(file) 
                self.__dict__.update(state)
        except Exception :
            pass


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
