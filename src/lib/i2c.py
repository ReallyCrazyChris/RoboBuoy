""" 
I2C instance
all drivers should use this instance
"""
from machine import I2C, Pin

###############
# ESP32
i2c = I2C(1,scl=Pin(22), sda=Pin(21), freq=400000)  

###############
# ESP32-S3 SRAM
#i2c = I2C(1,scl=Pin(9), sda=Pin(8), freq=400000) 
