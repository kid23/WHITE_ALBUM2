@echo off

IF [%1]==[] (
	@echo Bad argv.
	@echo %0 ^<dir^>
	exit /b
)

@rem %2 used for mask value

for %%i in ("%1\*.dds") do (
@echo %%i
..\..\3rd\nvtt\nvddsinfo.exe "%%i"
@echo.
)
