from Config import _CONFIG_
from core.Interface import Interface
from core.inputs.legacy.fsw_file_navigator import fsw_file_navbox
import tkinter

class FSWFile(tkinter.Toplevel):
    def __init__(self, parent, startingDir = None, fileType = ".s2p"):
        super().__init__(parent)
        self.parent = parent
        self.fileType = fileType

        self.transient(self.parent)
        self.geometry("400x200")
        self.title("Allocation File Selector")
        self.iconbitmap(_CONFIG_["favicon_path"])

        if startingDir is None or startingDir == "":
            self.directory = "C:\\"
        else:
            self.directory = startingDir

        self.columnconfigure(0, weight = 1)

        self.label = tkinter.Label(self, text = "Select FSW File of type: " + str(self.fileType), font = "Helevetica 12 bold underline")
        self.label.grid(row = 0, column = 0, pady = 10)
        
        self.navbox = fsw_file_navbox(self, self.directory, str(self.fileType))
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