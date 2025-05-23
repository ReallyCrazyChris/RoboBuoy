# This file defines the pin numbers for the ESP32 board used in the project.
# The pin numbers are used to configure the GPIO pins for various peripherals and components.
# The pin numbers are defined as constants for easy reference throughout the code.
# The pin numbers are based on the ESP32 board's GPIO pin mapping.

#I2C GPIO pins
SCL_pin = 22
SDA_pin = 21

# SPI GPIO pins
SCK_pin = 5
MOSI_pin = 27
MISO_pin = 19

# Lora SX127(X) control GPIO pins
SX127x_CS_pin = 18  # lora chip select
SX127x_RST_pin = 23 # lora chip reset
SX127x_RX_pin = 26  # lora packet received IRQ

# Motor control GPIO pins
PWM_left_pin = 13
PWM_right_pin = 2
