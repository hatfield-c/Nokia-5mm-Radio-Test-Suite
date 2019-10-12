import tkinter as tk
import STATION_globals as STATION
import iolog

EESS_band = [
    "band 1 -- 23.6 to 24 GHz",
    "band 2 -- 31.3 to 31.8 GHz",
    "band 3 -- 36 to 37 GHz",
    "band 4 -- 50.2 to 50.4 GHz",
    "band 5 -- 52.6 to 54.25 GHz",
    "band 6 -- 86 to 92 GHz"
    ]
def set_variables_GUI(root,variables):

    EESS_frame = tk.Frame(root)
    EESS_frame.grid(row=1,column=0)
    #
    #--------these are the input variables and default values ----
    #
    variables.set_tk_input('span',"band 1 -- 23.6 to 24 GHz")
    
    w = tk.OptionMenu(EESS_frame,
                      variables.tk_variables['span'],
                      EESS_band[0],
                      EESS_band[1],
                      EESS_band[2],
                      EESS_band[3],
                      EESS_band[4],
                      EESS_band[5],)
    w.grid(row=1,column=1)
    
    #
    #create the buttons
    #
    
    set_button = tk.Button(EESS_frame,
                           text='SET',
                           command=lambda :set_values(EESS_frame,
                                                      variables))
    set_button.grid(row=0,column=0)

    cancel_button = tk.Button(EESS_frame,
                              text='CANCEL',
                              command=lambda :cancel(EESS_frame))
    cancel_button.grid(row=0,column=1)
    
    
    


def set_values(frame,val):
    iolog.log('info', 'sending EESS commands to analyzer')
    frame.grid_remove()

    bandstring = val.get_tk_input('span')
    startstop = bandstring.split(' ')
    
    
    STATION.DEVICES['ANALYZER'].marker_band_power('ON')
    STATION.DEVICES['ANALYZER'].set_spectrum_analyzer_mode()
    STATION.DEVICES['ANALYZER'].start_frequency('{0}G'.format(startstop[3]))
    STATION.DEVICES['ANALYZER'].stop_frequency('{0}G'.format(startstop[5]))
    STATION.DEVICES['ANALYZER'].sweep_points(points)
    STATION.DEVICES['ANALYZER'].RBW('1M')
    STATION.DEVICES['ANALYZER'].VBW('AUTO')
    STATION.DEVICES['ANALYZER'].channel_power_mode(mode='ABS')
    STATION.DEVICES['ANALYZER'].channel_write_mode(write='WRIT')
    STATION.DEVICES['ANALYZER'].sweep_time_auto()
    STATION.DEVICES['ANALYZER'].sweep_mode(onoff='ON')
    STATION.DEVICES['ANALYZER'].trace_detector(trace=1,detector='RMS')
    STATION.DEVICES['ANALYZER'].gated_trigger(source='EXT',
                                              delay=val.get_tk_input('gate delay'),
                                              mode='LEV',
                                              polatity='POS',
                                              length=val.get_tk_input('gate length'))

                                              
    
    
    #set the constants and calculated values
    pass
    #send the FSW commands
    pass

def cancel(frame):
    
    frame.grid_remove()
    # close the GUI window
    # exit
    pass
