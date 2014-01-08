@echo off
mkdir txtcn
path %PATH%;D:\Perl\bin

for %%i in (eboot\*.txt) do (
@echo %%i
piconv -f cp932 -t cp936 %%i > txtcn/%%~ni.txt
)
pause