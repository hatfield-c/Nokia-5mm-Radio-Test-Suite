title Run_tubecal


rem Start tubeCalibration using the appropriate Python interpreter
set CURRDIR=%~dp0
echo Running in %CURRDIR%
start "tubecal" "%CURRDIR%\python37-32\python.exe" "%CURRDIR%MAIN_tubeCalibration.py" %1 %2 %3 %4 %5 %6 %7 %8 %9
pause