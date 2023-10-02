echo on
call ./env.bat

echo removing old files
ampy rm main.py
ampy rmdir /lib

echo uploading new files
ampy put ./src/lib /lib
ampy put ./src/main.py main.py

echo starting serial console
call ./console.bat