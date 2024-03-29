# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0

#       standard library imports
import csv
#       third party imports
import visa
#       local imports


def write_command(instrument, command):
    print(command)
    instrument.write(command)
    return process_system_error(instrument)

def write_query(instrument, command):
    print(command)
    buffer = instrument.query(command)
    bSuccess = process_system_error(instrument)
    return bSuccess, buffer

def process_system_error(instrument):
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


INSTRUMENT = "TCPIP::192.168.255.200::inst0::INSTR"

def evm_script(center_freq, attenuation,
                alloc_file, reset = True, qam = "64"):

    #convert center_freq from GHz to Hz
    center_freq_hz = int(float(center_freq)*(10**9))

    VisaResourceManager = visa.ResourceManager()
    # connect to analyzer
    Analyzer = VisaResourceManager.open_resource( INSTRUMENT )

    #unit housekeeping
    if reset is True:
        success = write_command( Analyzer, "*RST" )

    success = write_command( Analyzer, ":SYST:DISP:UPD ON" )
    #single sweep (turns off continuous)
    success = write_command( Analyzer, ":INIT:CONT OFF" )

    # #####################################################################
    # #User-defined correction selected (Option K-544).
    # filepath = ("C:\\R_S\\instr\\user\\s2p Corrections\\"
    #                 + str(testbench['Testbench Correction']))
    # #File name is selected by user or an external configuration file.
    # success = write_command( Analyzer, ":SENS:CORR:FRES:USER:STAT ON" )
    # success = write_command( Analyzer,
    #                 ":SENS:CORR:FRES:INP1:USER:SLIS1:INS '%s'"%(filepath) )
    #
    # #Noise correction ON
    # success = write_command( Analyzer, ":SENS:POW:NCOR ON" )
    #
    # #####################################################################

    # #New measurement window and title
    success = write_command( Analyzer, ":INST:CRE:NEW NR5G, '5G NR'" )
    #Single sweep mode
    success = write_command( Analyzer, ":INIT:CONT OFF")
    success = write_command( Analyzer,
                                ":SENS:FREQ:CENT %s"%(str(center_freq_hz)))

    success = write_command( Analyzer, ":INP:ATT %s" % (str(attenuation)))
    #f>6ghz
    success = write_command( Analyzer, ":CONF:NR5G:DL:CC1:DFR HIGH")

    #this errors when the file is wrong, add some kind of run guard or
    #a way to verify that the file is legitimate
    success = write_command( Analyzer, ":MMEM:LOAD:DEM:CC1 '%s'"%(alloc_file))

    #Sets cell id auto
    success = write_command( Analyzer, ":CONF:NR5G:DL:CC1:PLC:CID AUTO")

    iq_swap = True #temporary TODO
    if iq_swap is True:
        success = write_command( Analyzer, ":SENS:SWAP ON")

    success = write_command( Analyzer, ":INIT:IMM;*WAI" )

    feedback = {} #feedback dictionary
    feedback['Center Frequency'] = center_freq

    response = write_query( Analyzer, ":FETC:CC1:ISRC:FRAM:SUMM:EVM:DSSF:AVER?")

    # try:
    #     #get pdsch, evm is split upon and allocation file dependent.
    #     #16, 64, and 256 qam
    #     if qam is "16":
    #         response = write_query( Analyzer, ":FETC:CC1:FRAM:SUMM:EVM:DSST:AVER?")
    #     elif qam is "64":
    #         response = write_query( Analyzer, ":FETC:CC1:FRAM:SUMM:EVM:DSSF:AVER?")
    #     elif qam is "256":
    #         response = write_query( Analyzer, ":FETC:CC1:FRAM:SUMM:EVM:DSTS:AVER?")
    #     #get responses for whatever the active pdsch is
    #     feedback['EVM Average'] = response[1].strip()
    #
    # except:
    #     #just get average because that wont error out
    #     #queries for evm and freq error.
    #     response = write_query( Analyzer, ":FETC:CC1:FRAM:SUMM:EVM:ALL:AVER?")
    #     print("EVM mean")
    #     print(response)
    #     #get responses for whatever the active pdsch is
    #     feedback['EVM Average'] = response[1].strip()

    response = write_query( Analyzer, ":FETC:CC1:FRAM:SUMM:FERR:AVER?")
    print("Frequency Error Average")
    print(response)
    feedback['Frequency Error'] = response[1].strip()


    # back to local mode
    success = write_command(Analyzer, "@LOC")

    # cleanup
    Analyzer.close()
    VisaResourceManager.close()

    return feedback
