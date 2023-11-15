##################################################### 
# Persist and Hydrate the IMU's Settings
#####################################################
from lib.events import on

def persistedstate():
    ''' state that is to be persisted '''
    from lib.imu import IMU
    imu = IMU()
    return {
       "accelbias":imu.accelbias,
       "gyrobias":imu.gyrobias, 
       "magbias":imu.magbias, 
       "tempoffset":imu.tempoffset
    }

def saveimuconfig():
    """write persistedstate to flash"""
    import json
    from lib.imu import IMU
    imu = IMU()

    with open('imu.json', 'w') as file:
        json.dump(persistedstate(), file)
    
    print('saved imu config to imu.json:')
    print('accelbias',imu.accelbias)
    print('gyrobias',imu.gyrobias)
    print('magbias',imu.magbias)

def loadimuconfig():
    """load persistedstate from flash"""
    import json
    from lib.imu import IMU
    imu = IMU()
    try:
        with open('imu.json', 'r') as file:
            config = json.load(file) 
            # becasue json does not have tuples we do this:
            imu.accelbias = tuple(config['accelbias'])
            imu.gyrobias = tuple(config['gyrobias'])
            imu.magbias = tuple(config['magbias'])
            imu.tempsensitivity = config['tempsensitivity']
            imu.tempoffset = config['tempoffset']

    except OSError:
        print('imu.json not found ... imu will need calibraiton')    

# process received commands from the app
on('saveimuconfig',saveimuconfig)
on('loadimuconfig',loadimuconfig)
