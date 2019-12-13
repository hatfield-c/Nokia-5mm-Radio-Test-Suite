import tkinter
from core.interfaces.FSWFile import FSWFile as FSWInterface

class FSWFile(tkinter.Frame):
    # Defines the numerical index of the passed arguments data, and what they store
    # args["data"] = [
    #   0           The file extension that the browser looks for
    #   1           The default path of the field
    # ]

    DEFAULT = "<fsw_file|ALLOCATION|>"
    DEFAULT_BUILD = "<fsw_file|"

    def __init__(self, args):
        root = args["root"]
        configData = args["config"]
        data = args["data"]
        orig = args["orig"]

        config = { }
        super().__init__(root, config)
        self.columnconfigure(0, weight = 1)

        if len(data) < 1:
            self.fileType = "s2p"
        else:
            self.fileType = data[0]

        if len(data) < 2:
            self.path = ""
        else:
            self.path = data[1]
        
        self.fileField = tkinter.Entry(self)
        self.fileField.insert(index = 0, string = self.path)
        self.fileField.xview_moveto(1)
        self.fileField.grid(row = 0, column = 0, sticky = "ew")

        self.button = tkinter.Button(
            self, 
            text = u"\uD83D\uDCC1",
            command = lambda : self.getFSWFile(),
            borderwidth = 0,
            font = "Helevetica 12"
        )
        self.button.grid(row = 0, column = 1)

    def getFSWFile(self):
        filePath = self.fileField.get()
        fswInterface = FSWInterface(parent = self, startingDir = filePath, fileType = self.fileType)

        self.fileField.delete(0, 'end')
        self.fileField.insert(index = 0, string = self.path)

    def get(self):
        return self.fileField.get()

    def getRaw(self, value):
        rawString = "<"
        rawString += "fsw_file|"
        rawString += value
        rawString += ">"
        return rawString