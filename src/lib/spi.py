""" 
SPI singleton instance
all drivers should use this instance
"""
from machine import Pin, SPI

# SPI pins
SCK = 5
MOSI = 27
MISO = 19

# Lora SX127(X) control pins
CS = 18  # lora chip select
RST = 23 # lora chip reset
RX = 26  # lora packet received IRQ

spi = SPI(
    1,
    baudrate=10000000,
    sck=Pin(SCK, Pin.OUT, Pin.PULL_DOWN),
    mosi=Pin(MOSI, Pin.OUT, Pin.PULL_UP),
    miso=Pin(MISO, Pin.IN, Pin.PULL_UP),
)

spi.deinit() # re-initialized spi after soft-start
spi.init()
cs = Pin(CS, Pin.OUT)
rst = Pin(RST, Pin.OUT)
rx = Pin(RX, Pin.IN)