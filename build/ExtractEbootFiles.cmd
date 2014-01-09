call Config.cmd
@echo off

mkdir %DIR_TEMP%\eboot
path %PATH%;%DIR_PYTHON%
python wa2_eboot_tool.py -e %DIR_TEMP%\EBOOT.ELF %DIR_TEMP%
pause
