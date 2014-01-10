call Config.cmd
@echo off

IF [%1]==[] (
	@echo Bad argv.
	@echo %0 ^<dir^>
	exit /b
)

set EXTNAME=".elzma"
path %PATH%;%DIR_PYTHON%
for %%i in ("%1\*%EXTNAME%") do (
python wa2_eboot_tool.py -d "%%i" "%%~dpni"
)
pause