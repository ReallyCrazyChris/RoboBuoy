import uasyncio as asyncio
from lib.store import Store
store = Store.instance()

from lib.gps import GPS
gps = GPS()

async def testgps(): 
    # ARM
    print(' gps read')
    gps.readGpsTask()
    while not gps.positionAvailable.is_set():
        print('   gps - waiting for position')
        await asyncio.sleep(500)
    print('   gps - lat,lon ',store.position)
    print(' gps read done')



  
  