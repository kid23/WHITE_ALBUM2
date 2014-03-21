call Config.cmd
@echo off

path %PATH%;%DIR_PYTHON%
del "%DIR_TEMP%\pic\*.dds"
del "%DIR_TEMP%\pic\*.gtf"

call convert_png2dds.bat "%DIR_TEMP%\pic" -rgb16 -maskffff 
call convert_png2dds.bat "%DIR_TEMP%\pic\32" -rgb32 
move /y "%DIR_TEMP%\pic\32\*.dds" "%DIR_TEMP%\pic\"
call convert_png2dds.bat "%DIR_TEMP%\pic\8" -rgb8 
move /y "%DIR_TEMP%\pic\8\*.dds" "%DIR_TEMP%\pic\"
call convert_png2dds.bat "%DIR_TEMP%\pic\DXT5" -bc3 
move /y "%DIR_TEMP%\pic\DXT5\*.dds" "%DIR_TEMP%\pic\"

call convert_gtf.bat "%DIR_TEMP%\pic\" dds 

for %%i in ("%DIR_TEMP%\pic\*.pkgdds") do (
python import_file.py -ip "%%i"
)

call compress.bat "%DIR_TEMP%\pic\" pkgdds

for %%i in ("%DIR_TEMP%\pic\*.pkgdds") do (
echo %%~ni
move /y "%DIR_TEMP%\pic\%%~ni.pkgdds.elzma" "%DIR_OUTPUT%\dar\%%~ni.elzma"
)

del "%DIR_TEMP%\pic\*.gtf" 
pause
