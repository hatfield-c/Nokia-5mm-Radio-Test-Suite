version='X1.0'
import sys
rootDir=sys.path[0]

sys.path.append(rootDir+'\\data')
sys.path.append(rootDir+'\\support_files')
sys.path.append(rootDir+'\\configs')
sys.path.append(rootDir+'\\equipment_drivers')
sys.path.append(rootDir+'\\tests')
import tkinter as tk

#
# user modules here
#
import STATION_globals as STATION
import critical_variable_handler as val
import iolog


STATION.DEVICE_FILE = rootDir+'\\configs\\devices.txt'
STATION.ROOT_DIR = rootDir
import initialize_devices as DE


def kill_python(root,saved_values):
    
    saved_values.save_critical_values(File='defalt.txt')     
    root.destroy()


def test_eirp_aclr(root,variables):
    import EIRP_ACLR as aclr
    aclr_setup_variables = aclr.set_variables_GUI(root,variables)
    
    return aclr_setup_variables


def test_blockEdgeMask(root,variables):
    import Block_Edge_Mask as BEM
    bem_setup_variables = BEM.set_variables_GUI(root,variables)


def test_EESS(root,variables):
    import EESS
    eess_setup_variables = EESS.set_variables_GUI(root,variables)

root = tk.Tk()
root.title('software version: %s'%version)

main_frame = tk.Frame(root)
main_frame.grid(row=0,column=0)
iolog.start_log_file('log.txt')
saved_values = val.critical_variables(File='defalt.txt')

#
# prepare devices
#

#DE.initialize_device(device='ANALYZER')

#
# MAIN BUTTONS
#

ACLR = tk.Button(main_frame,
                         text="EIRP-ACLR",
                         command=lambda :test_eirp_aclr(root,saved_values))
                         
ACLR.grid(row=1,column=0)

#

quit_button = tk.Button(main_frame,
                        text="QUIT",
                        command=lambda:kill_python(root,saved_values))
quit_button.grid(row=0,column=2)

#

BEM = tk.Button(main_frame,
                        text="Block Edge Mask",
                        command=lambda:test_blockEdgeMask(root,saved_values))
BEM.grid(row=1,column=2)

#

EESS = tk.Button(main_frame,
                        text="EESS",
                        command=lambda:test_EESS(root,saved_values))
EESS.grid(row=1,column=3)

root.mainloop()
        
