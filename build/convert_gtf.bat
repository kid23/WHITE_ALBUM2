@echo off

IF [%1]==[] (
	@echo Bad argv.
	@echo %0 ^<dir^>
	exit /b
)

for %%i in ("%1\*.dds") do (
@echo %%i
..\..\tools\dds2gtf.exe "%%i" -o "%%~dpni.gtf"
)
