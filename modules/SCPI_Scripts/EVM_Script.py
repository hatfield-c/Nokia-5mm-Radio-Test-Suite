# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0

#       standard library imports
import csv
#       third party imports
import visa
import time
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
DELAY = 5

def evm_script(center_freq, attenuation,
                alloc_file, correction_file, cell_number,
                iq_swap = False, reset = True, bench_ip = None, qam = "64"):


    #convert center_freq from GHz to Hz
    center_freq_hz = int(float(center_freq)*(10**9))

    VisaResourceManager = visa.ResourceManager()
    # connect to analyzer
    instrument_ip = bench_ip
    Analyzer = VisaResourceManager.open_resource(("TCPIP::%s::inst0::INSTR"%instrument_ip))

    #unit housekeeping
    if reset is True:
        success = write_command( Analyzer, "*RST" )
    success = write_command( Analyzer, "*CLS" )
    success = write_command( Analyzer, ":SYST:DISP:UPD ON" )
    #single sweep (turns off continuous)
    success = write_command( Analyzer, ":INIT:CONT OFF" )


    #####################################################################
    # #User-defined correction selected (Option K-544).
    #filepath = parameters[]
    #File name is selected by user or an external configuration file.
    success = write_command( Analyzer, ":SENS:CORR:FRES:USER:STAT ON" )
    success = write_command( Analyzer,
                    ":SENS:CORR:FRES:INP1:USER:SLIS1:INS '%s'"%(correction_file) )

    #Noise correction ON
    success = write_command( Analyzer, ":SENS:POW:NCOR ON" )

    #####################################################################

    # #New measurement window and title
    success = write_command( Analyzer, ":INST:CRE:NEW NR5G, '5G NR'" )
    #Single sweep mode
    success = write_command( Analyzer, ":INIT:CONT OFF")
    success = write_command( Analyzer, ":DISP:WIND2:SUBW:SEL")
    success = write_command( Analyzer,
                                ":SENS:FREQ:CENT %s"%(str(center_freq_hz)))

    success = write_command( Analyzer, ":INP:ATT %s" % (str(attenuation)))
    #f>6ghz
    success = write_command( Analyzer, ":CONF:NR5G:DL:CC1:DFR HIGH")
    success = write_command( Analyzer, ":CONF:NR5G:DL:CC1:PLC:CID %s"%(str(cell_number)))

    #this errors when the file is wrong, add some kind of run guard or
    #a way to verify that the file is legitimate
    success = write_command( Analyzer, ":MMEM:LOAD:DEM:CC1 '%s'"%(alloc_file))

    #Sets cell id auto
    success = write_command( Analyzer, ":CONF:NR5G:DL:CC1:PLC:CID AUTO")

    if iq_swap is True:
        success = write_command( Analyzer, ":SENS:SWAP ON")

    success = write_command( Analyzer, ":CONF:NR5G:DL:CC1:SSBL:DET AUTO")
    success = write_command( Analyzer, ":CONF:NR5G:DL:CC1:FRAM1:BWP:DET AUTO")

    success = write_command( Analyzer, ":TRIG:SEQ:SOUR EXT" )
    success = write_command( Analyzer, ":TRIG:SEQ:LEV:EXT 1.4" )


    success = write_command( Analyzer, ";*WAI")
    #success = write_command( Analyzer, ":INIT:REFR;*WAI")

    success = write_command( Analyzer, ":INIT:IMM;" )
    time.sleep(DELAY)
    #wait for the 5gnr module to synchronize.
    #takes > 4 seconds. This may be the topic of adjustment.


    feedback = {} #feedback dictionary
    feedback['Center Frequency'] = center_freq

    try:
        #get pdsch, evm is split upon and allocation file dependent.
        #16, 64, and 256 qam
        if qam == "16":
            response = write_query( Analyzer, ":FETC:CC1:FRAM:SUMM:EVM:DSST:AVER?")
        elif qam == "64":
            response = write_query( Analyzer, ":FETC:CC1:FRAM:SUMM:EVM:DSSF:AVER?")
        elif qam == "256":
            response = write_query( Analyzer, ":FETC:CC1:FRAM:SUMM:EVM:DSTS:AVER?")
        #get responses for whatever the active pdsch is
        feedback['EVM Average'] = response[1].strip()

    except:
        #just get average because that wont error out
        #queries for evm and freq error.
        response = write_query( Analyzer, ":FETC:CC1:FRAM:SUMM:EVM:ALL:AVER?")
        #get responses for whatever the active pdsch is
        feedback['EVM Average'] = response[1].strip()

    response = write_query( Analyzer, ":FETC:CC1:FRAM:SUMM:FERR:AVER? ")
    print("Frequency Error Average")
    print(response)
    feedback['Frequency Error'] = response[1].strip()

    # back to local mode
    success = write_command(Analyzer, "@LOC")

    # cleanup
    Analyzer.close()
    VisaResourceManager.close()

    return feedback


if __name__ == '__main__':

    #run a EVM script sample
    print("evm")
