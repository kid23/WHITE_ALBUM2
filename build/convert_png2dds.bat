@echo off

IF [%2]==[] (
	@echo Bad argv.
	@echo %0 ^<dir^>
	exit /b
)

@rem %2 used for rgb bit
@rem %3 used for mask value

for %%i in ("%1\*.png") do (
@echo %%i
..\..\3rd\nvtt\nvcompress.exe -nomips -nocuda %2 %3 "%%i" -o "%%~dpni.dds"
)
