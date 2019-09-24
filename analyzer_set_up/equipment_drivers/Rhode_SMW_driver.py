import sys
sys.path.append('..\modules')
import re
import visa

class SMW():

    def __init__(self,address):
            
        self.rm = visa.ResourceManager()
        
        self.analyzer = self.rm.open_resource(address)   
        

            

            
    def send_command(self,commands):
        all_commands = commands.split(";")
        
        for command in all_commands:
            self.analyzer.write(command)
            
            error_check = self.analyzer.query(":SYST:ERR?")
            x = re.findall('([0-9]*),(["].*["])',error_check)
            
        return x[0][0],x[0][1]
            

    def read(self,command):
        level = self.analyzer.query(command)
        return float(level)
    
    def write(self,command):
        level = self.analyzer.write(command)
        return float(level)
    
    def frequency(self,frequency):
        ret = self.analyzer.write(":SOUR:FREQ {0}".format(frequency))
        return ret
    
    def level(self,level):
        ret = self.analyzer.write(":SOUR:POW {0}".format(level))
        self.output("ON")
        return ret
    
    def output(self,state):
        ret = self.analyzer.write(":OUTP {0}".format(state))
        return ret

    def modulation(self,path,state):
        ret = self.analyzer.write(":SOUR{Path}:IQ:STAT {stat}".format(Path=1,stat=state))
        return ret

        
    
if __name__ == ("__main__"):
    analyzer_address = "GPIB0::20::INSTR"
    ana=MXA(address,'MARKER',0,0)
    
    for x in range(50):
        
        print (ana.read_level())
    
                
    
