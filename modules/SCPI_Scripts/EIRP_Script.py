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

#center carrier anchor frequency spacing


INSTRUMENT = "TCPIP::192.168.255.200::inst0::INSTR"

#sweep time, BW, gate delay,
def eirp_script(center_freq, tx_bw, adj_bw, adj_space, user_standard,
                    testbench, reset = True):

    feedback = {}

    center_freq = float(center_freq.strip()) * (10 ** 9) #convert to Hz from GHz

    #Units are taken in hz.
    tx_bw = float(tx_bw * (10**6)) #convert bw values from MHz to Hz
    adj_bw = float(adj_bw * (10**6))
    alt_bw = float(alt_bw * (10**6))
    adj_space = float(adj_space * (10**6))
    alt_space = float(alt_space * (10**6))

    VisaResourceManager = visa.ResourceManager()
    # connect to analyzer
    Analyzer = VisaResourceManager.open_resource( INSTRUMENT )
    Analyzer.write_termination = '\n'
    Analyzer.clear()

    #external trigger 1

    #resolution bandwidth 1 MHZ
    #RF Attenuation
    #ref level 50
    #ref level offset = 21
    #turn on external reference
    #RBW 1kHz

    #restart
    if reset is True:
        success = write_command( Analyzer, "*RST" )

    #prepare mesurement
    success = write_command( Analyzer, ":CALC:MARK:FUNC:POW:SEL ACP" )

    #external trigger at 1.4 V
    success = write_command( Analyzer, ":TRIG:SEQ:SOUR EXT" )
    success = write_command( Analyzer, ":TRIG:SEQ:LEV:EXT 1.4" )

    #set sweep time to 100ms
    success = write_command( Analyzer, ":SENS:SWE:TIME 0.1" )


    #user selects GSM standard. (make this different)
    #success = write_command( Analyzer, "CALC:MARK:FUNC:POW:PRES GSM")

    #Center frequency based on radio's carrier frequency.
    success = write_command( Analyzer, ":SENS:FREQ:CENT %s"%(center_freq))
    #set up channels
    success = write_command( Analyzer, ":POW:ACH:TXCH:COUN 1" )
    #name channel
    success = write_command( Analyzer, ":POW:ACH:NAME:CHAN1 'TX Channel'" )
    success = write_command( Analyzer, ":POW:ACH:NAME:ACH 'Adj'" )


    #define bandwidth for channel bandwidth. tx_bw
    success = write_command( Analyzer, "POW:ACH:BWID:CHAN1 %s"%(tx_bw) )

    #define bandwidth for adjacent channels
    success = write_command( Analyzer, ":POW:ACH:BWID:ACH %s"%(adj_bw) )

    #define bandwidth for alternate channels
    #success = write_command( Analyzer, "POW:ACH:BWID:ALT1 %s"%(alt_bw) )

    #define distance from center of tx_ch to center of first alt_ch
    #define bandwidth for adjacent channels
    success = write_command( Analyzer, ":POW:ACH:SPAC:ACH %s"%(adj_space) )

    #define distance from center of transmission
    #to center of first alternate channel
    #success = write_command( Analyzer, "POW:ACH:SPAC:ALT1 %s"%(alt_space) )


    #####################################################################
    #User-defined correction selected (Option K-544).
    filepath = "C:\\R_S\\instr\\user\\NR5G\\rftube3_26_40GHz_20Nov19.s2p"
    #File name is selected by user or an external configuration file.
    success = write_command( Analyzer, ":SENS:CORR:FRES:USER:STAT ON" )
    success = write_command( Analyzer,
                    ":SENS:CORR:FRES:INP1:USER:SLIS1:INS '%s'"%(filepath) )

    #Noise correction ON
    success = write_command( Analyzer, ":SENS:POW:NCOR ON" )

    #####################################################################

    #Selecting Reference Channel, set to be relative.
    #success = write_command( Analyzer, ":POW:ACH:MODE:REL" )
    #define the tx_ch as the reference used
    success = write_command( Analyzer, ":POW:ACH:REF:TXCH:MAN 1" )

    #continous gate
    success = write_command(Analyzer, ":SWE:EGAT:CONT:STAT ON")
    #gate delay
    success = write_command(Analyzer, ":SWE:EGAT:HOLD 100us")

    #SAVE SETTINGS AS A USER standard
    success = write_command( Analyzer, (":CALC:MARK:FUNC:POW:STAN:SAVE '%s'"
                                            %(user_standard)) )
    #DEFINING WEIGHTING FILTERS
        #INSERT MORE COMMANDS (optional)


    #Performing the Measurement
    success = write_command( Analyzer, ":POW:ACH:PRES ACP;*WAI" ) #sync
    #determine the ideal reference level for the measurement
    success = write_command( Analyzer, ":POW:ACH:PRES:RLEV;*WAI" )
    success = write_command( Analyzer, ":INIT;*WAI" )
    #initiate new measurement and wait until finished

    #query the results for the ACLR measurement
    response = write_query( Analyzer, ":CALC:MARK:FUNC:POW:RES? ACP" )
    acp_str = response[1].strip()
    #seperate acp_str along its comma seperated value.
    acp_tup = acp_str.split(",")

    feedback['carrier'] = acp_tup[0]
    feedback['adj lower'] = acp_tup[1]
    feedback['adj upper'] = acp_tup[2]

    print(response) #check what format ACLR returns in

    #Power of the transmission channels
    #power of the adjacent channel (lower, upper)
    #power of the alternate channels (lower, upper)

    #shutdown stuff
    success = write_command( Analyzer, "@LOC" )  #back to local mode
    Analyzer.close()                             #close io channels
    VisaResourceManager.close()

    return feedback


if __name__ == "__main__":
    eirp = eirp_script(100, 30, 20, 30, 40, 15, "Name")
