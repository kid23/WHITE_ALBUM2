call Config.cmd
@echo off

path %PATH%;%DIR_PYTHON%
del "%DIR_OUTPUT%\dar.zip"
python setup.py py2exe -d "%DIR_OUTPUT%"
rmdir /S /Q build\ 
pause
