call Config.cmd
@echo off

path %PATH%;%DIR_PYTHON%
python font_tool.py -r %DIR_TEMP%\txtchs\ %DIR_TEMP%\scripts_all.tbl
call compress.bat %DIR_TEMP%\txtchs txt
rem python wa2_eboot_tool.py -i %DIR_TEMP%\EBOOT.ELF %DIR_TEMP%\txtchs
move /y "%DIR_TEMP%\txtchs\*.elzma" "%DIR_TEMP%\eboot\"
pause