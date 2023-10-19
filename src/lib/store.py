import uasyncio as asyncio
from lib import server

class Store(object):

    _instance = None # is a singleton
    
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__( self ):
        
        ####################
        # The RoboBuoy State
        ####################
            
        # Information
        self.number = 1     #Mark Number
        self.color= "green" #Primary Color of the Mark
        self.name = "Mark"  #Name of the RoboBupy in the APP
        self.mode = "stop"  #Current operational mode of the RoboBouy  ['stop','manual','auto']
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
        self.waypointarrivedradius = 5 # waypoint arrived radius (meters)
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
        self.steergain = 100 # steering gain
        self.mpl = 53  #  left pwm value where the motor starts to turn
        self.mpr = 55  #  right pwm value where the motor starts to turn
        self.maxpwm = 110 # maximum pwm signal sent to the motors

        ###################
        # Command Listeners
        # coming from the RoboBouyAPP
        # #################
               
        # Send RoboBouyAPP relevant state       
        server.addListener('getState',self.getState)

        # Information
        server.addListener('number',self.setnumber)
        server.addListener('color',self.setcolor)
        server.addListener('name',self.setname)

        # AutonomousPathfinding Listeners
        server.addListener('dc',self.setdesiredcourse)                
        server.addListener('wp',self.setwaypoints)
        server.addListener('wr',self.setwaypointarrivedradius)

        # Steering PID Listeners
        server.addListener('Kp',self.setKp)
        server.addListener('Ki',self.setKi)
        server.addListener('Kd',self.setKd)
        
        # Complimentary Filter Listeners
        server.addListener('magalpha',self.setmagalpha)
        server.addListener('gpsalpha',self.setgpsalpha)
        server.addListener('declinationalpha',self.setdeclinationalpha)

        # Motor State Listeners
        server.addListener('surge',self.setsurge)
        server.addListener('vmin',self.setvmin)
        server.addListener('vmax',self.setvmax)
        server.addListener('steergain',self.setsteergain)
        server.addListener('mpl',self.setmpl)
        server.addListener('mpr',self.setmpr)

        # Persistance Command Listeners
        server.addListener('savesettings',self.savesettings)
        server.addListener('loadsettings',self.loadsettings)

        # Request Listeners
        server.addListener('getPIDsettings', self.getPIDsettings)
        server.addListener('getMotorsettings', self.getMotorsettings)
        server.addListener('getAlphasettings', self.getAlphasettings)    


    ##############################
    # Setters ( old school style )
    ##############################
    # TODO create guards for the value setters
    # RoboBuoy Information Setters
    def setnumber(self,val):
        self.number = int(val)
    def setcolor(self,val):
        self.color = val 
    def setname(self,val):
        self.name = val 
    def setmode(self,val):
        self.mode = val 
    # Battery Setters
    def setbattery(self,val):
        self.battery = int(val)
    # Position Setters
    def setpositionvalid(self,val):
        self.positionvalid = bool(val)  
    def setposition(self,val):
        self.position = val 
    def setgpsspeed(self,val):
        self.gpsspeed = int(val)
    def setgpscourse(self,val):
        self.gpscourse = int(val)                  
    # Course
    def setcurrentcourse(self,val):
        self.currentcourse = int(val)    
    # AutonomousPathfinding
    def setdestination(self,val):
        self.destination = val 
    def setdistance(self,val):
        self.distance = int(val)
    def setdesiredcourse(self,val):
        self.desiredcourse = int(val)
    def setwaypoints(self,val):
        print(val)
        self.waypoints = val 
    def setwaypointarrivedradius(self,val):
        self.waypointarrivedradius = int(val) 
    # PID Setters - use setters to set the state
    def setKp(self,val):
        self.Kp = float(val) 
    def setKi(self,val):
        self.Ki = float(val) 
    def setKd(self,val):
        self.Kd = float(val) 
    # Complementary filter Setters - use setters to set the state
    def setmagalpha(self,val):
        self.magalpha = float(val) 
    def setgpsalpha(self,val):
        self.gpsalpha = float(val) 
    def setdeclinationalpha(self,val):
        self.declinationalpha = float(val)         
    # Motor Setters - use setters to set the state 
    def setsurge(self,val):
        self.surge = int(val) 
    def setsteer(self,val):
        self.steer = int(val) 
    def setvmin(self,val):
        self.vmin = int(val) 
    def setvmax(self,val):
        print('setvmax',val)
        self.vmax = int(val) 
    def setsteergain(self,val):
        self.steergain = int(val) 
    def setmpl(self,val):
        self.mpl = int(val)
    def setmpr(self,val):
        self.mpr = int(val)
    def setmaxpwm(self,val):
        self.maxpwm = int(val)    

    ##################################################### 
    # Tasks that update the RoboBuoyAPP State
    #####################################################
    
    async def sendMotionStateTask(self):
        ''' continously sends motion parameters to the RoboBouyApp '''
        try:
            print('starting sendMotionStateTask')
            while True:
                await asyncio.sleep_ms(1000)  
                state = {
                    "mode":self.mode,
                    "positionvalid":bool(self.positionvalid),
                    "position":self.position,
                    "currentcourse":int(self.currentcourse), 
                    "desiredcourse":int(self.desiredcourse),
                    "gpscourse":int(self.gpscourse),
                    "gpsspeed":int(self.gpsspeed),
                    "magcourse":int(self.magcourse),
                    "magdeclination":int(self.magdeclination),
                    "surge":int(self.surge),                
                }
                server.send('state',state)
        except asyncio.CancelledError:
            print( "stopping sendMotionStateTask")

    def sendWaypointsUpdate(self):
        ''' send a waypoints update '''
        state = {
            "waypoints":self.waypoints,
            "waypointarrivedradius":self.waypointarrivedradius,
        }
        server.send('state',state)


    ##################
    # Request Handlers
    ##################
    def getState(self):
        ''' send the state to the RoboBouyApp in chunks '''
        
        stateA = {
            "number":self.number,
            "name":self.name,
            "color":self.color,
            "mode":self.mode,
            "battery":self.battery,
        }
        stateB = {
            "waypoints":self.waypoints,
            "waypointarrivedradius":self.waypointarrivedradius,
        }
        stateC = {    
            "Kp":self.Kp, 
            "Ki":self.Ki, 
            "Kd":self.Kd,
            "magalpha":self.magalpha, 
            "gpsalpha":self.gpsalpha,
            "declinationalpha":self.declinationalpha
        }
        stateD = {                 
            "vmin":self.vmin, 
            "vmax":self.vmax, 
            "steergain":self.steergain, 
            "mpl":self.mpl, 
            "mpr":self.mpr, 
            "maxpwm":self.maxpwm, 
        }

        # send state in chunks
        server.send('state',stateA)
        server.send('state',stateB)
        server.send('state',stateC)
        server.send('state',stateD)

    def getPIDsettings(self):
        ''' send the state to the RoboBouyApp '''
        state = {
            "Kp":float(self.Kp), 
            "Ki":float(self.Ki), 
            "Kd":float(self.Kd)
        }
        server.send('state',state)

    def getMotorsettings(self):
        ''' send the state to the RoboBouyApp '''
        state = {    
            "surge":int(self.surge), 
            "vmin":int(self.vmin), 
            "vmax":int(self.vmax), 
            "steergain":int(self.steergain), 
            "mpl":int(self.mpl),
            "mpr":int(self.mpr),
            "maxpwm":int(self.maxpwm)
        }
        server.send('state',state)        

    def getAlphasettings(self):
        ''' send the state to the RoboBouyApp '''
        state = {    
            "gpsalpha":float(self.gpsalpha), 
            "magalpha":float(self.magalpha), 
            "declinationalpha":float(self.declinationalpha)
        }
        server.send('state',state)  
        
    ######################
    # Persistance Commands
    ######################
    def savesettings(self):
        """write store to flash"""
        import json
        print('save state to flash')
        with open('store.json', 'w') as file:

            state = {
                "number":self.number,
                "name":self.name,
                "color":self.color,
                "waypoints":self.waypointarrivedradius,
                "waypointarrivedradius":self.waypointarrivedradius,
                "Kp":self.Kp, 
                "Ki":self.Ki, 
                "Kd":self.Kd,
                "gpsalpha":self.gpsalpha,
                "magalpha":self.magalpha,
                "magdeclination":self.magdeclination, 
                "declinationalpha":self.declinationalpha,
                "vmin":self.vmin, 
                "vmax":self.vmax, 
                "steergain":self.steergain, 
                "mpl":self.mpl, 
                "mpr":self.mpr, 
                "maxpwm":self.maxpwm, 
            }

            json.dump(state, file)

    def loadsettings(self):
        """load store state from flash"""
        import json
        print('load store from flash') 
        try:
            with open('store.json', 'r') as file:
                state = json.load(file) 
                self.__dict__.update(state)
        except Exception :
            pass