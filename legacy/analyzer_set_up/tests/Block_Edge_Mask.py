import tkinter as tk
import STATION_globals as STATION
import iolog

def set_variables_GUI(root,variables):

    BEM_frame = tk.Frame(root)
    BEM_frame.grid(row=1,column=0)
    #
    #--------these are the input variables and default values ----
    #
    variables.set_tk_input('span',"below span 1")
    variables.set_tk_input('center freq',39)
    variables.set_tk_input('TX BW',39)
    
    w = tk.OptionMenu(BEM_frame,
                      variables.tk_variables['span'],
                      "below span 1",
                      "below span 2",
                      "above span 2",
                      "above span 1")
    w.grid(row=1,column=1)

    display1= tk.Entry(BEM_frame,
                        textvariable = variables.tk_variables['center freq'])
    display1.grid(row=2,column=1,sticky='w')
    z= tk.Label(BEM_frame,text='center freq')
    z.grid(row=2,column=0,sticky='e')

    
    display2= tk.Entry(BEM_frame,
                        textvariable = variables.tk_variables['TX BW'])
    display2.grid(row=3,column=1,sticky='w')
    z= tk.Label(BEM_frame,text='transmit bandwidth')
    z.grid(row=3,column=0,sticky='e')
    
    #
    #create the buttons
    #
    
    set_button = tk.Button(BEM_frame,
                           text='SET',
                           command=lambda :set_values(BEM_frame,
                                                      variables))
    set_button.grid(row=0,column=0)

    cancel_button = tk.Button(BEM_frame,
                              text='CANCEL',
                              command=lambda :cancel(BEM_frame))
    cancel_button.grid(row=0,column=1)
    
    
    

def setup_analyzer(root,variables):
    # main function which sends all parameters to the analyzer
    pass

def set_values(frame,val):
    iolog.log('info', 'sending Block Edge Mask commands to analyzer')
    cf = float( val.get_tk_input('center freq'))
    bw = val.get_tk_input('span')
    txbw = float(val.get_tk_input('TX BW'))
    
    lowerChannelEdge = cf- (txbw/2)
    upperChannelEdge = cf + (txbw/2)
    
    if bw == 'below span 1':
        start_freq = lowerChannelEdge-(txbw*.1)
        stop_freq = lowerChannelEdge
        points = 20
    elif bw == 'below span 2':
        start_freq = 38.6
        stop_freq = lowerChannelEdge-(txbw*.1)
        points = 680
    elif bw == 'above span 1':
        start_freq = upperChannelEdge
        stop_freq = upperChannelEdge+(txbw*.1)
        points = 20
    elif bw == 'above span 2':
        start_freq = upperChannelEdge+(txbw*.1)
        stop_freq = 40
        points == 1880
    
    frame.grid_remove()
    STATION.DEVICES['ANALYZER'].set_spectrum_analyzer_mode()
    STATION.DEVICES['ANALYZER'].start_frequency('{0}G'.format(start_freq))
    STATION.DEVICES['ANALYZER'].stop_frequency('{0}G'.format(stop_freq))
    STATION.DEVICES['ANALYZER'].sweep_points(points)
    STATION.DEVICES['ANALYZER'].RBW('1M')
    STATION.DEVICES['ANALYZER'].VBW('AUTO')
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
