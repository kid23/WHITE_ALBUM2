call Config.cmd
@echo off

path %PATH%;%DIR_PYTHON%
del "%DIR_OUTPUT%\dar.zip"
python setup.py py2exe -d "%DIR_OUTPUT%"
rmdir /S /Q build\ 
move /y "%DIR_OUTPUT%\import_file.exe" "%DIR_OUTPUT%\WA2_PS3_CHS_PATCH.exe"

del "%DIR_OUTPUT%\darjpn.zip"
python setup_jpn.py py2exe -d "%DIR_OUTPUT%"
rmdir /S /Q build\ 
move /y "%DIR_OUTPUT%\import_file.exe" "%DIR_OUTPUT%\WA2_PS3_JPN_RESTORE.exe"

pause
