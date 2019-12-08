# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0 

#result frame (deprecated) to act as a universal widget interpreting Results
#dicitionaries into gui readable elements

import tkinter as tk

class ResultPane(tk.Frame):

    def __init__(self, root, result_list):

        tk.Frame.__init__(self, root, height = 10, width = 20, borderwidth = 3)
        self.config( relief = tk.SUNKEN, padx = 2, pady = 2)

        #print results in a tkinter friendly format

        for result in result_list:
            lbl = tk.Label(self, text = result)

        #define header labels
        header = result_list[0].keys() #get dictionary keys.
        header_labels = {}

        y = 0
        for field in header:
            print(str(field) + "\t")
            header_labels[field] = tk.Label(self, text = field)
            header_labels[field].grid(row = 0, column = y)
            y += 1 #use y val axis index.


        for dic in result_list:
            for field in dic:
                pass
