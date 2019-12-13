
## System Requirements ##

### Python Data ###
Version: 3.7.0

Location: {PATH TO APP}\Python

Package Dependencies:

	- pyvisa

### Auto-Install Python ###

To run the Nokia™ Test Suite Manager, you will need to have Python 3.7.0 installed and configured with the tkinter, pyvisa, and pyvisa-py libraries. An installer is included in this TSM distribution, and is located at ‘Python/python-3.7.0-install.exe’. An internet connection is required to install the 3rd party pyvisa libraries, while tkinter usually comes default with python.

An automated install script is included with this distribution, which handles the python installation and library dependency downloads automatically. Run the file ‘reinstall.bat’, and the automated script will do its job. Rerunning the script after an install will result in a fresh reinstall procedure, with the previous python instance being uninstalled automatically

An 'uninstall.bat' script is included as well as a convenience. Please see documentation for debugging info on the auto-install process.

## Upgrading Python ##

When upgrading the Python instance used by this application, uninstall the old instance using the 'uninstall.bat' script.

Then, download the Python .EXE Windows Installer from the Python website with the desired version, and put it in the Python/ folder. Modify the 'reinstall.bat' and 'uninstall.bat' files to reference the new installer .exe file, and then 'reinstall.bat'.

## Running the Application from Python ##

There are two options to run this application. Make sure Python is installed using the 'reinstall.bat' script before proceeding, or use your own Python instance.

For the normal option, double click the 'run.bat' file, which will instantiate the application using Python.

For debugging, open a command prompt window and navigate to the root directory of the application. Then run the following command:

	{PATH TO PYTHON}\python.exe .\core\Application.py

Where {PATH TO PYTHON} is replaced with the path to the Python instance that will run the application (default is .\Python\python.exe).
