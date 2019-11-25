#Anthony tang


import tkinter as tk
#Use scpi to fetch the directory and return a list of it's components
import visa

def write_command(instrument, command) :
    instrument.write(command)
    return process_system_error(instrument)

def write_query(instrument, command) :
    buffer = instrument.query(command)
    bSuccess = process_system_error(instrument)
    return bSuccess, buffer

def process_system_error(instrument) :
    bSuccess = True
    EsrErrorMask = 0x3C
    if ((get_esr(instrument) & EsrErrorMask) != 0) :
        print(instrument.query(":SYST:ERR?"))
        instrument.write("*CLS")
        bSuccess = False
    return bSuccess

def get_esr(instrument):
    esr = instrument.query("*ESR?")
    return int(esr)

#OBUE script is the base case unit for the OBUE test.
#It contains the SCPI script that needs to be run.
#Init takes the parameters necessary to determine peak in span on test
#and the continued

def get_directory(filepath):

    ######################################################################
    # S C P I : critical section
    ######################################################################
    VisaResourceManager = visa.ResourceManager()
    # connect to analyzer
    Analyzer = VisaResourceManager.open_resource("TCPIP::192.168.255.200::inst0::INSTR")
    Analyzer.write_termination = '\n'
    Analyzer.clear()

    catalog = write_query( Analyzer, ":MMEM:CAT? '%s' "%filepath )
    if catalog[0]:
        #process catalog[1], a string of file names seperated by comma
        items = catalog[1].split(",")
        print(items)
        return(items)

def callback(one, two):
    print(one, two)
    print("CALLED")

hostname = "192.168.255.200"
user = "FSW50-103349\\Instrument"
password = "894129"

class fsw_file_navbox(tk.Frame):

    def __init__(self, root):

        tk.Frame.__init__(self, root, height = 20, width = 30, borderwidth = 3)
        self.config(relief = tk.GROOVE, padx = 2, pady = 2)

        filepath = "C:\\R_S\\Instr\\user\\NR5G"
        OPTIONS = get_directory(filepath)


        file_name = tk.StringVar(self)
        file_name.set("select file")
        menu = tk.OptionMenu(self, file_name, *OPTIONS)

        down_button = Menubutton(self, label "__Menu__")
        file_name.trace("w", callback)

        menu.pack()




if __name__ == '__main__':

    window = tk.Tk()
    window.title("filefinder")

    navbox = fsw_file_navbox(window)
    navbox.pack()


    #gui req
    window.mainloop()
