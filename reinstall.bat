@echo off

set check="n"
set /p check="Reinstall? (y/n): "

if NOT "%check%" == "y" (
    set check="n"
    exit /b
)

if exist "%~dp0\Python\python.exe" (
    .\Python\python-3.7.0-install.exe /uninstall
)

.\Python\python-3.7.0-install.exe /passive TargetDir="%~dp0\Python" installLauncherAllUsers=0
.\Python\python.exe -m pip install pyvisa 
.\Python\python.exe -m pip install pyvisa-py

set check="n"