echo on
call ./env.bat

echo removing old files
ampy rmdir /driver
 
echo uploading driver
ampy put ./src/driver /driver

echo starting serial console
call ./console.bat