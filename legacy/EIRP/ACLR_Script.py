# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0


#DEPRERCATED, see EIRP script for current version.


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
    return bSuccesss

def get_esr(instrument) :
    esr = instrument.query("*ESR?")
    return int(esr)


def aclr_script(center_freq = 37050000000, carrier_bw = 99840000,
                    acp_bw = 99840000, carrier_acp_spacing = 100000000,
                    pf_limit = -26, rbw = 1000000, attenuation = 30):

    # connect to analyzer
    VisaResourceManager = visa.ResourceManager()
    Analyzer = VisaResourceManager.open_resource("TCPIP::192.168.255.200::inst0::INSTR")
    success = write_command( Analyzer, "*CLS" )

    success = write_command( Analyzer, ":SYST:DISP:UPD ON" )
    success = write_command( Analyzer, ":INIT:CONT OFF" )

    #User-defined correction selected (Option K-544).  File name is selected by user or an external configuration file.
    success = write_command( Analyzer, ":SENS:CORR:FRES:USER:STAT ON" )
    correction_file = "C:\\R_S\\instr\\user\\s2p Corrections\\bench4_7jun.s2p"
    success = write_command( Analyzer,
                ":SENS:CORR:FRES:INP1:USER:SLIS1:INS '%s'"%(correction_file) )

    #New measurement window and titl
    success = write_command( Analyzer, ":INST:CRE:NEW SAN, 'ACLR'" )
    success = write_command( Analyzer, ":INIT:CONT OFF" )

    #Center frequency based on radio's carrier frequency.
    success = write_command( Analyzer, ":SENS:FREQ:CENT %s"%(center_freq) )


    #MEAS key -> Select measurement type
    success = write_command( Analyzer, ":CALC:MARK:FUNC:POW:SEL ACP" )

    #Following lines executed under the MEAS CONFIG key -> CP/ACLR Config window
    success = write_command( Analyzer, ":SENS:POW:ACH:ACP 1" )                  #Single carrier, one ACP channel
    success = write_command( Analyzer, ":SENS:POW:NCOR ON" )                    #Noise correction ON
    success = write_command( Analyzer, ":SENS:POW:ACH:BWID:CHAN1 %s"%(carrier_bw))    #99.84MHz Carrier BW
    success = write_command( Analyzer, ":SENS:POW:ACH:BWID:ACH %s"%(acp_bw))      #99.84MHz ACP BW
    success = write_command( Analyzer, ":SENS:POW:ACH:SPAC:CHAN1 %s"%(carrier_acp_spacing))   #100MHz Spacing btwn Carrier and ACP frequency

    success = write_command( Analyzer, ":CALC:LIM:ACP:ACH:REL:STAT ON" )        #Setting ACP limit to Relative
    success = write_command( Analyzer, ":CALC:LIM:ACP:ACH:REL %s"%pf_limit)            #Setting ACP P/F limit in dBc
    success = write_command( Analyzer, ":CALC:LIM:ACP:STAT ON" )                #Turning on P/F check

    #RBW defined
    success = write_command( Analyzer, ":SENS:BAND:RES %s"%(rbw) )   #1MHz RBW.  Value may change based on 3gPP standards

    #Sweep time defined
    success = write_command( Analyzer, ":SENS:SWE:TIME:AUTO OFF" )  #Sweep time manually defined
    success = write_command( Analyzer, ":SENS:SWE:TIME 0.1" )       #Sweep time set to 100ms.  May change.

    #Trigger setup
    success = write_command( Analyzer, ":TRIG:SEQ:SOUR EXT" )           #Trigger defined = External
    success = write_command( Analyzer, ":TRIG:SEQ:LEV:EXT 1" )          #Trigger type defined as Level at 1.0V
    success = write_command( Analyzer, ":SENS:SWE:EGAT ON" )            #Gated trigger turned ON, Edge mode
    success = write_command( Analyzer, ":SENS:SWE:EGAT:HOLD 0.00036" )  #Trigger hold defined as 360us.  May change.
    success = write_command( Analyzer, ":SENS:SWE:EGAT:LENG 0.0001" )   #Gate Settings -> Gate length = 100us
    success = write_command( Analyzer, ":SENS:SWE:EGAT:CONT:STAT ON" )  #Gated Settings -> Cont. Gate ON
    success = write_command( Analyzer, ":SENS:FREQ:CENT %s"% (center_freq) )  #Freqency set to center frequency

    #Input attenuation manually defined at 30dB.  May change.
    success = write_command( Analyzer, ":INP:ATT:AUTO OFF" )
    success = write_command( Analyzer, ":INP:ATT %s"%(attenuation) )

    #Offset and Reference level defined.
    #Offset (OFFS) based on measurement antenna gain.
    #This value may change and/or be read from an external file.
    success = write_command( Analyzer, ":DISP:WIND:SUBW:TRAC:Y:SCAL:RLEV:OFFS 21")
    success = write_command( Analyzer, ":DISP:WIND:SUBW:TRAC:Y:SCAL:RLEV 50" )

    #query the results for the ACLR measurement
    response = write_query( Analyzer, "CALC:MARK:FUNC:POW:RES? ACP" )
    feedback['ACP'] = response[1]

    # back to local mode
    success = write_command(Analyzer, "@LOC")


if __name__ == '__main__':

    aclr_script()
