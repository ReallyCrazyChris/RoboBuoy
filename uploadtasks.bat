echo on
call ./env.bat

echo removing old files
ampy rmdir /tasks
 
echo uploading tasks
ampy put ./src/tasks /tasks

echo starting serial console
call ./console.bat