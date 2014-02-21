call Config.cmd
@echo off

path %PATH%;%DIR_PYTHON%
call DecryptEboot.cmd
call python wa2_eboot_tool.py -rebuild "%DIR_TEMP%\EBOOT.ELF" "%DIR_TEMP%\eboot"
call EncryptEboot.cmd
pause
