call Config.cmd
echo off

call convert_png2dds.bat "%DIR_TEMP%\pic\gtf32" -rgb32 
call convert_gtf.bat "%DIR_TEMP%\pic\gtf32" dds 
call compress.bat "%DIR_TEMP%\pic\gtf32" gtf
for %%i in ("%DIR_TEMP%\pic\gtf32\*.gtf") do (
echo %%~ni
move /y "%DIR_TEMP%\pic\gtf32\%%~ni.gtf.elzma" "%DIR_OUTPUT%\dar\%%~ni.elzma"
)
del "%DIR_TEMP%\pic\gtf32\*.gtf"
del "%DIR_TEMP%\pic\gtf32\*.dds"

call convert_png2dds.bat "%DIR_TEMP%\pic\eboot" -rgb32 
call convert_gtf.bat "%DIR_TEMP%\pic\eboot" dds 
call compress.bat "%DIR_TEMP%\pic\eboot" gtf
del "%DIR_TEMP%\pic\eboot\*.gtf"
del ""%DIR_TEMP%\pic\eboot\*.dds"

pause
