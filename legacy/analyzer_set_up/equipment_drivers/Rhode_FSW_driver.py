import sys
import re
import visa
import iolog

class FSW():
    def __init__(self,address):

        iolog.log("starting FSW instrument")
            
        self.rm = visa.ResourceManager()
        
        self.analyzer = self.rm.open_resource(address)   
        

            

            
    def send_command(self,commands):
        all_commands = commands.split(";")
        
        for command in all_commands:
            iolog.log ('-->',command)
            self.analyyzer.write(command)
            
            error_check = self.analyzer.query(":SYST:ERR?")
            x = re.findall('([0-9]*),(["].*["])',error_check)
            iolog.log ('<--',error_check)
        return x[0][0],x[0][1]
            
    def set_spectrum_analyzer_mode(self):
        ret = self.send_command(":INST SAN")
        
    def frequency(self,frequency):
        ret = self.send_command(":FREQ:CENT {0}".format(frequency))
        return ret
    
    def span(self,frequency):
        ret = self.send_command(":FREQ:SPAN {0}".format(frequency))
        return ret

    def start_freq(self,frequency):
        ret = self.send_command(":FREQ:STAR {0}".format(frequency))
        return ret
    
    def stop_freq(self,frequency):
        ret = self.send_command(":SOUR:STOP {0}".format(frequency))
        return ret

    def read(self,num,averages=1):
        self.send_command("CALC1:MARK{0}:MAX".format(num))
        ret=0
        for x in range(averages):
            ret += float(self.analyzer.query("CALC1:MARK{0}:Y?".format(num)))
        return ret/averages

    def RBW(self,rbw):
        ret = self.send_command("BAND {0}".format(rbw))
        return ret

    def VBW(self,vbw):
        ret = self.send_command("BAND:VID {0}".format(vbw))
        return ret

    def average(self,averages):
        ret = self.send_command("AVER:COUN {0}".format(averages))
        return ret

    def sweep(self,auto):
        ret = self.send_command("SWE:MODE {0}".format(auto))
        return ret
    
    def marker_2_peak(self):
        pk = self.send_command(':CALC:MARK1:MAX')
        return 1
    
    def marker(self,num,func):
        ret = self.send_command("CALC1:MARK{0}:TRAC 0".format(num))
        return ret

    def marker_band_power(self,state='ON',mode='POW',span='200.0M')
        ret = self.send_command('CALC:MARK:FUNC:BPOW {0}'.format(state))
        ret = self.send_command('CALC:MARK:FUNC:BPOW:MODE {0}'.format(mode))
        ret = self.send_command('CALC:MARK:FUNC:BPOW:SPAN {0}'.format(span))
        
    def ACP(self,acptype='ACP'):
        
        ret = self.send_command('CALC:MARK:FUNC:POW:SEL {0}'.format(acptype))
	#[CPOW] - channel power with single carrier
	#[MCAC]- multi carrier ACP
	#[GACL] - Gap ACLR Channel

    def ACP_num_channels(self,x):
        
        ret = self.send_command('SENS:POW:ACH:ACP {0}'.format(x))

    def channel_power_mode(self,mode='ABS'):

        ret = self.send_command('SENS:POW:ACH:MODE {0}'.format(mode))
        #[ABS or REL]
    def channel_write_mode(self,write='WRIT'):
        
        ret = self.send_command('CALC:MARK:FUNC:POW:MODE {0}'.format(write))
        #WRIT [WRIT or MAXH] (maxhold or clearwrite)

    def channel_power_reference_mode(self,mode='MAX'):
        ret = self.send_command('SENS:POW:ACH:REF:TXCH:AUTO {0}'.format(mode))

    def adjacent_channel_spacing(self,x):
        ret = self.send_command('SENS:POW:ACH:SPAC:ACH {0}'.format(x))

    def adjacent_channel_bandwidth(self,x):
        ret = self.send_command('SENS:POW:ACH:BAND:ACH {0}'.format(x))

    def power_channel_spacing(self,TXchan=1,spacing=1):
        ret = self.send_command('SENS:POW:ACH:SPAC:CHAN{0} {1}'.format(TXchan,spacing))

    def power_channel_bandwidth(self,TXchan,bandwidth='500M'):
        ret = self.send_command('SENS:POW:ACH:BAND:CHAN{0} {1}'.format(TXchan,bandwidth))
        
    def trigger_source(self,source='EXT'):
        ret = self.send_command('TRIG:SOUR {0}'.format(source))


    def trigger_delay(self,delay):
        ret = self.send_command('TRIG:HOLD {0}'.format(delay))

    def gated_trigger(self,source='EXT',delay=1.0,mode='LEV',polarity='POS',length='125n'):
        
        ret = self.send_command('SWE:EGAT ON')

        ret = self.send_command('SWE:EGAT:HOLD {0}'.format(delay))

        ret = self.send_command('SWE:EGAT:TYPE EDGE {0}'.format(mode))

        ret = self.send_command('SWE:EGATe:POL {0}'.format(polarity))

        ret = self.send_command('SWE:EGAT:LENG {0}'.format(length))

        ret = self.send_command('SWE:EGAT:SOUR {0}'.format(source))


    def sweep_points(self,points):
        
        ret = self.send_command('SWE:POIN {0}'.format(points))

    def sweep_time_auto(self):
        ret = self.send_command('SWE:TIME:AUTO ON')

    def sweep_mode(self,onff='ON'):
        ret = self.send_command('INIT:CONT {0}'.format(onoff))


    def trace_detector(self,trace =  1,detector='RMS'):
        ret=self.send_command('DET{0} {1}'.format(trace,detector))

    def input_ref_level(self,level):
        ret = self.send_command('DISP:WIND:TRAC:Y:RLEV {0}'.format(level))

    def input_ref_level_offset(self,offset):
        ret = self.send_command('DISP:WIND:TRAC:Y:RLEV:OFFS {0}'.forget(offset))

    def input_RF_atten(self,atten):
        ret = self.send_command('INP:ATT {0}'.format(atten))

   
if __name__ == ("__main__"):
    analyzer_address = "GPIB0::20::INSTR"
    ana=MXA(address,'MARKER',0,0)
    
    for x in range(50):
        
        print (ana.read_level())
    
                
    
