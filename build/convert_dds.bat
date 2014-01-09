echo off

for %%i in ("E:\wa\PS3_Projects\WHITE_ALBUM2\build\data.dar_unpacked\*.gtf") do (
@echo %%i
..\binary\gtf2dds.exe "%%i" -o "%%i.dds"
)
pause