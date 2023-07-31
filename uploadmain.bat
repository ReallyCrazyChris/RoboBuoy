echo on
call ./env.bat

rem removing old files
ampy rm main.py

echo uploading new files
ampy put ./src/main.py main.py

echo starting serial console
call ./console.bat