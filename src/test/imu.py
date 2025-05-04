import uasyncio as asyncio
from lib.store import Store
store = Store.instance()

from lib.imu import IMU
imu = IMU()

async def testimu(): 
    # ARM
    print(' imu read')
  
    ax,ay,az,adT =  imu.readCalibratedAccel()
    print('   accel - ax,ay,az,adT ',ax,ay,az,adT)
    await asyncio.sleep_ms(100) 
    
    gx,gy,gz,gdT =  imu.readCalibratedGyro()
    print('   gyro - gx,gy,gz,gdT ',gx,gy,gz,gdT)
    await asyncio.sleep_ms(100) 

    temp =  imu.readTemp()
    print('   imu temp ',temp)
    print(' imu read done')
     



  
  