@call Config.cmd
@echo off

path %PATH%;%DIR_PYTHON%
python font_tool.py -mup "%DIR_TEMP%\txtchs" "%DIR_TEMP%\font\up.txt"
"%WORK_SPACE%\binary\FontMake.exe" -fwa2 "%DIR_TEMP%\font\org\02309.pkgdds_000.bmp" "%DIR_TEMP%\t3add.txt" 0 "%DIR_TEMP%\up_sorted.txt" 0 "%DIR_TEMP%\sorted_mini.txt" 
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
pause
