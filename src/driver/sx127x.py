""" 
SPI singleton instance
all drivers should use this instance
"""
from machine import Pin, SPI
from constants.pins import SCK_pin, MOSI_pin, MISO_pin, SX127x_CS_pin, SX127x_RST_pin, SX127x_RX_pin

spi = SPI(
    1,
    baudrate=10000000,
    sck=Pin(SCK_pin, Pin.OUT, Pin.PULL_DOWN),
    mosi=Pin(MOSI_pin, Pin.OUT, Pin.PULL_UP),
    miso=Pin(MISO_pin, Pin.IN, Pin.PULL_UP),
)

spi.deinit() # re-initialized spi after soft-start
spi.init()
cs = Pin(SX127x_CS_pin, Pin.OUT)
rst = Pin(SX127x_RST_pin, Pin.OUT)
rx = Pin(SX127x_RX_pin, Pin.IN)