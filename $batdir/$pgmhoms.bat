@ECHO OFF
%TRACE%

if "%1" == "python"		goto rpython

EXIT /B 4

:rpython
set PYTHON_HOME=%PGMFILES%\Python\Python37-32
set PYSCRIPTS_PATH=%PYTHON_HOME%\Scripts
goto end

:end
EXIT /B
