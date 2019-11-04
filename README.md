# Application Info #

## Python Data ##

Version: 3.7.4
Location: Python37-32

Package Dependencies:

	- tkinter
		UI Framework upon which the application is build
	- Pillow
		Images processing framework based off the PIL (Python-Imaging-Library) package

## Upgrading Python ##

When upgrading the local Python version, install it to a new folder, and make sure to have the 'pip' and 'tkinter' modules installed as a part of the installation procedure (Should be offered as an option during install of Python. If not, then you'll have to figure out how to install them manually, or find a new installer). Then, run the following command on the Window command line:
	
	{PATH TO PYTHON}\python.exe {PATH TO PYTHON}\scripts\pip.exe install Pillow

This will install the Pillow library into the upgraded Python instance, and all dependency requirements should be met.

## Running the Application from Python ##

With the local Python instance, you do not need to have Python installed/configured on the machine you wish to run the application from. Simply run the following command from the Windows command line:

	{PATH TO PYTHON}\python.exe {PATH TO APP}\core\Application.py

# FSW Automation 5G #

## OBUE Multicarrier Module Addition ##

maintained by Anthony.Tang@nokia.com

Last Changed: 8/08/2019 Anthony Tang
Python Version: 3.7.0

To run use:    

    .\Python37-32\python.exe FSW_interface.py

    run_obue.bat
    run_eirp.bat
    run_5GNR.bat

Full installation of python is in here so just run
all commands with the internal python installation

    .\Python37-32\python.exe <commands go here>


Run to check all installed python dependencies.

    .\Python37-32\python.exe -m pip list

By specifying the python instance we bypass system path things and ensure
the embedded environment is used along with those dependent modules.

### OBUE Test ###

- Centre Frequency in GHz
- Channel Bandwidth in MHz
- Resolution Bandwidth
- Sweep Time
- Optional Test Bench Struct


### EIRP Test ###

- TX Bandwidth
- Adjacent BW
- Alternate BW
- Adjacent Spacing
- Alternate Spacing
- User Standard
- Optional Test Bench Struct


### 5GNR Signal Quality Test ###

- Centre Frequency in GHz
- Attenuation dBm
- Allocation File (Absolute Filepath)


## Default Values ##

Default values for test files are defined in the "Resources" directory. They are
stored as .xlsx files and are accessed though the testconf class. The file
access is name dependent and stored in the TestConfig.py file and are defined
as relative file paths.

Changing the default values will involve opening up the excel file and editing
the data field. Attribute fields are dictionary use sensitive so the
attribute column should not be edited.  

## Test Configuration ##

The test bench is defined in the testbench.xlsx file and defines attributes
relevant to the test set up and radio hardware, as compared to the individual
test case.

Editing the testbench configuration can be done directly in the .xlsx file.
Additional data fields can be added and will receive logging.

## Results ##

Test results come back in GUI form, as well as an auto generated .csv file
that can be found in the "Results" directory.


## Batch Test Input Parser #

The batching system operates on the assumption that the TEXT CORRECT
attribute values are defined for each of the attributes and corresponding
data points. The TEST attribute in column informs the function and parameters
requested by each test, the TEST attribute requires:

    Attribute to be <"TEST">
    Data to be < "OBUE" | "EIRP" | "5GNR" >

Extraneous data will be ignored. Data definitions must be in row directly
after their attribute definitions.
Additional values will be logged, but not considered in the test operation.

"OBUE" required fields:
	<
	"Center Frequency(GHz)",
	"Channel Bandwidth(MHz)"
	"Resolution Bandwidth(Hz)"
	"Sweep Time(s)"
	>

"EIRP" required fields:
	<
  "Center Frequency(GHz)"
	"TX BW"
	"Adjacent BW"
	"Alternate BW"
	"Adjacent Spacing"
	"Alternate Spacing"
	"User Std."
	>

"5GNR" required fields:
	<
	"Centre Frequency(GHz)"
	"Attenuation(dBm)"
	"Allocation File"
	>
