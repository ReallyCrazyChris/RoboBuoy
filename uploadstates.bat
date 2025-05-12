echo on
call ./env.bat

echo removing old files
ampy rmdir /states
 
echo uploading states
ampy put ./src/states /states

echo starting serial console
call ./console.bat