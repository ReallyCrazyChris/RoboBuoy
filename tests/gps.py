import uasyncio as asyncio
from lib.store import Store
store = Store.instance()

from lib.gps import GPS
gps = GPS()

async def testgps(): 
    # ARM
    print(' gps read')
    gpsTask = asyncio.create_task( gps.readGpsTask() )
    await asyncio.sleep(1500)
    print('   gps - lat,lon ',store.position)
    print(' gps read done')
    gpsTask.cancel()



  
  