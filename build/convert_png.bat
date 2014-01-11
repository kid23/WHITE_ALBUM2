call Config.cmd
@echo off

IF [%1]==[] (
	@echo Bad argv.
	@echo %0 ^<dir^>
	exit /b
)

cd %I_VIEW_DIR%
i_view32.exe "%1\*.dds" /convert="%1\png\*.png"
cd %DIR_BUILD%