call Config.cmd
cd "%PS3_TOOL%\"
scetool.exe -i "%PS3_RESOURCE%\EBOOT.BIN">"%DIR_BUILD%\log.txt"
scetool.exe --decrypt "%PS3_RESOURCE%\EBOOT.BIN" "%DIR_TEMP%\EBOOT.ELF">>"%DIR_BUILD%\log.txt"
pause
