from core.Interface import Interface
from core.inputs.legacy.fsw_file_navigator import fsw_file_navbox
import tkinter

class AllocationFile(tkinter.Toplevel):
    def __init__(self, parent, startingDir = None ):
        super().__init__(parent)
        self.parent = parent

        self.transient(self.parent)
        self.geometry("400x200")
        self.title("Allocation File Selector")
        #title = "Allocation File Selector", dimensions = { "height": 200, "width": 400 })

        if startingDir is None or startingDir == "":
            self.directory = "C:\\R_S\\Instr\\user\\NR5G"
        else:
            self.directory = startingDir

        self.columnconfigure(0, weight = 1)

        self.label = tkinter.Label(self, text = "Select Allocation File", font = "Helevetica 12 bold underline")
        self.label.grid(row = 0, column = 0, pady = 10)
        
        self.navbox = fsw_file_navbox(self, self.directory, "s2p")
        self.navbox.grid(row = 1, column = 0)

        self.submitButton = tkinter.Button(self, text = "Submit", padx = 10, command = lambda : self.submit())
        self.submitButton.grid(row = 2, column = 0, pady = 20)

        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda : self.cancel())
        self.wait_window(self)

    def submit(self):
        path = self.navbox.get_filepath()
        
        if path is not None and path != "":
            self.parent.path = path
        
        self.cancel()    

    def cancel(self):
        self.destroy()