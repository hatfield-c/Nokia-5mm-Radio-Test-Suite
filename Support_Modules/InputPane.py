# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0

import tkinter as tk

#input pane provides a generic tkinter widget that takes a
#list of string field values and returns a dictionary of
#those strings linked to the entry box values.
#<label><entry> format.

class InputPane(tk.Frame):

    def __init__(self, root, title = None, entry_fields = [],
                    default_vals = None):

        tk.Frame.__init__(self, root, height = 20, width = 30, borderwidth = 3)
        self.config(relief = tk.GROOVE, padx = 2, pady = 2)

        labels = {}
        entries = {}
        self.entry_strs = {}
        index = 0

        if title:
            #make a title label if one has been provided.
            self.title_lable = tk.Label(self, text = title)
            self.title_lable.grid(column = 0, row = index, sticky = tk.N + tk.W)
            index += 1

        for field in entry_fields:
            #print(field)
            self.entry_strs[field] = tk.StringVar(self)
            labels[field] = tk.Label(self, text = field)
            entries[field] = tk.Entry(self,
                                        textvariable = self.entry_strs[field])
            if(default_vals):
                self.entry_strs[field].set(default_vals[field])
            labels[field].grid(column = 0, row = index, sticky = tk.N + tk.W)
            entries[field].grid(column = 1, row = index, sticky = tk.N + tk.W)
            index += 1


    def get_parameters(self):

        print("Fetching parameters" )
        field_dic = {}
        for entry in self.entry_strs:
            var = self.entry_strs[entry].get()
            field_dic[entry] = var

        return field_dic

    def get_title(self):
        return self.title_lable

        #returns something.
