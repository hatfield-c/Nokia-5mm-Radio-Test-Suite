The batching system operates on the assumption that the TEXT CORRECT attribute
values are defined for each of the attributes and corresponding data points.
The TEST attribute in column informs the function and parameters requested
by each test, the TEST attribute requires:

	Attribute to be <"TEST">
	Data to be < "OBUE" | "EIRP" | "5GNR" >

Extraneous data will be ignored. Data definitions must be in row directly after their attribute definitions.
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
	"TX BW"
	"Adjacent BW"
	"Alternate BW"
	"Adjacent Spacing"
	"Alternate Spacing"
	"User Std."
	>

"5GNR" required fields:
	<
	"Center Frequency (GHz)"
	"Attenuation (dBm)"
	"Allocation File"
	>
