@echo off

IF [%1]==[] (
	@echo Bad argv.
	@echo %0 ^<dir^>
	exit /b
)

@rem %2 used for mask value

for %%i in ("%1\*.png") do (
@echo %%i
..\..\3rd\nvtt\nvcompress.exe -nomips -nocuda -rgb16 %2 "%%i" -o "%%~dpni.dds"
)
