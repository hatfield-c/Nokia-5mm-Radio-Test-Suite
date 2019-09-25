# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0

import sys
sys.path.insert(0, '')

import tkinter as tk

import EVM_5GNR_Test as evm
from Support_Modules import InputPane as ip
from Support_Modules import SpecPane as sp
from Support_Modules import TestConfig as tcfg
from Support_Modules import ResultPane as rp


#GUI elements for the 5GNR signal quality tests.
class EVM_5GNR_Window():

    version = "1.0"

    def __init__(self):

        self.window = tk.Tk()
        self.window.title("5GNR BETA %s"% self.version)

        #parse for the configuration from the res file.
        self.test_conf = tcfg.TestConfig("5GNR")
        default_vals = self.test_conf.read_default_vals()

        #menu and associated buttons.
        menu = tk.Menu(self.window)
        menu.add_command(label = "View Setup", command = lambda:
                                            self.test_conf.view_config())
        self.window.config(menu = menu)

        #add input pane consisting of independent
        #values needed in the 5gnr test.
        entry_fields = ["Center Frequency(GHz)",
                            "Attenuation(dBm)",
                            "Allocation File",
                            "QAM PDSCH"]
        #i wanted to make this radio buttons but lets get it working first
        #because ive got like 2 hours of gainful employment left

        self.input_pane = ip.InputPane(self.window,
                                        "EVM Frequency Error",
                                        entry_fields, default_vals)
        self.input_pane.pack()

        go_button = tk.Button(self.window, text = "Run", bg = "green",
                                command = lambda: self.run_test())
        go_button.pack()

        #gui req
        self.window.mainloop()


    def run_test(self):
        parameters = self.input_pane.get_parameters()
        test = evm.EVM_Test(parameters, self.test_conf.testbench_configuration)
        feedback = test.run_test()
        self.spawn_spec_pane(feedback)


    def spawn_spec_pane(self, feedback):
        spec_pane = sp.SpecPane(self.window, "Results EVM", feedback)
        spec_pane.pack()


if __name__ == '__main__':

    EVM_5GNR_Window()
