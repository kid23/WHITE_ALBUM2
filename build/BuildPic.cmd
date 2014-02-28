call Config.cmd
echo off

call convert_gtf.bat "%DIR_TEMP%\pic\" dds 
call compress.bat "%DIR_TEMP%\pic\" gtf
for %%i in ("%DIR_TEMP%\pic\*.gtf") do (
echo %%~ni
move /y "%DIR_TEMP%\pic\%%~ni.gtf.elzma" "%DIR_OUTPUT%\dar\%%~ni.elzma"
)
pause
