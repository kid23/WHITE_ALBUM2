call Config.cmd

@echo off
if /I %SELF_OUTPUT_TYPE%==NPDRM (
set SELF_ARGS=--self-type=NPDRM --np-license-type=FREE --np-app-type=UEXEC --np-content-id=JP0761-BLJM60229_00-WHITEALBUMPATCH0 --np-real-fname=EBOOT.BIN
) else (
set SELF_ARGS=--self-type=APP
)
@echo on

cd "%PS3_TOOL%\"
scetool.exe --sce-type=SELF %SELF_ARGS% --skip-sections=FALSE --key-revision=1c --self-auth-id=1010000001000003 --self-vendor-id=01000002 --self-app-version=0001000000000000 --encrypt "%DIR_TEMP%\EBOOT.ELF" "%DIR_OUTPUT%\PS3_GAME\USRDIR\EBOOT.BIN" >"%DIR_BUILD%\log.txt"
scetool.exe -i "%DIR_OUTPUT%\PS3_GAME\USRDIR\EBOOT.BIN" >>"%DIR_BUILD%\log.txt"
pause