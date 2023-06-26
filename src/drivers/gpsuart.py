""" 
A Singleton Instance of the UART 
all drivers should use this Instance
"""
import uasyncio as asyncio
import uasyncio as asyncio
from machine import UART
from store.gps import gpssentence

uart = UART(2, baudrate=9600, bits=8, parity=None, stop=1, tx=5, rx=13, rts=-1, cts=-1, txbuf=256, rxbuf=256, timeout=0, timeout_char=2)

async def readlineTask( readlineEvent=None ):
    """
    A Async task that polls the serial buffer for a line
    fires the async realineEvent
    """
    while readlineEvent != None:
    
        line = uart.readline()
        
        if line != None:
            print( line )
            gpssentence( line )
            readlineEvent.set()

        await asyncio.sleep(0.1)
