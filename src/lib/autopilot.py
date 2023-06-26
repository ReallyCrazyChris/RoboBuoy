from math import radians, atan2, sin, cos

class AutoPilot():
    def __init__(self ):
    
        
        self.currentHeading = 0 #deg TODO needs to be radians
        self.desiredBearing = 0  #deg TODO needs to be radiansc  
        self.magDeclinaiton = 0 

        #PID tuning gains
        self.Kp = 1
        self.Ki = 0.5
        self.Kd = 0.0001

        #PID variables
        self.error = 0
        self.errSum = 0
        self.dErr = 0      
        self.lastErr = 0  # Previous error  

        # Compelmentary Filter tuning constants
        self.alpha = 0.97  # places a high emphasis on the gyro value over the compass / gps heading

        #RudderControl
        self.rudder = 0 #angular velocity rad_s


    def fuseHeading(self, gpsHeading = None, magHeading = 0, gyroVelocity = 0, deltaT = 0):
        """
        fusion of the gps Heading(slow but accurate),
        with Magnetometer( faster but inaccurate)
        with Gyro ( very fast with drift )
        to produce an overall fast and accutate heading
        """

        # calculate the magnetic declinaiton if gpsHeading true north is availiable
        if gpsHeading != None:
            self.magDeclinaiton = gpsHeading - magHeading
        
        # calculate the heading wrt true north
        trueHeading = self.magDeclinaiton + magHeading 

        # integrate gyro_z deg_s to provide gyro_z deg angular rotation
        # A complementary filter to estimate the new heading by fusing compass and gyro values.
        self.currentHeading = (1.0 - self.alpha) * trueHeading + self.alpha * ( self.currentHeading + gyroVelocity * deltaT )

        #self.currentHeading = trueHeading

        return self.currentHeading

    def headingPID(self, deltaT ):
        """
        determins the angular velocity to keep the desired heading in radians
        """

        # Error between the goal angle and robot angle
        error  = radians(self.desiredBearing) - radians(self.currentHeading)
        #clamps the error to the range 0..2PI
        self.error = atan2(sin(error), cos(error))  
        #self.error  = self.desiredBearing - self.currentHeading
        self.errSum = self.errSum + (self.error * deltaT)
        self.dErr = (self.error - self.lastErr) / deltaT
       
        self.rudder = (self.Kp * self.error) + (self.Ki * self.errSum) + (self.Kd * self.dErr)

        self.lastErr = self.error

        # clamps the output to the range 0..2PI
        self.rudder = atan2(sin(self.rudder), cos(self.rudder))



       