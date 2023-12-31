""" 
GPS UART instance
all drivers should use this instance
"""
from machine import UART
# T-Beam V1.1
gpsuart = UART(2, baudrate=9600, bits=8, parity=None, stop=1, tx=12, rx=34, rts=-1, cts=-1, txbuf=256, rxbuf=256, timeout=0, timeout_char=2)