# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0

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

def obue_script(test_name, sweep, rbw_MHz, start, stop, testbench,
                    reset = True, iq_swap = False):

        feedback = {} #feedback dictionary.
        feedback['Name'] = test_name
        feedback['Span Start'] = round(float(start), 5)
        feedback['Span Stop'] = round(float(stop), 5)

        #calc min number points. Cannot be lower than 1001
        rbw = int(rbw_MHz)* (10**6)
        span = (stop - start) * (10**9)
        points =  int(2*(span/rbw))
        if points < 1001:
            feedback['Number Points'] = 1001
        else:
            feedback['Number Points'] = points

        #used in offset calculations
        feedback['mAM Gain'] = testbench['Measured Antenna Gain']
        feedback['RA Gain'] = testbench['Radio Antenna Gain']

        print("Running test for \n%s : %s"%(str(start), str(stop)) )

        #convert start and stop units
        start = int(start * (10**9))
        stop = int(stop * (10**9))

        ######################################################################
        # S C P I : critical section
        ######################################################################
        VisaResourceManager = visa.ResourceManager()
        # connect to analyzer
        Analyzer = VisaResourceManager.open_resource(testbench['Instrument'])
        Analyzer.write_termination = '\n'
        Analyzer.clear()

        if reset is True:
            success = write_command( Analyzer, "*RST" )
        success = write_command( Analyzer, "*CLS" )
        success = write_command( Analyzer, ":SYST:DISP:UPD ON" )
        success = write_command( Analyzer, ":INIT:CONT OFF" )

        #38.50034

        ##TODO: Re enable Trigger, add back with
        ##some option for selection when working with the radio module.
        success = write_command( Analyzer, ":TRIG:SEQ:SOUR EXT" )
        success = write_command( Analyzer, ":TRIG:SEQ:LEV:EXT 1" )

        # #User-defined correction selected (Option K-544).
        # filepath = ("C:\\R_S\\instr\\user\\s2p Corrections\\"
        #                 + str(testbench['Testbench Correction']))

        filepath = "C:\\R_S\Instr\\user\\NR5G\\rftube3_26_40GHz_20Nov19.s2p"

        #File name is selected by user or an external configuration file.
        success = write_command( Analyzer, ":SENS:CORR:FRES:USER:STAT ON" )
        success = write_command( Analyzer,
                    ":SENS:CORR:FRES:INP1:USER:SLIS1:INS '%s'"%(filepath) )

        if iq_swap is True:
            success = write_command( Analyzer, ":SENS:SWAP ON")

        #Noise correction ON
        success = write_command( Analyzer, ":SENS:POW:NCOR ON" )

        #performs and measurement and waits for it to end.
        success = write_command( Analyzer, ":SENS:SWE:TIME:AUTO OFF" )
        success = write_command( Analyzer, ":SENS:SWE:TIME %s"%( sweep ))
        success = write_command( Analyzer, ":SENS:BAND:RES %s"%( rbw ))

        #TEST MODE: Execute with freq value 34 and 38,
        success = write_command( Analyzer, ":SENS:FREQ:STAR %s"%( start ))
        success = write_command( Analyzer, ":SENS:FREQ:STOP %s"%( stop ))
        success = write_command( Analyzer, ":SENS:WIND1:DET1:FUNC RMS" )
        success = write_command( Analyzer, ":TRIG:SEQ:SOUR IMM" )
        success = write_command( Analyzer,
                                    ":SENS:SWE:WIND:POIN %s"%
                                    (feedback['Number Points']) )

        # added by SCPI recorder for synchronization
        success = write_command( Analyzer, ":INIT:IMM;*WAI" )

        #set markers off
        success = write_command( Analyzer, ":CALC:MARK:AOFF" )

        #draw trace. Added explicity to fix the resolution pts mismatch
        success = write_query( Analyzer, ":TRAC1:DATA? TRACE1;*WAI" )

        #TODO:::USER INPUT OFFSET LEVEL?
        #I dont know where this goes but it needs to be somewhere on here
        success = write_command( Analyzer,
                                    ":DISP:WIND:SUBW:TRAC:Y:SCAL:RLEV:OFFS %s"
                                    %testbench['Measured Antenna Gain'])

        #turn on marker. Will find its own peak.
        success = write_command( Analyzer, ":CALC:MARK1 ON" )

        #Activates marker 1 and sets it to the peak of trace 1
        xval = write_query( Analyzer, ":CALC:MARK1:X?" )
        yval = write_query( Analyzer, ":CALC:MARK1:Y?" )

        #TRP = Raw Result + Meas. Ant Gain - Radio Ant Gain

        #So say you have a string representation of a frequency value in Hz
        #First strip the whitespace. Then convert to an int. Then
        #convert to GHz by dividing by 10^9, then convert that to a
        #float that is used in the formatting of a string with
        #4 decimal places.
        feedback['Pk Frequency'] = str(round(((float(xval[1].strip()))/(10**9)), 5))
        feedback['Pk Amplitude'] = str(round(float(yval[1].strip()), 1))

        #calculate TRP (raw + measure - radio )
        feedback['TRP'] = str(round((float(yval[1].strip())
                                            + feedback['mAM Gain']
                                            - feedback['RA Gain']), 1) )

        #cleanup
        success = write_command( Analyzer, "@LOC")  #back to local mode
        Analyzer.close()                            #close io channels
        VisaResourceManager.close()

        return feedback
