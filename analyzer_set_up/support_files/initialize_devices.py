import sys
import tkinter as tk
from tkinter import messagebox as tkMessageBox
import imp
import os
import re


import STATION_globals as gv
import fileStuff as fs

class Device():
    def __init__(self,name,device_file_name):
        self.name = name
        self.reference = None
        self.error = 0

        device_list = fs.spreadsheet_file_2_array(device_file_name)

        for a_device in device_list:
            if (not re.match('^[!# @*]',a_device[0])
                and
                a_device[0] != ''
                and
                (device == 'ALL' or a_device[0] == device)):
                
                try:
                    
                    found = imp.find_module(a_device[2])
                    module = imp.load_source(a_device[2],found[1])
                    exec('self.reference = module.{0}({1})'.format(a_device[1],a_device[3]))
                    
                
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    print ('error initializing {0} in {1} {2}'.format(a_device[0],a_device[1],exc_type))
                    tkMessageBox.showerror('ERROR',"error initializing {0} {1}".format(a_device[0],exc_type))
                    num_errors += 1
            
    

        
def initialize_device(device='ALL',
                      device_file = gv.DEVICE_FILE,
                      classname='',
                      drivercode='',
                      parameters=''):
    num_errors=0
    
    if device_file != '' :
        
        device_list = fs.spreadsheet_file_2_array(device_file)
        for a_device in device_list:
            if (not re.match('^[!# @*]',a_device[0])
                and
                a_device[0] != ''
                and
                (device == 'ALL' or a_device[0] == device)):
                
                try:
                    print ('initializing '+a_device[0])
                    found = imp.find_module(a_device[2])
                    module = imp.load_source(a_device[2],found[1])
                    print (str(module)+'.%s(%s)'%(a_device[1],a_device[3]))
                    exec ('gv.DEVICES[a_device[0]]=module.%s(%s)'%(a_device[1],a_device[3]))
                
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    print ('error initializing %s in %s %s'%(a_device[0],a_device[1],exc_type))
                    tkMessageBox.showerror('ERROR',"error initializing %s %s"%(a_device[0],exc_type))
                    num_errors += 1
    else:
        try:
            found = imp.find_module(drivercode)
            module = imp.load_source(drivercode,found[1])
            exec ('gv.DEVICES[device]=module.%s(%s)'%(classname,parameters))
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print ('error initializing %s %s'%(device,exc_type))
            num_errors +=1
    return gv.DEVICES

if __name__ == '__main__':
    pass
