@echo off
set check = "n"
if exist "%~dp0\Python\python.exe" (
    set /p check="Uninstall? (y/n): "
)

if NOT "%check%" == "y" (
    set check = "n"
    exit /b    
)

.\Python\python-3.7.0-install.exe /uninstall
set check = "n"