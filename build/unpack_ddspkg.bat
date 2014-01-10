call Config.cmd
@echo off

IF [%1]==[] (
	@echo Bad argv.
	@echo %0 ^<dir^>
	exit /b
)

set EXTNAME=".ddspkg"
for %%i in ("%1\*%EXTNAME%") do (
..\binary\quickbms.exe extract_ddspack.bms "%%i" %1
)
convert_dds.bat %1
pause