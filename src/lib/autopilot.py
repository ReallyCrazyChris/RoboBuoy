import time
from machine import PWM, Pin
from math import degrees, radians, sin, cos, atan2

motorLeft = PWM(Pin(16))
motorLeft.freq(50)

motorRight = PWM(Pin(17))
motorRight.freq(50)


def translate(num, inMin, inMax, outMin, outMax):
  return int(outMin + ((num - inMin) / (inMax - inMin) * (outMax
                  - outMin)))

class AutoPilot():
    def __init__(self, i2c ):
    
        self.i2c = i2c

        self.name = "RoboBuoy"

        # If the motors are active or not
        self.motorsactive = False 

        # Magnetic course and declination
        self.magcourse = 0    
        self.magdeclinaiton = 0 

        # Course
        self.currentcourse = 0 # Fused from GPS, Magnetic and Gyro Course 
        self.desiredcourse = 0 # the course to steer : degrees
        self.distance = None
        # Pathfinding

        self.autopilot = True # If the robot should navigate itself to the next waypoint

        # PID tuning gains to control the steering based on desiredcourse vs currentcourse
        self.Kp = 1
        self.Ki = 0 #.5
        self.Kd = 0 #.0001

        # PID variables to matintain course by steering
        self.error = 0
        self.errSum = 0
        self.dErr = 0      
        self.lastErr = 0  # Previous error

        # PID output to steer and surge the robot
        self.steer = 0 # The steering angle in radians #TODO ... sort of (unconfirmed)  
        self.surge = 0 # The forward speed in meters per second m/s #TODO ... sort of (unconfirmed)  
        # Compelmentary Filter tuning constants
        self.alpha = 0.97  # places a high emphasis on the gyro value over the compass / gps heading

        self.speedleft = 0
        self.speedright = 0
        self.minpwm=40
        self.maxpwm=110


    def integrate_gyro(self,gyro_deg_s,deltaT ):
        self.currentcourse =  ( self.currentcourse + gyro_deg_s * deltaT )
        return self.currentcourse


    def fusecourse(self, gpscourse = None, magcourse = 0, gyro_deg_s = 0, deltaT = 0):
        """
        fusion of the gpscourse (slow but accurate),
        with magcourse ( faster but inaccurate)
        with gyro ( very fast but with drift )
        to produce an overall fast and accutate current course
        """

        # calculate the magnetic declinaiton if gpsHeading true north is availiable
        #if gpscourse != None:
        #    self.magdeclinaiton = gpscourse - magcourse
        
        # calculate the heading wrt true north
        #truemagcourse = self.magdeclinaiton + magcourse 

        # integrate gyro_z deg_s to provide gyro_z deg angular rotation
        # A complementary filter to estimate the new course by fusing compass and gyro values.
        #self.currentcourse = (1.0 - self.alpha) * truemagcourse + self.alpha * ( self.currentcourse + gyro_deg_s * deltaT )

        self.currentcourse =  ( self.currentcourse + gyro_deg_s * deltaT )

        return self.currentcourse


    def steering_pid(self, desiredcourse, currentcourse, deltaT ):
        """
        determins the steer in radians to keep the desired course in radians
        """

        self.error  = self.desiredcourse - self.currentcourse
        #self.errSum = self.errSum + (self.error * deltaT)
        #self.dErr = (self.error - self.lastErr) / deltaT
    
        steering_angle = (self.Kp * self.error) #+ (self.Ki * self.errSum) + (self.Kd * self.dErr)
        self.lastErr = self.error

        return steering_angle 


    def course_pid(self, desiredcourse, currentcourse, deltaT ):
        """
        determins the steer in radians to keep the desired course in radians
        """

        # Error between the desiredcourse angle and currentcourse angle
        #error  = radians(self.desiredcourse) - radians(self.currentcourse)
        
        self.error  = self.desiredcourse - self.currentcourse

        #self.error = atan2(sin(error), cos(error))  #clamps the error to the range 0..2PI #TODO do more effeciently
        
        #self.errSum = self.errSum + (self.error * deltaT)
        #self.dErr = (self.error - self.lastErr) / deltaT
    
        steering_angle = (self.Kp * self.error) #+ (self.Ki * self.errSum) + (self.Kd * self.dErr)
        self.lastErr = self.error

        # clamps the output to the range 0..2PI #TODO can this be done more effeciently
        #self.steer = atan2(sin(w), cos(w))

        return steering_angle 

    

    def drive(self,steer,surge):
        """
        from steer in rad/s and surge in meters/s
        determin the needed left and right motor speeds in rad/s
        """
        if self.motorsactive:
            speedleft = round(255 * steer) + surge
            speedright = round(-255 * steer) + surge

            # clamp the speed in range -254..254
            speedleft = min(254,speedleft)
            speedleft = max(speedleft,0)
            # clamp the speed in range -254..254
            speedright = min(254,speedright)
            speedright = max(speedright,0)
            
            self.drivemotors(speedleft,speedright)
        else:
            self.stopmotors()


    def drivemotors(self,speedleft,speedright):
        """
        drives the motor right and left speeds in rad/s
        """      

        self.speedleft = speedleft
        self.speedright = speedright

        leftduty = translate(self.speedleft,0,254,self.minpwm,self.maxpwm)
        rightduty = translate(self.speedright,0,254,self.minpwm,self.maxpwm)

        #print(leftduty,rightduty)

        motorLeft.duty(leftduty)
        motorRight.duty(rightduty)
        
    def stopmotors(self):
        """
        stops both motors
        """
        motorLeft.duty(0)
        motorRight.duty(0)

    def armmotors(self):
        """
        arms both motors
        """
        motorLeft.duty(self.maxpwm)
        motorRight.duty(self.maxpwm)
        time.sleep(3)
        motorLeft.duty(self.minpwm)
        motorRight.duty(self.minpwm)


