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

def convert_dm_dd(degree :str,minutes :str, hemi :str) -> str:
    '''
    Converts "degrees, decimal.minutes" -> degrees.decimal:str 

    Returns tuple :
        float   degrees.decimal with 6 digits of precision,
        integer with 9 digits of precision

    e.g.
    49.6939697, 496939697 =  convert_dm_dd("49","41.638187","N") 

    Micropyhton has poor floating point precision
    this means that distance and bearing calculations are too inaccurate.
    The solution here providesds float values, but also integervalues specific for the 
    distance and bearing calculaiton.
    ''' 
    degree = int(degree)
    minuite, minuite_decimal = minutes.split('.')
    degree_decimal  = int(minuite + minuite_decimal) // 6

    if hemi in ['S','W']:
        degree=degree * -1

    dd = str(degree)+"."+str(degree_decimal) 
    dd = '{:<010s}'.format(dd) # Micropython 10 Digits Precision (2147483647), 
    dd = dd[:10] #we choose 9 digit precision

    return dd

def convert_dd_int(degreedecimal:str) -> int:
    '''
    converts degree decimal to big int
    "49.6939697" => 496939697
    '''
    degree, decimal = degreedecimal.split('.')
    dd = str(degree)+str(decimal) 
    dd = '{:<09s}'.format(dd) # Micropython 10 Digits Precision (2147483647), we choose 9 digit precision
    dd = dd[:9]
    return int(dd)

def distancebearing(position_str,destination_str):
    '''
    Provides distance (meters:float) and bearing (degrees:float) from a position to a destination 
    This calculation is suitable for distances 10km or less and it is customized to mitigate the 
    poor floating point precision of Micropython
    For larger distances the Haversine formula would be needed
    '''

    print('position_str',position_str)
    lat_p = convert_dd_int(position_str[0])
    lon_p = convert_dd_int(position_str[1])
    print('lat_p,lon_p',lat_p,lon_p)

    print('destination_str',destination_str)
    lat_d = convert_dd_int(destination_str[0])
    lon_d = convert_dd_int(destination_str[1])
    print('lat_d,lon_d',lat_d,lon_d)

    dy = lat_d-lat_p # delta latitude
    dx = lon_d-lon_p # delta longitude

    # correct dx due to the curvature of the earth
    latA = float(destination_str[0])
    latB = float(position_str[0])
    latAvg = (latA+latB)/2
    dx = dx*cos(radians(latAvg))   

    arcdegrees = sqrt(dx**2 + dy**2)    # good old pythagoras
    meters = arcdegrees * 0.011112      # 111120 / 10000000 # 111120 meters in an arcdegree
    meters = round(meters,1)

    bearing = degrees(atan2(dx,dy))
    bearing = round(bearing,1) 

    return meters, bearing