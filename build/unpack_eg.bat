call Config.cmd
@echo off

IF [%1]==[] (
	@echo Bad argv.
	@echo %0 ^<dir^>
	exit /b
)

set EXTNAME=".eg"
for %%i in ("%1\*%EXTNAME%") do (
..\binary\quickbms.exe extract_eg.bms "%%i" %1
..\..\tools\gtf2dds.exe "%%i_0.gtf" -o "%%i_0.gtf.dds"
)
