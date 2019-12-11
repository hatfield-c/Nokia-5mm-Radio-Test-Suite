
if NOT exist "%~dp0\Python\python.exe" (
    start "" cmd /c "echo.&echo.&echo Python was not detected!&echo.&echo Please try running 'reinstall.bat' to install a local Python instance, or install one yourself in the 'Python/' folder.&echo.&echo.&echo(&pause"
    exit /b
)

.\Python\python.exe .\Application.py