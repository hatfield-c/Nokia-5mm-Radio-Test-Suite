import STATION_globals as gv

def start_log_file(filename):
    gv.LOGFILE = filename

def log(direction,*input_data):
    with open(gv.LOGFILE,'w') as f:
        for i in input_data:
            line = '{0} \t {1} \n'.format(direction,i)
            f.write(line)
            
            
    
    
