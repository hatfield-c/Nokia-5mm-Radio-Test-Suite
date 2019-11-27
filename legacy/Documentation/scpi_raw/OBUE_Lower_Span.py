# python script created by FSW: 01:07:2019 15:50:30

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


#i dont actually know why or if you're supposed to do this.
Analyzer.write_termination = '\n'
Analyzer.clear()

success = write_command( Analyzer, "*RST" )

success = write_command( Analyzer, "*CLS" )

success = write_command( Analyzer, ":SYST:DISP:UPD ON" )

success = write_command( Analyzer, ":INIT:CONT OFF" )

#success = write_command( Analyzer, ":TRIG:SEQ:SOUR EXT" ) 

#success = write_command( Analyzer, ":TRIG:SEQ:LEV:EXT 1" )

# added by SCPI recorder for synchronization
success = write_command( Analyzer, ":INIT:IMM;*WAI" )

success = write_command( Analyzer, ":SENS:SWE:TIME:AUTO OFF" )
#SET SWEEP TIME GATE TODO:::

success = write_command( Analyzer, ":SENS:BAND:RES 1000000" )

#TEST MODE: Execute with freq value 34 and 38,
success = write_command( Analyzer, ":SENS:FREQ:STAR 34000000000" )

success = write_command( Analyzer, ":SENS:FREQ:STOP 38000000000" )

success = write_command( Analyzer, ":SENS:WIND1:DET1:FUNC RMS" )

success = write_command( Analyzer, ":TRIG:SEQ:SOUR IMM" )

success = write_command( Analyzer, ":SENS:SWE:WIND:POIN 2001" ) 
#calculated value Num points TODO:

# back to local mode
success = write_command(Analyzer, "@LOC")

# cleanup
Analyzer.close()
VisaResourceManager.close()
