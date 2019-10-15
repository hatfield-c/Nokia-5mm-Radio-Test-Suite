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

#input number of carriers
class M_OBUE_Window():

    version = "0.1"


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
