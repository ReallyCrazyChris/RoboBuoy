echo on
call ./env.bat

echo removing old files
ampy rm main.py
ampy rmdir /constants
ampy rmdir /driver
ampy rmdir /lib
ampy rmdir /states
ampy rmdir /storage
ampy rmdir /tasks
ampy rmdir /transport    

echo uploading constants
ampy put ./src/constants /constants
echo uploading drivers
ampy put ./src/driver /driver
echo uploading lib
ampy put ./src/lib /lib
echo uploading states
ampy put ./src/states /states
echo uploading storage
ampy put ./src/storage /storage
echo uploading tasks
ampy put ./src/tasks /tasks
echo uploading transport
ampy put ./src/transport /transport 
echo uploading main.py
ampy put ./src/main.py main.py

echo starting serial console
call ./console.bat