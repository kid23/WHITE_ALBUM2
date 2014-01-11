@rem make sure free space > 12G
@rem require quickbms
@rem require python 

@echo off

call ExtractDar.cmd
decompress.bat ..\temp\data.dar_unpacked

mkdir ..\temp\data.dar_unpacked\ddspkg
mkdir ..\temp\data.dar_unpacked\eg
mkdir ..\temp\data.dar_unpacked\elzma
mkdir ..\temp\data.dar_unpacked\gtf

move ..\temp\data.dar_unpacked\*.elzma ..\temp\data.dar_unpacked\elzma 
move ..\temp\data.dar_unpacked\*.ddspkg ..\temp\data.dar_unpacked\ddspkg
move ..\temp\data.dar_unpacked\*.eg ..\temp\data.dar_unpacked\eg
move ..\temp\data.dar_unpacked\*.gtf ..\temp\data.dar_unpacked\gtf

unpack_ddspkg.bat ..\temp\data.dar_unpacked\ddspkg
convert_dds.bat ..\temp\data.dar_unpacked\ddspkg
convert_png.bat %DIR_TEMP%\data.dar_unpacked\ddspkg

rem unpack_eg.bat ..\temp\data.dar_unpacked\eg
rem convert_dds.bat ..\temp\data.dar_unpacked\eg

rem convert_dds.bat ..\temp\data.dar_unpacked\gtf
