echo on

call ./env.bat

echo removing main.py, drivers, lib
ampy rm /main.py
ampy rmdir /drivers
ampy rmdir /lib

echo creating directories: drivers, lib
ampy mkdir /drivers
ampy mkdir /lib

echo uploading drivers: i2c, imu

rem ampy put ./src/drivers/mqtt.py /drivers/mqtt.py
ampy put ./src/drivers/i2c.py /drivers/i2c.py
ampy put ./src/drivers/imu.py /drivers/imu.py
ampy put ./src/drivers/bleuart.py /drivers/bleuart.py
ampy put ./src/drivers/thruster.py /drivers/thruster.py


echo uploading lib: steeringPID gps
ampy put ./src/lib/steeringPID.py /lib/steeringPID.py
ampy put ./src/lib/gps.py /lib/gps.py
ampy put ./src/lib/server.py /lib/server.py
ampy put ./src/lib/bencode.py /lib/bencode.py

echo uploading main 
ampy put ./src/main.py /main.py

echo starting serial console
call ./console.bat



