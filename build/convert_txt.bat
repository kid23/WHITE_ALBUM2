call Config.cmd
@echo off

set OUTPUT_DIR=..\temp\txtcn
mkdir %OUTPUT_DIR%
path %PATH%;%DIR_PERL%
for %%i in (..\temp\eboot\*.txt) do (
piconv -f cp932 -t cp936 %%i > %OUTPUT_DIR%\%%~ni.txt
)
pause