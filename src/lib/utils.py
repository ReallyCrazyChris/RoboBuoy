from math import floor, ceil, radians, sin, cos, sqrt, degrees, atan2

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
