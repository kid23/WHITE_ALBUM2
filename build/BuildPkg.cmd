call Config.cmd
@echo off

del "%DIR_TEMP%\pic\*.dds"
del "%DIR_TEMP%\pic\*.gtf"

call convert_png2dds.bat "%DIR_TEMP%\pic" -maskffff 
call convert_gtf.bat "%DIR_TEMP%\pic\" dds 

for %%i in ("%DIR_TEMP%\pic\*.pkgdds") do (
python import_file.py -ip "%%i"
)

call compress.bat "%DIR_TEMP%\pic\" pkgdds

for %%i in ("%DIR_TEMP%\pic\*.pkgdds") do (
echo %%~ni
move /y "%DIR_TEMP%\pic\%%~ni.pkgdds.elzma" "%DIR_OUTPUT%\dar\%%~ni.elzma"
)
pause
