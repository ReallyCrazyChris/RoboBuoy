echo on
call ./env.bat

rem removing old files
ampy rm lib/motors.py

echo uploading lib.motors
ampy put ./src/lib/motors.py lib/motors.py

echo starting serial console
call ./console.bat