
"""
Path Planning
Station Keeping
Waypoint Following
Course and Speed to Waypoint
Course PID Controller
Heading Fusion of Gyro, Magetometer, GPS Heading
Speed Fusion of Accelerometer and GPS Speed
Gyro - Done
Accelerometer - Done
Magnetomoeter - Done
GPS Position, Heading, Speed, Accuracy
Differential Thruster Mixer - Done
Thruster Driver - Done
Brushless Motors
https://www.youtube.com/watch?v=2et2Q3v6XPg&feature=youtu.be
https://github.com/CRAWlab/RoboBoat-2019/blob/master/Python%20Scripts/Utility%20Scripts/geographic_calculations.py
https://github.com/sergiuharjau/roboBoat/blob/master/mainSteering.py

test:$ pytest ./pseudo.py

"""

def planwaypoints( waypoint ):
    """
    plan a seris of waypoints from the current loaction
    to the target waypoint.
    """
    # uses gps
    pass

def followwaypoints( waypoints ):
    """
    strategy to follow one or more waypoints    
    """
    # uses gps
    # uses course to set a new course
    pass

def keepstation():
    """
    strategy to keep the current position
    """
    # uses positionFusion to get a fast and accurate position
    # uses course to keep the station
    pass

def currentPosition():
    """
    fustion of the gps Position (slow but accurate)
    with accelerometer ( fast but with integral drift )
    """
    # uses gps
    # uses accermeter
    # returns a fast and accurate position
    pass


def currentHeading():
    """
    fusion of the gps Heading(slow but accurate),
    with Magnetometer( faster but inaccurate)
    with Gyro ( very fast with drift )
    """
    # uses gps
    # uses magnetometer
    # uses gyro
    # return an accurate and fast low drift heading
    pass

def currentSpeed():
    """
    fusion of the gps speed (slow but accurate )
    with Acceleroeter ( very fast but with drift)
    """
    # uses gps
    # uses accelerometer
    # return an accurate and fast speed 
    pass


def headingPID( currentHeading, desiredBearing ):
    """
    keeps the desired heading in radians
    """
    #uses currentHeading
    pass

def speedPID( currentSpeed, desiredSpeed ):
    """
    keeps the desired speed -1..0..1
    """
    #uses currentSpeed
    pass

def waypoint( lat, long ):
    """
    sets the desired waypoint to go to
    """
    # uses gps position
    # uses course
    pass

def course( desiredBearing, desiredSpeed ):
    """
    Maintains a course
    Inputs:
        desiredBearing radians
        desiredSpeed 0..1

    Outputs:
        rudderAngle radians in range -pi/2 ..0 .. p/2
        desiredPower float -1 .. 0 .. 1

    """

    #uses currentHeading
    #uses currentSpeed
    #uses headingPID
    #uses speedPID
    #uses thrustermixer
    pass



def distance(position1, position2):
    """
    calculate distance between two lat/long positions 
    position1 = lat/long pair in decimal degrees DD.dddddd
    position2 = lat/long pair in decimal degrees DD.dddddd
    distance meters
    """

    R = 6373000        # Radius of the earth in m
    
    lat1, long1 = radians(position1)
    lat2, long2 = radians(position2)
    
    dLat = lat2 - lat1
    dLon = long2 - long1
    
    x = dLon * cos((lat1+lat2)/2)
    distance = sqrt(x**2 + dLat**2) * R
    
    return distance

def bearing( position1, position2 ):
    lat1, long1 = deg2rad(position1)
    lat2, long2 = deg2rad(position2)
    
    dLon = long2 - long1
    
    y = sin(dLon) * cos(lat2)
    x = cos(lat1)*  sin(lat2) - sin(lat1) * cos(lat2) * cos(dLon)
    
    bearing = ( degrees( atan2(y, x) ) + 360) % 360
    
    return bearing


def deg2rad( position ):
    """
    converts a degrees position to a radians position
    """
    return ( radians(position[0]), radians (position[1]) )






