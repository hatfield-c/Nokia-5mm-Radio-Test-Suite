import tkinter as tk
import STATION_globals as STATION
import iolog

def set_variables_GUI(root,variables):

    EIRP_ACLR_frame = tk.Frame(root)
    EIRP_ACLR_frame.grid(row=1,column=0)
    #
    #--------these are the input variables and default values ----
    #
    var=[['TX channel count','1'],
    ['ADJ channel count','2'],
    ['TX BW',95],
    ['ADJ BW',95],
    ['center freq',39.0],
    ['expected rf level',0], # 5db above sig level
    ['ref level offset',65], #from cal file
    ['gate delay','262u'],
    ['gate length','97u']]
    display = {}
    i = 0
    #
    # create the input fields
    #
    for name,default in var:
        variables.set_tk_input(name,default)
        i += 1
        display['in{0}'.format(i)] = tk.Entry(EIRP_ACLR_frame,
                                   textvariable = variables.tk_variables[name])
        display['in{0}'.format(i)].grid(row=i+1,column=1,sticky='w')
        z= tk.Label(EIRP_ACLR_frame,text=name)
        z.grid(row=i+1,column=0,sticky='e')

    #
    #create the buttons
    #

    set_button = tk.Button(EIRP_ACLR_frame,
                           text='SET',
                           command=lambda :set_values(EIRP_ACLR_frame,
                                                      variables))
    set_button.grid(row=0,column=0)

    cancel_button = tk.Button(EIRP_ACLR_frame,
                              text='CANCEL',
                              command=lambda :cancel(EIRP_ACLR_frame))
    cancel_button.grid(row=0,column=1)


def setup_analyzer(root,variables):
    # main function which sends all parameters to the analyzer
    pass

def set_values(frame,val):
    iolog.log('info', 'sending EIRP_ACLR commands to analyzer')
    frame.grid_remove()
    STATION.DEVICES['ANALYZER'].ACP('ACP')
    STATION.DEVICES['ANALYZER'].ACP_num_channels(val.get_tk_input('ADJ channel count'))
    STATION.DEVICES['ANALYZER'].power_channel_bandwidth(1,val.get_tk_input('TX BW'))
    STATION.DEVICES['ANALYZER'].adjacent_channel_bandwidth(1,val.get_tk_input('ADJ BW'))
    STATION.DEVICES['ANALYZER'].power_channel_spacing(1,'99.84M')
    STATION.DEVICES['ANALYZER'].adjacent_channel_spacing(1,'100M')
    STATION.DEVICES['ANALYZER'].frequency(val.get_tk_input('center freq'))
    STATION.DEVICES['ANALYZER'].span('1G')
    STATION.DEVICES['ANALYZER'].RBW('1M')
    STATION.DEVICES['ANALYZER'].VBW('AUTO')
    STATION.DEVICES['ANALYZER'].channel_power_mode(mode='ABS')
    STATION.DEVICES['ANALYZER'].channel_write_mode(write='WRIT')
    STATION.DEVICES['ANALYZER'].sweep_time_auto()
    STATION.DEVICES['ANALYZER'].sweep_mode(onoff='OFF')
    STATION.DEVICES['ANALYZER'].gated_trigger(source='EXT',
                                              delay=val.get_tk_input('gate delay'),
                                              mode='LEV',
                                              polatity='POS',
                                              length=val.get_tk_input('gate length'))
    STATION.DEVICES['ANALYZER'].trace_detector(trace=1,detector='RMS')


    #set the constants and calculated values
    pass
    #send the FSW commands
    pass

def cancel(frame):
    print ('cancelling')
    frame.grid_remove()
    # close the GUI window
    # exit
    pass
