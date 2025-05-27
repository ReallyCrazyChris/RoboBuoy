@echo off
call ./env.bat
PuTTY.exe -serial %AMPY_PORT% -sercfg 115200,8,n,1,N
echo in the console execute a soft-reboot with Ctrl + D 
echo or enter the REP with Ctrl + C 