import uasyncio as asyncio
from lib import server

class Store(object):

    _instance = None # is a singleton
    
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__( self ):
        
        self.name = "Mark"
        self.color= "green"
        self.number = 1

        # Battery
        self.battery = 35 # % Capacity of Battery Remaining

        # Position
        self.positionvalid = False
        self.latitude = 0 # degree decimal north
        self.longitude = 0 # degree decimal east
        self.latitude_string = '' # degree decimal north 24 bit precision, 
        self.longitude_string = ''# degree decimal east 24 bit precision
        self.position = (0,0) # degree decimal north, degree decimal east

        # Course
        self.gpscourse = 0
        self.currentcourse = 0 # deg° of the current heading

        # Speed
        self.gpsspeed = 0.0  # knots

        # Pathfinding
        self.destination = (0,0) # degree decimal north, degree decimal east
        self.distance = 0 # float meters : distance to desired posiiton
        self.desiredcourse = 0 # deg° of the desired heading
        self.waypoints = [] # waypoint positions
        self.waypointarrivedradius = 5 # waypoint arrived radius (meters)

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

        # Motor Control
        self.motorsactive = False # enables / disbles the motors
        self.surge = 0 #  desired robot speed cm/s
        self.steer = 0 #  desired robot angualr rotation deg/s
        self.vmin = 0  #  minimum robot velocity cm/s
        self.vmax = 50 #  maximum robot velocity cm/s
        self.steergain = 100 # steering gain
        self.mpl = 53  #  left pwm value where the thruster start to turn
        self.mpr = 55  #  right pwm value where the thruster start to turn
        self.maxpwm = 110 # maximum pwm signal sent to the motors



        server.addListener('active',self.setactive) 
        server.addListener('surge',self.setsurge)
        server.addListener('dc',self.setdesiredcourse)
        server.addListener('wp',self.setwaypoints)
        server.addListener('save',self.savestate)
        server.addListener('load',self.loadstate)

        server.addListener('SMT', self.startSendMotionStateTask)
        server.addListener('getSteerPIDState', self.getSteerPIDState)
        server.addListener('getMotorState', self.getMotorState)   



    ##################### 
    # SendMotionStateTask
    def startSendMotionStateTask(self):
        motionStateTask = asyncio.create_task( self.sendMotionStateTask() )
        server.addListener('sSMT', motionStateTask.cancel)        

    async def sendMotionStateTask(self):
        ''' continously sends motion parameters to the RoboBouyApp '''
        try:
            print('starting sendMotionStateTask')
            while True:
                await asyncio.sleep_ms(1000)  

                state = {
                    "battery":int(self.battery),
                    "positionvalid":bool(self.positionvalid),
                    "position":self.position,
                    "currentcourse":int(self.currentcourse), 
                    "surge":int(self.surge),
                    "distance":int(self.distance)
                }

                server.send('state',state)
                

        except asyncio.CancelledError:
            print( "stopping sendMotionStateTask")


    def old_getstate(self):
        ''' send the state to the RoboBouyApp '''
        state = {
            "name":self.name,
            "color":self.color,
            "number":self.number,
            "battery":self.battery,
            "active":self.active, 
            "surge":self.surge, 
            "steer":self.steer, 
            "vmin":self.vmin, 
            "vmax":self.vmax, 
            "steergain":self.steergain, 
            "mpl":self.mpl, 
            "mpr":self.mpr, 
            "maxpwm":self.maxpwm, 
            #"dcourse":int(self.desiredcourse), 
            "ccourse":int(self.currentcourse), 
            "Kp":self.Kp, 
            "Ki":self.Ki, 
            "Kd":self.Kd, 
            "compassalpha":self.compassalpha, 
            "gpsalpha":self.gpsalpha,
            "a":"b"
        }

        server.send('state',state)

    def getSteerPIDState(self):
        ''' send the state to the RoboBouyApp '''
        state = {
            "Kp":float(self.Kp), 
            "Ki":float(self.Ki), 
            "Kd":float(self.Kd)
        }
        server.send('state',state)

    def getMotorState(self):
        ''' send the state to the RoboBouyApp '''
        state = {
            "active":bool(self.active), 
            "surge":int(self.surge), 
            "steer":int(self.steer), 
            "vmin":int(self.vmin), 
            "vmax":int(self.vmax), 
            "steergain":int(self.steergain), 
            "mpl":int(self.mpl),
            "mpr":int(self.mpr),
            "maxpwm":int(self.maxpwm)
        }
        server.send('state',state)        
         
        
    ####################
    # Setters
    def setactive(self,val):
        self.active = bool(val) 
        print('setactive', self.active) 

    def setsurge(self,val):
        self.surge = int(val)

    def setwaypoints(self,val):
        self.waypoints = val
        print('set waypoints',self.waypoints)

    def setdesiredcourse (self,val):
        self.desiredcourse = int(val) 
        print('desiredcourse',self.desiredcourse)

    ################
    # Persistance
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