@ECHO OFF
%TRACE%

if "%1" == "python"		goto rpython

EXIT /B 4

:rpython
call $pgmhoms python
echo %PATH% | FINDSTR /C:%PYTHON_HOME% > nul
IF %ERRORLEVEL% == 0 GOTO end
set path=%path%;%PYTHON_HOME%;%PYSCRIPTS_PATH%
goto end

:end
set mytmp=
exit /b
