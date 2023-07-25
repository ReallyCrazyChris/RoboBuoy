echo on
call ./env.bat

echo removing main 
ampy rm /main.py
ampy rm /lib/server.py

echo  server main
ampy put ./src/lib/server.py /lib/server.py
ampy put ./src/main.py /main.py

echo starting serial console
call ./console.bat