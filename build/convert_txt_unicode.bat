call Config.cmd
@echo off

path %PATH%;%DIR_PYTHON%

IF [%1]==[] (
	@echo Bad argv.
	@echo %0 ^<dir^>
	exit /b
)

for %%i in ("%1\*.txt") do (
@echo "%2\%%~dpni.txt"
python font_tool.py -c "%%i" "%2\%%~ni.txt"
)
