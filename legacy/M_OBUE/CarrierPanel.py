#Anthony Tang
#AnthonyJiangTang@gmail.com

import tkinter as tk
from Support_Modules import InputPane as ip


#Carrier panel is responsible for a single carrier's center
#frequency and the channel bandwidth.
class CarrierPanel(tk.Frame):

    def __init__(self, root, title, entry_fields, default_vals = None):

        tk.Frame.__init__(self, root, height = 20, width = 30, borderwidth = 3)
        self.config(relief = tk.GROOVE, padx = 2, pady = 2)

        ip.InputPane(root, title, entry_fields):
