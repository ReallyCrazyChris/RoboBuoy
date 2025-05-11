import uasyncio as asyncio
from driver.imu import IMU, MagDataNotReady
from storage.store import Store
store = Store.instance() #singleton reference
imu = IMU()

########################################
# Calibrate Magnetometer Async Task
async def calibrateMagTask(samples:int=1000,delay:int=20) -> tuple:
    '''
    create magnetometer bias, normailization and scaling
    this is perferformed while the magnetomer is rotating around all axes
    '''
    try:
        print('starting calibrateMagTask')

        samples = int(samples) 
        delay = int(delay) 

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
        store.magbias = (cx, cy, cz ,nx, ny, nz, sx, sy, sz) 
        # save the imu settings (incle magbias)
        #imu.save()

        return cx, cy, cz ,nx, ny, nz, sx, sy, sz
    
    except asyncio.CancelledError:
        print( "stopping calibrateMagTask" ) 