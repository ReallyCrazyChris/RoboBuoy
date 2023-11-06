import uasyncio as asyncio
from lib.imu import IMU, MagDataNotReady
imu = IMU()

########################################
# Calibrate Magnetometer Async Task
########################################

async def calibrateMagTask(samples:int=800,delay:int=10) -> tuple:
    '''
    create magnetometer bias, normailization and scaling
    this is perferformed while the magnetomer is rotating around all axes
    '''
    try:
        print('starting calibrateMagTask')

        samples = int(samples) or 800
        delay = int(delay) or 10

        minx = 0
        maxx = 0
        miny = 0
        maxy = 0
        minz = 0
        maxz = 0

        # collect minimum and maximum magnetometer samples
        while samples :
            try:
                await asyncio.sleep_ms(delay)
            
                x,y,z = imu.readMag()  
                samples = samples - 1
                minx = min(x,minx)
                maxx = max(x,maxx)
                miny = min(y,miny)
                maxy = max(y,maxy)
                minz = min(z,minz)
                maxz = max(z,maxz)
            
            except MagDataNotReady:
                pass
                

        # Average
        cx = (maxx + minx) / 2
        cy = (maxy + miny) / 2  
        cz = (maxz + minz) / 2  

        # Normailze
        nx = abs(maxx - cx)
        ny = abs(maxy - cy)
        nz = abs(maxz - cz)

        # Soft iron correction
        avg_delta_x = (maxx - minx) / 2
        avg_delta_y = (maxy - miny) / 2
        avg_delta_z = (maxz - minz) / 2

        avg_delta = (avg_delta_x + avg_delta_y + avg_delta_z) / 3
        
        sx = avg_delta / avg_delta_x
        sy = avg_delta / avg_delta_y
        sz = avg_delta / avg_delta_z

        print("bias",cx,cy,cz)
        print("normalisation",nx,ny,nz)
        print("scale",sx,sy,sz)

        # update the magbias
        imu.magbias = (cx, cy, cz ,nx, ny, nz, sx, sy, sz) 
        # save the imu settings (incle magbias)
        imu.save()

        return cx, cy, cz ,nx, ny, nz, sx, sy, sz
        print( "completed calibrateMagTask" ) 
    except asyncio.CancelledError:
        print( "stopping calibrateMagTask" ) 


########################################
# Calibrate Accelerometer Task
########################################

async def calibrateAccelTask(samples:int=100,delay:int=10) -> tuple:
    ''' creates accelerometer averaged values for biasing the accelerometer at rest'''
        
    try:
        print('starting calibrateAccelTask')
        
        ox, oy, oz = 0.0, 0.0, 0.0
        n = float(samples) #TODO do we need float here ?

        while samples:
            await asyncio.sleep_ms(delay)
            gx, gy, gz = imu.readAccel()
            ox += gx
            oy += gy
            oz += gz
            samples -= 1

        # mean accel values
        ox,oy,oz = ox / n, oy / n, oz / n
        # update the accel bias
        imu.accelbias = (ox,oy,oz)
        # save the imu settings
        imu.save()

        print( "completed calibrateAccelTask" )

        return ox,oy,oz 

    except asyncio.CancelledError:
        print( "stopping calibrateAccelTask" )  

########################################
# Calibrate Gyro Task
########################################

async def calibrateGyroTask( samples:int=100, delay:int=10 ) -> tuple:
    ''' creates gyro averaged values for biasing the gyro at rest '''        
    try:
        print('starting calibrateAccelTask')        
        ox, oy, oz = 0.0, 0.0, 0.0
        n = float(samples)

        while samples:
            await asyncio.sleep_ms(delay)
            gx, gy, gz = imu.readGyro()
            ox += gx
            oy += gy
            oz += gz
            samples -= 1

        # mean gyro values
        ox,oy,oz = ox / n, oy / n, oz / n

        # update the gyro bias
        imu.gyrobias = (ox,oy,oz)

        # save the settings
        imu.save()

        return ox,oy,oz  
    
    except asyncio.CancelledError:
        print( "stopping calibrateAccelTask" ) 
    
