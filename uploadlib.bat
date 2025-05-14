echo on
call ./env.bat

echo removing old files
ampy rmdir /lib
 
echo uploading lib
ampy put ./src/lib /lib

echo starting serial console
call ./console.bat