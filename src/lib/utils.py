from math import floor, ceil, radians, sin, cos, sqrt, degrees, atan2, pi



def translateValueRange(input,minIn,maxIn,minOut,maxOut):
    ''' Translate input value from one range to another '''
    # input is between minIn and maxIn
    # output is between minOut and maxOut
    # e.g. translateValueRange(0,0,100,0,255) => 0

    speed = min(maxIn, max(minIn, input))
    out =(speed-minIn)/(maxIn-minIn)*(maxOut-minOut)+minOut
    return int(out)




def normalize(angle):
    '''Normalize degrees to -PI to PI radians range'''
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

    #print('position_str',position_str)
    lat_p = convert_dd_int(position_str[0])
    lon_p = convert_dd_int(position_str[1])
    #print('lat_p,lon_p',lat_p,lon_p)

    #print('destination_str',destination_str)
    lat_d = convert_dd_int(destination_str[0])
    lon_d = convert_dd_int(destination_str[1])
    #print('lat_d,lon_d',lat_d,lon_d)

    dy = lat_d-lat_p # delta latitude
    dx = lon_d-lon_p # delta longitude

    # correct dx due to the curvature of the earth
    latA = float(destination_str[0])
    latB = float(position_str[0])
    latAvg = (latA+latB)/2
    dx = dx*cos(radians(latAvg))   

    # The distances are relatively small and the curvature of the earth is not taken into account
    # The distance is calculated in arcdegrees, which is then converted to meters
    # ISSUE : distance may be inaccurate for the higher lattitudes, where the curvature of the earth is more pronounced
    arcdegrees = sqrt(dx**2 + dy**2)    # good old pythagoras
    distance = arcdegrees * 0.011112      # 111120 / 10000000 # 111120 meters in an arcdegree
    distance = round(distance,1)    # distance in meters

    bearing = round(atan2(dx,dy),3) # bearing in radians
   
    return distance, bearing