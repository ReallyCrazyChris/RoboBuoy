
import uasyncio as asyncio

async def connect_to_wifi(ssid='SummerTime', password='Calmhat436'):
    import network
    try:
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            print('connecting to wifi network...')
            sta_if.active(True)
            sta_if.connect(ssid, password)
            while not sta_if.isconnected():
                await asyncio.sleep(1)  
        
        print('successfull connection to ',ssid)
        print('network config:', sta_if.ifconfig())

    except asyncio.CancelledError:
        print( "connect_to_wifi_stopped" )