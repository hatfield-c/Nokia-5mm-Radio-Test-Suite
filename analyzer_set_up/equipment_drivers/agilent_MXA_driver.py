import sys
sys.path.append('..\modules')
import re
import visa

class MXA():

    def __init__(self,
                 address='',
                 measurement_type='MARKER',
                 freq=39.002,
                 level=-39):
        if measurement_type == 'MARKER':
            self.query_string = ';:CALC:MARK1:Y?'
            commandString = ':SWE:TIME:AUTO OFF;:SWE:TIME .001'
##            commandString = ":FREQ:CENTER %f" % (float(freq)*1e9)
##            commandString += ";:FREQ:SPAN %f" % (500000)
##            commandString += ";:DISP:WIND:TRAC:Y:RLEV %s;:DISP:WIND:TRAC:Y:RLEV:OFFS %f" % (level,0)
##            commandString += ";:POW:ATT:AUTO OFF"
##            commandString += ";:TRAC1:TYPE WRIT"
##            commandString += ";:TRAC1:UPD ON"
##            commandString += ";:TRAC1:DISP ON"
##            commandString += ";:SWE:POIN %d" % (1001)
##            commandString += ";:DET:TRAC1:AUTO ON"
##            commandString += ";:DISP:WIND:TRAC:Y:SPAC LOG;:DISP:WIND:TRAC:Y:PDIV 10"
##            commandString += ";:INIT:CONT ON"
##            commandString += ";:CALC:MARK1:MODE POS"
##            commandString += ";:CALC:MARK1:X:READ:AUTO ON"
##            commandString += ";:CALC:MARK1:FCO ON"
##            commandString += ";:CALC:MARK1:FCO:GAT:AUTO ON"
        elif measurement_type == 'CHANNEL POWER':
            self.query_string = ':FETC:CHP1?'
            commandString = ''
            #:CALC:CHP:MARK%d:X?;:CALC:CHP:MARK%d:Y?;
            #commandString = ";:CONF:CHP" 
            #commandString += ";:FREQ:CENTER %f"% (float(freq)*1e9)
            
        self.rm = visa.ResourceManager()
        
        self.analyzer = self.rm.open_resource(address)   
        send_error, theError = self.send_command(commandString)

            

            
    def send_command(self,commands):
        all_commands = commands.split(";")
        print all_commands
        for command in all_commands:
            self.analyzer.write(command)
            print command
            error_check = self.analyzer.query(":SYST:ERR?")
            x = re.findall('([0-9]*),(["].*["])',error_check)
            
        return x[0][0],x[0][1]
            

    def read_level(self):
        level = self.analyzer.query(self.query_string)
##        lev=level.split(";")
##        print lev
##        return float(lev[1])
        return float(level)
    
    def marker_2_peak(self):
        pk = self.analyzer.write(':CALC:MARK1:MAX')
        return 1
        
    
if __name__ == ("__main__"):
    analyzer_address = "GPIB0::20::INSTR"
    ana=MXA(address,'MARKER',0,0)
    
    for x in range(50):
        
        print ana.read_level()
    
                
    
