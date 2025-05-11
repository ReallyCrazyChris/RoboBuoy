import uasyncio as asyncio

from test.i2c import testi2c
print('test i2c')
testi2c() 
print('test i2c done')

from test.motors import testmotors
print('test motors')
asyncio.run( testmotors() )    
print('test motors done')

from test.imu import testimu
print('test imu')   
asyncio.run( testimu() )
print('test imu done')

from test.gps import testgps
print('test gps')
asyncio.run( testgps() )    
print('test gps done')