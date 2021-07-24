@ECHO OFF
%TRACE%

:: GENERIC PROMPT for all run environments

:: Start virtual environment
IF NOT DEFINED VENV_DIR GOTO venv2
IF NOT DEFINED RUN_CMD  GOTO venverr 'RUN_CMD'
FOR /F "DELIMS= " %%A IN ("%RUN_CMD% ++") DO (SET RCMD=%%A)
CALL $patch_%RCMD%.bat %VENV_DIR%
:venv2
IF NOT DEFINED VENV_DIR2 GOTO venv3
IF NOT DEFINED RUN_ENV2  GOTO venverr 'RUN_ENV2'
CALL $patch_%RUN_ENV2%.bat %VENV_DIR2%
:venv3
IF NOT DEFINED VENV_DIR3 GOTO cont
IF NOT DEFINED RUN_ENV3  GOTO venverr 'RUN_ENV3'
CALL $patch_%RUN_ENV3%.bat %VENV_DIR3%

:cont
:: Get program files directory
CALL $getdirs.bat

:: Get run environments' home directories
:: to be concatenated with the PATH sys env var
If DEFINED RUN_ENV1 CALL $setpat.bat %RUN_ENV1%
If DEFINED RUN_ENV2 CALL $setpat.bat %RUN_ENV2%
If DEFINED RUN_ENV3 CALL $setpat.bat %RUN_ENV3%

IF DEFINED APPDIR CD %APPDIR%

:: Get run environment verification command
:: to be executed at CMD.EXE runtime
If DEFINED RUN_VER1 SET RUN_VER=%RUN_VER1%
If DEFINED RUN_VER2 SET RUN_VER=%RUN_VER% ++ ECHO. ++ %RUN_VER2%
If DEFINED RUN_VER3 SET RUN_VER=%RUN_VER% ++ ECHO. ++ %RUN_VER3%

:: Get details of program to run 
SET CMD_PRM=%RUN_VER%
IF DEFINED RUNPAT (
   IF DEFINED RUNPGM (
      SET CMD_PRM=%RUN_VER% ++ ECHO. ++ @ECHO %RUNPGM% running... ++ %RUN_CMD% %RUNPAT%\%RUNPGM%
      GOTO exec
   )
) ELSE (
   IF DEFINED RUNPGM (
      SET CMD_PRM=%RUN_VER% ++ ECHO. ++ @ECHO %RUNPGM% ++ %RUN_CMD% %RUNPGM%
      GOTO exec
   )
)

:exec
CMD %CMD_OPTS% "%CMD_PRM:++=&&%"
EXIT /B

:venverr
@ECHO VenvError: Missing/Invalid required variable - %1
EXIT /B 4
