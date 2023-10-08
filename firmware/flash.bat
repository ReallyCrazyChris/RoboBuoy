@echo off
call ../env.bat

echo flashing firmware for standard ESP32
esptool.py --chip esp32 --port %AMPY_PORT%  write_flash -z 0x1000 ./ESP32_GENERIC-20230426-v1.20.0.bin

rem echo flashing firmware for ESP32 with SPIRAM
rem esptool.py --chip esp32 --port %AMPY_PORT%  write_flash -z 0x1000 ./ESP32_GENERIC-SPIRAM-20231005-v1.21.0.bin