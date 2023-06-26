echo on
call ./env.bat

echo removing main autopilot
ampy rm /main.py
rem ampy rm /lib/autopilot.py
ampy rm /drivers/thruster.py

echo uploading autopilot main
ampy put ./src/drivers/thruster.py /drivers/thruster.py
rem ampy put ./src/lib/autopilot.py /lib/autopilot.py
ampy put ./src/main.py /main.py

echo starting serial console
call ./console.bat



