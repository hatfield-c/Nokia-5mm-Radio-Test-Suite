#Anthony tang


import tkinter as tk
import visa

#pyvisa methods
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


instrument_ip = "192.168.255.200"
#SCPI script. Given a directory filepath and a type, return all listings in the
#filepath directory of the specificed file type and subdirectories
def get_directory(filepath, filetype):

    ######################################################################
    # S C P I : critical section
    ######################################################################
    VisaResourceManager = visa.ResourceManager()
    # connect to analyzer
    Analyzer = VisaResourceManager.open_resource("TCPIP::%s::inst0::INSTR"%instrument_ip)
    Analyzer.write_termination = '\n'
    Analyzer.clear()

    catalog = write_query( Analyzer, ":MMEM:CAT? '%s' "%filepath )
    if catalog[0]:
        #process catalog[1], a string of file names seperated by comma
        items = catalog[1].split(",")
        items = [item.replace('\'', '').strip() for item in items]

        #classify whether file or not by seraching for extension.
        nav_list = []
        for item in items:
            itm_tup = item.split(".")
            if len(itm_tup) > 1:
                if itm_tup[1] == filetype:
                    nav_list.append(item)
            #directory, so add
            else:
                nav_list.append(item)
        return(nav_list)


#defines a frame that allows forward and backward navigation of the FSW
#using pyvisa
class fsw_file_navbox(tk.Frame):

    menu = None

    #initialize the filebox from parent frame, starting directory, and
    #the string file extension of the type we're searchign for
    #eg: (s2p, ALLOCATION, txt)
    def __init__(self, root, starting_directory, filetype):

        tk.Frame.__init__(self, root, height = 20, width = 30, borderwidth = 3)
        self.config(relief = tk.GROOVE, padx = 2, pady = 2)

        self.filetype = filetype
        self.filepath = starting_directory
        self.update_menu()


    def update_menu(self):

        #destroy previous menu
        if self.menu:
            self.menu.forget()

        directory_list = [".."]
        directory_list += get_directory(self.filepath, self.filetype)
        self.file_name = tk.StringVar(self)
        self.file_name.set("select file")
        self.menu = tk.OptionMenu(self, self.file_name, *directory_list)

        self.file_name.trace("w", self.callback)
        self.menu.pack()


    def up_level(self, new_dir):
        print("cd %s"%new_dir)
        self.filepath += ("\\%s"%new_dir)
        print(self.filepath)


    def down_level(self):
        print("cd .. ")
        #split on \\
        path_list = self.filepath.split("\\")
        if len(path_list) > 1: #guard to ensure C/ stays in path
            leaving = path_list.pop()
        print("leaving ", leaving)

        newpath = ""
        print(path_list)
        for node in path_list:
            newpath += node
            newpath += "\\"
        self.filepath = newpath[:-1] #also remove the extra hanging \


    def callback(self, *args):
        selection = self.file_name.get()
        self.file_name.set(selection)
        print("selection", selection)
        if(selection == ".."):
            self.down_level()
            self.update_menu()

        #truncate the last extension from the filepath
        #if the file is a directory, open that directory.
        else:
            #split the file name to determine whether directory of
            #file
            if len(selection.split(".")) <= 1:
                #found directory. Append directory to the filepath
                self.up_level(selection)
                #get the new directory
                self.update_menu()


    #returns the current filepath.
    def get_filepath(self):
        if self.file_name.get() == "select file":
            print("Select file before proceeding")
            return False

        file = (self.filepath + "\\" + self.file_name.get())
        print(file)
        return file


#Sample test case for the filefinder
if __name__ == '__main__':

    window = tk.Tk()
    window.title("file finder")

    starting_directory = "C:\\R_S\\Instr\\user\\NR5G"
    navbox = fsw_file_navbox(window, starting_directory, "s2p")
    navbox.pack()

    #gui req
    window.mainloop()
