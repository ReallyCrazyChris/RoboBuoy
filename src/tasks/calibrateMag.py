import uasyncio as asyncio
from driver.imu import IMU, MagDataNotReady
from storage.store import Store
store = Store.instance() #singleton reference
imu = IMU()

########################################
# Calibrate Magnetometer Async Task
async def calibrateMagTask(samples:int=1000,delay:int=100):
    '''
    create magnetometer bias, normailization and scaling
    this is perferformed while the magnetomer is rotating around all axes
    '''
    try:
        print('starting calibrateMagTask')

        samples = int(samples) 
        delay = int(delay) 

        # initialize the varibles with actual data
        try:
            x,y,z = imu.readMag()  
            minx = x
            maxx = x
            miny = y
            maxy = y
            minz = z
            maxz = z
            await asyncio.sleep_ms(delay)
        except MagDataNotReady:
                pass

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
                
        # Calculate hard iron offsets (center of min/max for each axis)
        cx = (maxx + minx) / 2
        cy = (maxy + miny) / 2  
        cz = (maxz + minz) / 2  

        # Calculate soft iron scaling (scale each axis to spherical)
        avg_delta = ( (maxx - minx) +  (maxy - miny) +  (maxz - minz) ) / 3
        sx = avg_delta / (maxx - minx) if maxx != minx else 1
        sy = avg_delta / (maxy - miny) if maxy != miny else 1
        sz = avg_delta / (maxz - minz) if maxz != minz else 1

        # Factors to soft iron scaling the data in a range -1..1
        nx = abs(maxx - cx)
        ny = abs(maxy - cy)
        nz = abs(maxz - cz)

        print("hard iron offsets",cx,cy,cz)
        print("soft iron scaling",sx,sy,sz)
        print("normalize factors",nx,ny,nz)

        # update the magbias
        store.magbias = (cx, cy, cz, sx, sy, sz, nx, ny, nz) 

        return cx, cy, cz, sx, sy, sz, nx, ny, nz
    
    except asyncio.CancelledError:
        print( "stopping calibrateMagTask" ) 