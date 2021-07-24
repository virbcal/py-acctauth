@ECHO OFF
%TRACE%

set APPSDIR=%CD%
set BATDIR=%APPSDIR%\$batdir
set CEAPPS=%APPSDIR%\ceapps
set CEUTILS=%APPSDIR%\ceutils

:: Virtual Environment where the dependencies reside
set PYVEGUI=C:\Users\%username%\wk_%username%\dev\python\py-dev\projects\ve_gui

cd %APPSDIR%
