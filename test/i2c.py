

from lib.i2c import i2c


def testi2c(): 
    # Scan all I2C addresses between 0x08 and 0x77 inclusive and return a list of those that respond
    print(' scan i2c bus')
    i2c_devices = i2c.scan()
    print('   i2c devices ',i2c_devices)

    
    

    
     



  
  