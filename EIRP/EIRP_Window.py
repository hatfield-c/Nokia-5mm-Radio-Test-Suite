# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0

#   First party
import sys
sys.path.insert(0, '')

import tkinter as tk

#   Third party modules

#   Local modules
import EIRP_Test as eirp
from Support_Modules import InputPane as ip
from Support_Modules import SpecPane as sp
from Support_Modules import TestConfig as tcfg
from Support_Modules import ResultPane as rp

#GUI elements for the EIRP ACLR test
class EIRP_Window():

    version = "1.0"

    def __init__(self):

        #init window and name
        self.window = tk.Tk()
        self.window.title("EIRP BETA %s"% self.version)

        #parse for the configuration from the res file.
        self.test_conf = tcfg.TestConfig("EIRP")
        default_vals = self.test_conf.read_default_vals()

        #menu and associated buttons.
        menu = tk.Menu(self.window)
        menu.add_command(label = "View Setup", command = lambda:
                                            self.test_conf.view_config())
        self.window.config(menu = menu)

        entry_fields = ["Center Frequency(GHz)",
                        "TX BW", "Adjacent BW", "Alternate BW",
                        "Adjacent Spacing", "Alternate Spacing",
                        "User Std."]

        self.input_pane = ip.InputPane(self.window, "ACLR Config",
                                        entry_fields, default_vals)
        self.input_pane.pack()

        #add button
        go_button = tk.Button(self.window, text = "Run", bg = 'green',
                                command = lambda: self.run_test() )
        go_button.pack()

        #gui req
        self.window.mainloop()


    def run_test(self):
        #should get all data from input pane.
        params = self.input_pane.get_parameters()
        eirp_test = eirp.EIRP_Test(params,
                                    self.test_conf.testbench_configuration)
        feedback = eirp_test.run_test()
        #send feedback to gui
        self.spawn_res_pane(feedback)


    def spawn_res_pane(self, feedback):
        print(feedback)
        res_pane = sp.SpecPane(self.window, "ACLR Results", feedback)
        res_pane.pack()


if __name__ == '__main__':

    EIRP_Window()
