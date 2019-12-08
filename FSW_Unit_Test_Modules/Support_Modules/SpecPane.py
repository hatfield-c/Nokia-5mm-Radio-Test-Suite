# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0 

#       standard library imports
import tkinter as tk
#       third party imports

#       local imports

#generic listing widget in order to display any list of specs
#in the <label> <spec> format. Specpane uses labels for both fields.

class SpecPane(tk.Frame):

    def __init__(self, root, title, specification):

        tk.Frame.__init__(self, root, height = 20, width = 30, borderwidth = 3)
        self.config(relief = tk.GROOVE, padx = 2, pady = 2)

        title = tk.Label(self, text = title)
        title.grid(column = 0, row = 0)

        row_counter = 1

        #loop to create all label entry fields with field name as dic key
        for field in specification:
            label = tk.Label(self, text = field)
            spec = tk.Label(self, text = specification[field])

            label.grid(column = 0, row = row_counter, sticky = tk.N + tk.W)
            spec.grid(column = 1, row = row_counter, sticky = tk.N + tk.W,
                        columnspan = 3)
            row_counter += 1
        return
