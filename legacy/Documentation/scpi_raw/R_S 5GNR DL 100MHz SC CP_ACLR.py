# python script created by FSW: 02:07:2019 16:28:01

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

def get_esr(instrument) :
    esr = instrument.query("*ESR?")
    return int(esr)


VisaResourceManager = visa.ResourceManager()

# connect to analyzer
Analyzer = VisaResourceManager.open_resource("TCPIP::192.168.255.200::inst0::INSTR")
success = write_command( Analyzer, "*CLS" )

success = write_command( Analyzer, ":SYST:DISP:UPD ON" )
success = write_command( Analyzer, ":INIT:CONT OFF" )

#User-defined correction selected.  File name is selected by user or an external configuration file.
success = write_command( Analyzer, ":SENS:CORR:FRES:USER:STAT ON" )
success = write_command( Analyzer, ":SENS:CORR:FRES:INP1:USER:SLIS1:INS 'C:\\R_S\\instr\\user\\s2p Corrections\\bench4_7jun.s2p'" )

#New measurement window and title
success = write_command( Analyzer, ":INST:CRE:NEW SANALYZER, %s"%("SC CP_ACLR") )

#Center frequency based on radio's carrier frequency.
success = write_command( Analyzer, ":SENS:FREQ:CENT 37050000000" )

#success = write_command( Analyzer, ":INIT:CONT OFF" )

#Following lines executed under the MEAS CONFIG key -> CP/ACLR Config window
success = write_command( Analyzer, ":CALC:MARK:FUNC:POW:SEL ACP" )
success = write_command( Analyzer, ":CALC:MARK:FUNC:POW:PRES F2D100" )  #5G NR FR2 DL 100MHz pre-defined setup.  User-input?
success = write_command( Analyzer, ":SENS:POW:NCOR ON" )                #Noise correction on
success = write_command( Analyzer, ":SENS:POW:ACH:PRES ACP" )           #Not sure what the next two lines do
success = write_command( Analyzer, ":SENS:POW:ACH:PRES ACP" )
success = write_command( Analyzer, ":CALC:LIM:ACP:ACH:REL -26" )        #Setting ACP P/F limit in dBc
success = write_command( Analyzer, ":CALC:LIM:ACP:STAT ON" )            #Turning on P/F check

#Trigger settings
success = write_command( Analyzer, ":TRIG:SEQ:SOUR EXT" )           #Trigger defined = External
success = write_command( Analyzer, ":TRIG:SEQ:LEV:EXT 1" )          #Trigger type defined as Level at 1.
success = write_command( Analyzer, ":SENS:SWE:EGAT ON" )            #Gated trigger turned ON, Edge mode
success = write_command( Analyzer, ":SENS:SWE:EGAT:HOLD 0.00036" )  #Trigger hold defined as 360us.  May change.
success = write_command( Analyzer, ":SENS:SWE:EGAT:LENG 0.0001" )   #Trigger length defined as 100us.  May change.
success = write_command( Analyzer, ":SENS:SWE:EGAT:CONT:STAT ON" )  #Gated Settings -> Cont. Gate ON

#Sweep time defined
success = write_command( Analyzer, ":SENS:SWE:TIME:AUTO OFF" )  #Sweep time manually defined
success = write_command( Analyzer, ":SENS:SWE:TIME 0.1" )       #Sweep time set to 100ms.  May change.

#Input attenuation manually defined at 30dB.  May change.
success = write_command( Analyzer, ":INP:ATT:AUTO OFF" )
success = write_command( Analyzer, ":INP:ATT 30" )

#Offset and Reference Level defined.
#Offset (OFFS) based on measurement antenna gain.  This value may change and/or be read from an external file.
success = write_command( Analyzer, ":DISP:WIND:SUBW:TRAC:Y:SCAL:RLEV:OFFS 21" )
success = write_command( Analyzer, ":DISP:WIND:SUBW:TRAC:Y:SCAL:RLEV 50" )

# added by SCPI recorder for synchronization
success = write_command( Analyzer, ":INIT:IMM;*WAI" )


# back to local mode
success = write_command(Analyzer, "@LOC")

# cleanup
Analyzer.close()
VisaResourceManager.close()
