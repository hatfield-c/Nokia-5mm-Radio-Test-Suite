#Use scpi to fetch the directory and return a list of it's components
import visa

def write_command(instrument, command) :
    instrument.write(command)
    return process_system_error(instrument)

def write_query(instrument, command) :
    buffer = instrument.query(command)
    bSuccess = process_system_error(instrument)
    return bSuccess, buffer

def process_system_error(instrument) :
    bSuccess = True
    EsrErrorMask = 0x3C
    if ((get_esr(instrument) & EsrErrorMask) != 0) :
        print(instrument.query(":SYST:ERR?"))
        instrument.write("*CLS")
        bSuccess = False
    return bSuccess

def get_esr(instrument):
    esr = instrument.query("*ESR?")
    return int(esr)

#OBUE script is the base case unit for the OBUE test.
#It contains the SCPI script that needs to be run.
#Init takes the parameters necessary to determine peak in span on test
#and the continued

def get_directory(filepath):

    ######################################################################
    # S C P I : critical section
    ######################################################################
    VisaResourceManager = visa.ResourceManager()
    # connect to analyzer
    Analyzer = VisaResourceManager.open_resource("TCPIP::192.168.255.200::inst0::INSTR")
    Analyzer.write_termination = '\n'
    Analyzer.clear()

    catalog = write_query( Analyzer, ":MMEM:CAT? '%s' "%filepath )
    if catalog[0]:
        return(catalog[1])

    

if __name__ =='__main__':

    get_directory("C:\\R_S\\Instr\\user\\NR5G")
