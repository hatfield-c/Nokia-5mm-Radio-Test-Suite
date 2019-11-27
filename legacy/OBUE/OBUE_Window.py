# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0

#       standard library imports
import sys
sys.path.insert(0, '')
import tkinter as tk
import traceback

#       third party imports
import visa

#       local imports
import OBUE_Test as obue
import PeakPane as pkpn
from Support_Modules import InputPane as ip
from Support_Modules import SpecPane as spec
from Support_Modules import TestConfig as tcfg

class OBUE_Window():

    #OBUE window is the GUI and control mechanism for the OBUE testing module.
    #From this class, the gui shows and allows editing for the testing config.

    #OBUE_test handles calculation and OBUE_Script is exclusivly the obue base
    #SCPI scripts necessary to get the peak in span.

    peak_list_pane = None
    version = "2.0"
    def __init__(self):

        self.window = tk.Tk()
        self.window.title("OBUE BETA %s"% self.version)

        #parse for the configuration from the res file.
        self.test_conf = tcfg.TestConfig('OBUE')
        default_vals = self.test_conf.read_default_vals()

        #menu and associated buttons.
        menu = tk.Menu(self.window)
        menu.add_command(label = "View Setup", command = lambda:
                                            self.test_conf.view_config())


        view_menu = tk.Menu(menu)

        #adding toggling check button for iq swap usage.
        self.iq_swap_selected = tk.BooleanVar()
        self.iq_swap_selected.set(False)
        view_menu.add_checkbutton(label = "I\\Q Swap", onvalue = 1,
                                offvalue = 0, variable=self.iq_swap_selected)
        menu.add_cascade(label="I Q", menu=view_menu)

        self.window.config(menu = menu)

        entry_fields = ["Center Frequency(GHz)",
                            "Channel Bandwidth(MHz)",
                            "Resolution Bandwidth(Hz)",
                            "Sweep Time(s)"]

        self.input_pane = ip.InputPane(self.window, "OBUE Config",
                                            entry_fields, default_vals)
        self.input_pane.grid(column = 0, row = 1, rowspan = 6, columnspan = 2)



        #Calculate and Go buttons.
        #Calculate stops short of the actual sending command.
        #run test is calculate specs but at the ends it issues the test
        #command to the OBUE mod.
        calc_btn = tk.Button(self.window,
                                text = "Calculate",
                                bg = 'light blue',
                                command = lambda:
                                    self.calculate_specs())
        calc_btn.grid(column = 1, row = 7, sticky = tk.S + tk.E)

        go_button = tk.Button(self.window, text = "Run", bg = "green",
                                command = lambda: self.run_test() )
        go_button.grid(column = 1, row = 8, sticky = tk.S + tk.E)

        self.window.mainloop()#tkinter support


    def fill_spec_pane(self, configuration):
        #make pane and fill in all entries.
        self.spec_pane = spec.SpecPane(self.window,
                                        "Test Config", configuration)
        self.spec_pane.grid(column = 3, row = 0,
                                columnspan = 12, rowspan = 12,
                                sticky = tk.N + tk.W)


    def calculate_specs(self):

        if self.peak_list_pane:
            self.peak_list_pane.grid_forget()

        #Only calculate and update
        parameters = self.input_pane.get_parameters()

        #run the obue test with some stubbed out parameters.
        testcase = obue.OBUE_Test(
                        parameters = parameters,
                        testbench = self.test_conf.testbench_configuration)
        self.fill_spec_pane(testcase.return_configuration())


    def run_test(self):
        #build variables from the string vars.
        parameters = self.input_pane.get_parameters()

        #run the obue test with some stubbed out parameters.
        testcase =  obue.OBUE_Test(
                        parameters = parameters,
                        testbench = self.test_conf.testbench_configuration,
                        iq_swap = self.iq_swap_selected)

        self.fill_spec_pane(testcase.return_configuration())

        try:
            peak_list = testcase.run_test()
            self.display_results(peak_list)
        except visa.VisaIOError:
            print("ERROR: Visa IO Error")


    def display_results(self, peak_list):
        #display specialized peak frames
        self.peak_list_pane = pkpn.PeakPane(self.window, peak_list)
        self.peak_list_pane.grid(column = 0, row = 15,
                                columnspan = 10, rowspan = 4, sticky = tk.E)
        #and also open up some kind of tkinter resource.



if __name__ == '__main__':

    OBUE_Window()
