echo on
call ./env.bat

echo removing old files
ampy rmdir /transport
 
echo uploading transport
ampy put ./src/transport /transport

echo starting serial console
call ./console.bat