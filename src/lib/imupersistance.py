##################################################### 
# Persist and Hydrate the IMU's Settings
#####################################################
from lib.events import on
from lib.imu import IMU
imu = IMU()

def persistedstate():
    ''' state that is to be persisted '''
    return {
       "accelbias":imu.accelbias,
       "gyrobias":imu.gyrobias, 
       "magbias":imu.magbias, 
       "tempoffset":imu.tempoffset
    }

def saveimuconfig():
    """write persistedstate to flash"""
    import json
    with open('imu.json', 'w') as file:
        json.dump(persistedstate(), file)
    
    print('saved imu config to imu.json:')
    print('accelbias',imu.accelbias)
    print('gyrobias',imu.gyrobias)
    print('magbias',imu.magbias)

def loadimuconfig():
    """load persistedstate from flash"""
    import json
    try:
        with open('imu.json', 'r') as file:
            settings = json.load(file) 
            imu.__dict__.update(settings)

        print('loaded imu config from imu.json:')
        print('accelbias',imu.accelbias)
        print('gyrobias',imu.gyrobias)
        print('magbias',imu.magbias)
    except Exception :
        pass

# process received commands from the app
on('saveimuconfig',saveimuconfig)
on('loadimuconfig',loadimuconfig)

            