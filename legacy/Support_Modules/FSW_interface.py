# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0

#deprecated


#       standard library imports
import tkinter as tk

#       third party imports
import visa

#       local imports
import OBUE_Test as obue
import OBUE_Window as obue_gui
import EIRP_Window as eirp_gui


#fsw interface can be bypassed in
#favor of launching each module individually
class FSW_interface():

    def __init__(self):

        root = tk.Tk()
        root.title("FSW")

        obue_btn = tk.Button(root, text = "OBUE",
                                command = lambda: self.launch_obue() )
        obue_btn.pack()

        eirp_btn = tk.Button(root, text = "EIRP EVM",
                                command = lambda: self.launch_eirp_evm() )
        eirp_btn.pack()

        root.mainloop() #gui requirement

    def launch_obue(self):
        obue = obue_gui.OBUE_Window()

    def launch_eirp_evm(self):
        eirp = eirp_gui.EIRP_Window()
        return

if __name__ == "__main__":

    FSW_interface()
