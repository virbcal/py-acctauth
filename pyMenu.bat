@echo off
SETLOCAL
set TRACE=
call $settings.bat
set APPDIR=%cd%
set RUN_CMD=python
set RUN_ENV1=python
set RUN_ENV2=
set RUN_ENV3=
set RUN_VER1=python -V
set RUN_VER2=
set RUN_VER3=
set CMD_OPTS=/C
set VENV_DIR=%PYVEGUI%
set RUNPAT=%CEAPPS%
set RUNPGM=gMenu.py

PUSHD "%BATDIR%"
call $spromp.bat
POPD