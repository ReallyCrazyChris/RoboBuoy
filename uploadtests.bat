echo on
call ./env.bat

echo removing old files
ampy rmdir /tests
 
echo uploading tests
ampy put ./tests /tests

echo starting serial console
call ./console.bat