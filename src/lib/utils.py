from math import floor, ceil, radians, sin, cos, sqrt, degrees, atan2, pi

def translateValue(valueIn,minIn,maxIn,minOut,maxOut):
    ''' Translate value from one range to another '''
    valueIn = min(maxIn, max(minIn, valueIn)) # clamp the input value
    valueOut =(valueIn-minIn)/(maxIn-minIn)*(maxOut-minOut)+minOut # translate the value
    return valueOut

def normalize(angle):
    '''Normalize radians to -PI to PI radians range'''
    return (angle + pi) % (2 * pi) - pi

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
    The solution here provides float values, but also integer values specific for the 
    distance and bearing calculation.
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
    Converts degree decimal to integer
 
    Micropython has limited floading precision of 10 Digits.
    Some functions like math.cos, have results that are too imprecise for navigation
    The poor mans fix is to do these calculation with integers

    Args:
        degreedecimal: "49.6939697" 

    Returns:
        integer 496939697 suitable for precise calculations
       
    '''
    degree, decimal = degreedecimal.split('.')
    dd = str(degree)+str(decimal) 
    dd = '{:<09s}'.format(dd) # Micropython 10 Digits Precision (2147483647), we choose 9 digit precision
    dd = dd[:9]
    return int(dd)

    
def positionDifference(position_str:str,destination_str:str) -> tuple:
    ''' 
        Provides the longitudal and latitudal differnce in meters
        This calculation is suitable for distances 10km or less and
        it is customized to mitigate the poor floating point precision of Micropython.
        For larger distances the Haversine formula would be needed
    '''

    lat_p = convert_dd_int(position_str[0])
    lon_p = convert_dd_int(position_str[1])

    lat_d = convert_dd_int(destination_str[0])
    lon_d = convert_dd_int(destination_str[1])

    # delta longitude, latitude, in arcdegrees
    dx_arc = lon_d-lon_p 
    dy_arc = lat_d-lat_p 


    # correct dx_arc due to the curvature of the earth
    latA = float(destination_str[0])
    latB = float(position_str[0])
    latAvg = (latA+latB)/2
    correct_dx_arc = dx_arc*cos(radians(latAvg))   

    # The distances dx and dy are arcdegrees, which is then converted to meters
    dx_meters = correct_dx_arc * 0.011112       # 111120 / 10000000 # 111120 meters in an arcdegree
    dy_meters = dy_arc * 0.011112           	# 111120 / 10000000 # 111120 meters in an arcdegree

    return dx_meters, dy_meters

 
def distanceBearing(position_str:str,destination_str:str) -> tuple:
    '''
    Provides distance (meters:float) and bearing (degrees:float) from a position to a destination 
    '''

    dx_meters, dy_meters = positionDifference(position_str,destination_str)
    
    distance_meters = round(sqrt(dx_meters**2 + dy_meters**2),1)   # distance in meters, limted to 1 decimal
    bearing_rad = round(atan2(dx_meters,dy_meters),3) # bearing in radians, limited to 3 decimals

    return distance_meters, bearing_rad ,dx_meters, dy_meters