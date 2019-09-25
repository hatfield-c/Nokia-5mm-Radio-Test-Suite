# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git

#       standard library imports
import csv
#       third party imports
import visa
#       local imports


def write_command(instrument, command):
    instrument.write(command)
    print(command)
    return process_system_error(instrument)

def write_query(instrument, command):
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
attenuation = 14

#:MMEM:LOAD:DEM:CC1 'C:\R_S\Instr\user\NR5G\AllocationFiles\DL\Single Carrier\64QAM_cellid1_papr11_27_120kHz_100MHz.allocation'
#codify the allocation folder used by the program. (enforce however we can)

def aclr_5gnr_script():


    VisaResourceManager = visa.ResourceManager()
    # connect to analyzer
    Analyzer = VisaResourceManager.open_resource( INSTRUMENT )
    success = write_command( Analyzer, "*RST" )

    success = write_command( Analyzer, ":SYST:DISP:UPD ON" )
    success = write_command( Analyzer, ":INIT:CONT OFF" )

    #filename = "C:\\R_S\\instr\\user\\s2p\\Corrections\\bench4_7jun.s2p"
    #User-defined correction selected.  File name is selected by user or an external configuration file.
    #success = write_command( Analyzer, ":SENS:CORR:FRES:USER:STAT ON" )
    #success = write_command( Analyzer, ":SENS:CORR:FRES:INP1:USER:SLIS1:INS '%s'"% (filename) )

    # #New measurement window and title
    success = write_command( Analyzer, ":INST:CRE:NEW NR5G, '5G NR'" )
    #
    # #Center frequency based on radio's carrier frequency.
    success = write_command( Analyzer, ":SENS:FREQ:CENT 37050000000" )
    success = write_command( Analyzer, ":INP:ATT %s" % (str(attenuation)))
    success = write_command( Analyzer, ":INIT:CONT OFF" ) #single sweep mode

    success = write_command( Analyzer, ":CONF:NR5G:DL:CC1:DFR HIGH")
    #set f > 6Ghz

    #Analyzer
    success = write_command( Analyzer, "CONF:NR5G:DL:CC1:PLC:CID AUTO")

    #this errors when the file is wrong, add some kind of run guard or
    #a way to verify that the file is legitimate
    alloc_file = 'C:\\R_S\\Instr\\user\\NR5G\\AllocationFiles\\DL\\Single Carrier\\64QAM_cellID1_papr13_120KHz_100MHz.allocation'
    success = write_command( Analyzer, "MMEM:LOAD:DEM:CC1 '%s'"%(alloc_file) )

    # #Following lines executed under the MEAS CONFIG key -> CP/ACLR Config window
    # success = write_command( Analyzer, ":CALC:MARK:FUNC:POW:SEL ACP" )
    # success = write_command( Analyzer, ":CALC:MARK:FUNC:POW:PRES F2D100" )  #5G NR FR2 DL 100MHz pre-defined setup.  User-input?
    # success = write_command( Analyzer, ":SENS:POW:NCOR ON" )                #Noise correction on
    # success = write_command( Analyzer, ":SENS:POW:ACH:PRES ACP" )           #Not sure what the next two lines do
    # success = write_command( Analyzer, ":SENS:POW:ACH:PRES ACP" )
    # success = write_command( Analyzer, ":CALC:LIM:ACP:ACH:REL -26" )        #Setting ACP P/F limit in dBc
    # success = write_command( Analyzer, ":CALC:LIM:ACP:STAT ON" )            #Turning on P/F check
    #
    # #Trigger settings
    # success = write_command( Analyzer, ":TRIG:SEQ:SOUR EXT" )           #Trigger defined = External
    # success = write_command( Analyzer, ":TRIG:SEQ:LEV:EXT 1" )          #Trigger type defined as Level at 1.
    # success = write_command( Analyzer, ":SENS:SWE:EGAT ON" )            #Gated trigger turned ON, Edge mode
    # success = write_command( Analyzer, ":SENS:SWE:EGAT:HOLD 0.00036" )  #Trigger hold defined as 360us.  May change.
    # success = write_command( Analyzer, ":SENS:SWE:EGAT:LENG 0.0001" )   #Trigger length defined as 100us.  May change.
    # success = write_command( Analyzer, ":SENS:SWE:EGAT:CONT:STAT ON" )  #Gated Settings -> Cont. Gate ON
    #
    # #Sweep time defined im faily certain that sweep time cannot be defined in the 5gNR class.
    #success = write_command( Analyzer, ":SENS:SWE:TIME 25" )       #Sweep time set to 100ms.  May change.
    #
    # #Input attenuation manually defined at 30dB.  May change.
    # success = write_command( Analyzer, ":INP:ATT:AUTO OFF" )
    # success = write_command( Analyzer, ":INP:ATT 30" )
    #
    # #Offset and Reference Level defined.
    # #Offset (OFFS) based on measurement antenna gain.  This value may change and/or be read from an external file.
    # success = write_command( Analyzer, ":DISP:WIND:SUBW:TRAC:Y:SCAL:RLEV:OFFS 21" )
    # success = write_command( Analyzer, ":DISP:WIND:SUBW:TRAC:Y:SCAL:RLEV 50" )
    #
    # # added by SCPI recorder for synchronization
    success = write_command( Analyzer, ":INIT:IMM;*WAI" ) #sweep

    #Offset and Reference Level defined.
    #Offset (OFFS) based on measurement antenna gain.  This value may change and/or be read from an external file.
    offset = 21
    success = write_command( Analyzer, ":DISP:WIND:SUBW:TRAC:Y:SCAL:RLEV:OFFS %s"%(offset) )
    success = write_command( Analyzer, ":DISP:WIND:SUBW:TRAC:Y:SCAL:RLEV 50" )


    response = write_query( Analyzer, ":FETC:CC1:FRAM:SUMM:EVM:ALL:AVER?")
    print("EVM mean")
    print(response)
    response = write_query( Analyzer, ":FETC:CC1:FRAM:SUMM:FERR:AVER?;")
    print("Frequency Error Average")
    print(response)


    # back to local mode
    success = write_command(Analyzer, "@LOC")

    # cleanup
    Analyzer.close()
    VisaResourceManager.close()
