"""
Micropython Driver for the NeoPixels RGB Led
"""

import ustruct
from machine import Pin
from neopixel import NeoPixel

# create NeoPixel driver on GPIO15 for 10 pixels
pin = Pin(15, Pin.OUT)   
np = NeoPixel(pin,10)   

def rgb(color=0xFFFFFF):
    """ sets the color e.g 0xFFFFFF for WHITE """
    for i in range(len(np.buf)//3):
        np[i] = ustruct.pack(">i",color)[1:4]
    np.write()  

def on():
    """ all led's on"""
    rgb(0xFFFFFF)      

def off():
    """ all led's off """
    rgb(0x000000)      

