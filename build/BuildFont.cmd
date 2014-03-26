@call Config.cmd
@echo off

path %PATH%;%DIR_PYTHON%

python font_tool.py -mup "%DIR_TEMP%\txtchs" "%DIR_TEMP%\mini_up.txt"
python font_tool.py -mm "%DIR_TEMP%\mini_up.txt" "%DIR_TEMP%\scripts_all.tbl" "%DIR_TEMP%\mini_up" 0

"%WORK_SPACE%\binary\FontMake.exe" -fwa2 "%DIR_TEMP%\font\org\02309.pkgdds_000.bmp" "%DIR_TEMP%\scripts_all_add.txt" 0 "%DIR_TEMP%\mini_up_sorted.txt" 0 "%DIR_TEMP%\mini_eboot_all.txt" 
copy "%DIR_TEMP%\data.dar_unpacked\ddspkg\02309.pkgdds" "%DIR_TEMP%\font"
move font1.png "%DIR_TEMP%\font\02309.pkgdds_000.png"
move font2.png "%DIR_TEMP%\font\02309.pkgdds_001.png"
rem move font3.png "%DIR_TEMP%\font\02309.pkgdds_002.png"
..\..\3rd\nvtt\nvcompress.exe -nomips -nocuda -rgb16 "%DIR_TEMP%\font\02309.pkgdds_000.png"
..\..\3rd\nvtt\nvcompress.exe -nomips -nocuda -rgb16 "%DIR_TEMP%\font\02309.pkgdds_001.png"
rem ..\..\3rd\nvtt\nvcompress.exe -nomips -nocuda -rgb8 "%DIR_TEMP%\font\02309.pkgdds_002.png"
"%PS3_TOOL%\dds2gtf.exe" "%DIR_TEMP%\font\02309.pkgdds_000.dds"
"%PS3_TOOL%\dds2gtf.exe" "%DIR_TEMP%\font\02309.pkgdds_001.dds"
rem "%PS3_TOOL%\dds2gtf.exe" "%DIR_TEMP%\font\02309.pkgdds_002.dds"
python import_file.py -mp "%DIR_TEMP%\font\02309.pkgdds"
call compress.bat "%DIR_TEMP%\font\" pkgdds
move /Y "%DIR_TEMP%\font\02309.pkgdds.elzma" "%DIR_OUTPUT%\dar\02309.elzma"
del "%DIR_TEMP%\font\*.gtf"
del "%DIR_TEMP%\font\*.dds"

@echo.
@echo Waiting for manual process mini.bin
pause

copy /Y "%DIR_TEMP%\data.dar_unpacked\gtf\01409.gtf" "%DIR_TEMP%\font\01409.gtf"
"%PS3_TOOL%\gtf2dds.exe" "%DIR_TEMP%\font\01409.gtf"
python font_tool.py -e3 "%DIR_TEMP%\font\01409.dds"
copy /Y mini.bin "%DIR_TEMP%\font\01409.dds_g.bin"
@echo Import 01409.dds
python font_tool.py -m3 "%DIR_TEMP%\font\01409.dds" "%DIR_TEMP%\font\01409.dds"
"%PS3_TOOL%\dds2gtf.exe" "%DIR_TEMP%\font\01409.dds"
call compress.bat "%DIR_TEMP%\font\" gtf
move /Y "%DIR_TEMP%\font\01409.gtf.elzma" "%DIR_OUTPUT%\dar\01409.elzma"
pause
