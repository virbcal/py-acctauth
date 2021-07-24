@ECHO OFF
%TRACE%

IF "%1" == "" GOTO error
set mytmp=%1\Scripts
IF NOT EXIST "%mytmp%" GOTO error

echo %PATH% | FINDSTR /C:%mytmp% > nul
IF %ERRORLEVEL% == 0 GOTO end
set path=%mytmp%;%path%
activate

:end
set mytmp=
exit /b

:error
@ECHO PatchError: (%~nx0) Missing/Invalid required parameter - %1
EXIT /B 4
