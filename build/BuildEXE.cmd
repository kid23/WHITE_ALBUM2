call Config.cmd
@echo off

path %PATH%;%DIR_PYTHON%
rem del "%DIR_OUTPUT%\dar.zip"
"C:\Program Files\WinRAR\rar.exe" au -ep1 "%DIR_OUTPUT%\dar.zip" "%DIR_OUTPUT%\dar\*.elzma" 
python setup.py py2exe -d "%DIR_OUTPUT%"
pause
