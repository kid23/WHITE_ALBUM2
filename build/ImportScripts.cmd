call Config.cmd
@echo off

path %PATH%;%DIR_PYTHON%
python font_tool.py -r %DIR_TEMP%\txtchs\ %DIR_TEMP%\font\t1.TBL
call compress.bat %DIR_TEMP%\txtchs txt
python wa2_eboot_tool.py -i %DIR_TEMP%\EBOOT.ELF %DIR_TEMP%\txtchs
pause