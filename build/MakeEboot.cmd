call Config.cmd
@echo off

path %PATH%;%DIR_PYTHON%
call DecryptEboot.cmd
python wa2_eboot_tool.py -rebuild "%DIR_TEMP%\EBOOT.ELF" "%DIR_TEMP%\eboot"
"..\binary\WQSG 导出(导入)_v2012.12070.exe" i -tbl "%DIR_TEMP%\font\final.tbl" -tbl2 "%DIR_TEMP%\font\control.tbl" -rom "%DIR_TEMP%" -text "%DIR_TEMP%" -sp1 0x20
python wa2_eboot_tool.py -patch "%DIR_TEMP%\EBOOT.ELF" 3844 "%DIR_TEMP%\pic\eboot\warning.gtf.elzma"
call EncryptEboot.cmd
pause
