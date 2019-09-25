# python script created by FSW: 02:07:2019 17:56:28

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


success = write_command( Analyzer, ":SENS:FREQ:CENT 37050000000" )  #Define trigger center frequency. Variable set by user/radio carrier frequency
success = write_command( Analyzer, ":TRIG:SEQ:SOUR EXT" )           #External trigger source

success = write_command( Analyzer, ":TRIG:SEQ:LEV:EXT 0.5" )        #Trigger level defined to 0.5V.  Variable set by end user.

success = write_command( Analyzer, ":SENS:SWE:EGAT ON" )            #Gated trigger ON   
success = write_command( Analyzer, ":SENS:SWE:EGAT:TYPE EDGE" )     #Gated trigger set to EDGE
success = write_command( Analyzer, ":SENS:SWE:EGAT:POL POS" )       #Trigger Source Slope = Rising
success = write_command( Analyzer, ":SENS:SWE:EGAT:HOLD 0.0004" )   #Gated trigger delay defined to 400us. Variable set by end user.
success = write_command( Analyzer, ":SENS:SWE:EGAT:LENG 0.0001" )   #Gated trigger length defined to 100us. Variable set by end user.

success = write_command( Analyzer, ":SENS:SWE:EGAT:CONT:STAT ON" )      #Continous Gate ON
success = write_command( Analyzer, ":SENS:SWE:EGAT:CONT:PLEN 0.01" )    #Continous Gate Length 10ms.  Controlled varialbe (XML file?)
success = write_command( Analyzer, ":SENS:SWE:EGAT:CONT:PCO 10" )       #Continous Gate Period Count set to 10.  Controlled varialbe (XML file?)

# back to local mode
success = write_command(Analyzer, "@LOC")

# cleanup
Analyzer.close()
VisaResourceManager.close()
