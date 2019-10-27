#Anthony Tang

#       standard library imports
import sys
sys.path.insert(0, '')
import tkinter as tk
import traceback

#       third party imports
import visa

#       local imports
import M_OBUE_Test as m_obue
import PeakPane as pkpn
from Support_Modules import InputPane as ip
from Support_Modules import SpecPane as spec
from Support_Modules import TestConfig as tcfg

#TODO:
#Hook up to test class.
#Develop grid layout for tkinter GUI elements for better formatting.

#input number of carriers
class M_OBUE_Window():

    version = "0.1"
    number_carriers = 0
    carriers = []


    def __init__(self):

        self.window = tk.Tk()
        self.window.title("M OBUE %s"% self.version)

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

        #resolution bandwidth and sweep time are universal to carriers
        entry_fields = ['Resolution Bandwidth(MHz)', 'Sweep Time(s)']
        self.shared_input_pane = ip.InputPane(self.window, title = None,
                                            entry_fields =entry_fields)
        self.shared_input_pane.grid(row =0, column = 0, padx = 1, pady =2)

        self.test_category = tk.StringVar(self.window, 'A')
        category_a_rdb = tk.Radiobutton(self.window, text = "A",
                                            variable = self.test_category,
                                            value = 1)
        category_b_rdb = tk.Radiobutton(self.window, text = "B",
                                            variable = self.test_category,
                                            value = 2)
        category_a_rdb.grid(row =1, column = 0, padx = 1, pady =2)
        category_b_rdb.grid(row =2, column = 0, padx = 1, pady =2)
        self.test_category.set(1)

        #add carrier btn
        add_carrier_btn = tk.Button(self.window,
                                    text = "Add Carrier",
                                    bg = "light blue",
                                    command = lambda: self.add_carrier_pane())
        add_carrier_btn.grid(row =3, column = 0, padx = 1, pady =2)

        #remove carrier btn
        remove_carrier_btn = tk.Button(self.window,
                                text = "Remove Carrier",
                                bg = "orange",
                                command = lambda: self.remove_carrier_pane() )
        remove_carrier_btn.grid(row =4, column = 0, padx = 1, pady =2)

        #
        run_test_btn = tk.Button(self.window,
                                text = "Run Test",
                                bg = "green",
                                command = lambda: self.run_test() )
        run_test_btn.grid(row =5, column = 0, padx = 1, pady =2)


        #add initial carrier pane.
        self.add_carrier_pane()

        self.window.mainloop() #tkinter loop


    def add_carrier_pane(self):

        title = "Carrier %d"%self.number_carriers
        entry_fields = ['Center Frequency(GHz)', 'Channel Bandwidth(MHz)']
        self.carriers.append(ip.InputPane(self.window, title, entry_fields))
        self.carriers[self.number_carriers].grid(row = 6+self.number_carriers, column = 0, padx = 1, pady =2)
        self.number_carriers += 1
        return


    def remove_carrier_pane(self):

        if self.number_carriers <= 1:
            #stub out button
            return

        #remove carrier.
        else:
            #remove from list
            remove = self.carriers.pop()
            #remove graphical pane
            remove.grid_forget()
            self.number_carriers -= 1 #decerement carriers


    def get_parameters(self):

        #return all parameters in the parameter dictionary.
        parameters = {}

        parameters['Category'] = self.test_category.get()
        parameters.update(self.shared_input_pane.get_parameters())
        for ip in self.carriers:
            carrier_name = ip.get_title()
            parameters[carrier_name] = ip.get_parameters()


        #print(parameters)
        return parameters


    def run_test(self):

        parameters = self.get_parameters()

        m_obue(parameters, testbench = self.testbench,
                    iq_swap = self.iq_swap_selected.get() )

        return


if __name__ == '__main__':

    M_OBUE_Window()
