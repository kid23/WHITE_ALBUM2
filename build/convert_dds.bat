@echo off

IF [%1]==[] (
	@echo Bad argv.
	@echo %0 ^<dir^>
	exit /b
)

for %%i in ("%1\*.gtf") do (
@echo %%i
..\..\tools\gtf2dds.exe "%%i" -o "%%~dpni.dds"
)
pause