call Config.cmd
@echo off

IF [%1]==[] (
	@echo Bad argv.
	@echo %0 ^<dir^> ^<extname^> 
	exit /b
)
IF [%2]==[] (
	@echo Bad argv.
	@echo %0 ^<dir^> ^<extname^> 
	exit /b
)

set EXTNAME=.%2
path %PATH%;%DIR_PYTHON%
for %%i in ("%1\*%EXTNAME%") do (
python wa2_eboot_tool.py -c "%%i" "%%i.elzma"
)
