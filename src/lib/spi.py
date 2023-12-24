""" 
SPI instance
all drivers should use this instance
"""
from machine import Pin, SPI

###############
# ESP32

# SPI pins
SCK = 5
MOSI = 27
MISO = 19

# Lora SX1278 control pins
CS = 18  # Chip select
RX = 26  # Receive IRQ
RST = 23  # Receive IRQ

# Setup SPI
spi = SPI(
    1,
    baudrate=10000000,
    sck=Pin(SCK, Pin.OUT, Pin.PULL_DOWN),
    mosi=Pin(MOSI, Pin.OUT, Pin.PULL_UP),
    miso=Pin(MISO, Pin.IN, Pin.PULL_UP),
)

spi.init()
cs = Pin(CS, Pin.OUT)
rx = Pin(RX, Pin.IN)
rst = Pin(RST, Pin.IN)