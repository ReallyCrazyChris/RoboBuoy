""" 
I2C instance
all drivers should use this instance
"""
from machine import I2C, Pin
from constants.pins import SCL_pin, SDA_pin

###############
# ESP32
i2c = I2C(1,scl=Pin(SCL_pin), sda=Pin(SDA_pin), freq=400000)  

###############
# ESP32-S3 SRAM
#i2c = I2C(1,scl=Pin(9), sda=Pin(8), freq=400000) 
