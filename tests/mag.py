import uasyncio as asyncio

from driver.imu import IMU, MagDataNotReady
imu = IMU()

async def getmagdata(): 
    ''' generates a magdata.csv file with raw magneometer data'''
    print('start: get mag data')
    samples = 100
    delay   = 100 #ms
    csv=open("magdata.csv","at")

    # collect magnetometer samples
    while samples :
        try:
            samples = samples - 1
            await asyncio.sleep_ms(delay)
            x,y,z = imu.readMag()
            csv.write("{:5.2f},{:5.2f},{:5.3f}\n".format(x,y,z))
            print("{:5.2f},{:5.2f},{:5.3f}\n".format(x,y,z))
            
        except MagDataNotReady as me:
            pass
        except OSError:
            csv.close()
            print("Disk full?")

    csv.close()
    print('end: get mag data')




  
  