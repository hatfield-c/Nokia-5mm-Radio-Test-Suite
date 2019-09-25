# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0 

#       standard library imports
import tkinter as tk
#       third party imports

#       local imports

class PeakPane(tk.Frame):

    #peaklist packed as a list of dictionaries.
    def __init__(self, root, peak_list):

        #establish self object frame
        tk.Frame.__init__(self, root, height = 20, width = 20, borderwidth = 3)
        self.config(relief = tk.GROOVE, padx = 2, pady = 2)

        x_index = 0
        y_index = 0

        if peak_list[0]:
            for key in peak_list[0].keys():
                attr = tk.Label(self, text = key)
                attr.grid(column = x_index, row = y_index)
                x_index += 1

            #zero x and y for the start of the non key dic print
            x_index = 0
            y_index += 1
            for peak in peak_list:
                for key in peak:
                    peak_field_label = tk.Label(self,
                                        text = (peak[key]))
                    peak_field_label.grid(column = x_index,
                                            row = y_index,
                                            sticky = tk.W)
                    x_index += 1
                #
                y_index += 1 #increment y
                x_index = 0  #reset x for the next set of attribute values.
