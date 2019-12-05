import tkinter
from core.interfaces.AllocationFile import AllocationFile as AllocationInterface

class AllocationFile(tkinter.Frame):
    # Defines the numerical index of the passed arguments data, and what they store
    POSITIONAL_DATA = [
    #    0          The default path of the field
    ]

    DEFAULT = "<allocation_file|>"

    def __init__(self, args):
        root = args["root"]
        configData = args["config"]
        data = args["data"]
        orig = args["orig"]

        config = { }
        super().__init__(root, config)
        self.columnconfigure(0, weight = 1)

        if len(data) < 1:
            self.path = ""
        else:
            self.path = data[0]
        
        self.fileField = tkinter.Entry(self)
        self.fileField.insert(index = 0, string = self.path)
        self.fileField.xview_moveto(1)
        self.fileField.grid(row = 0, column = 0, sticky = "ew")

        self.button = tkinter.Button(
            self, 
            text = u"\uD83D\uDCC1",
            command = lambda : self.getAllocationFile(),
            borderwidth = 0,
            font = "Helevetica 12"
        )
        self.button.grid(row = 0, column = 1)

    def getAllocationFile(self):
        filePath = self.fileField.get()
        allocationInterface = AllocationInterface(parent = self, startingDir = filePath)

        self.fileField.delete(0, 'end')
        self.fileField.insert(index = 0, string = self.path)

    def get(self):
        return self.fileField.get()

    def getRaw(self, value):
        rawString = "<"
        rawString += "allocation_file|"
        rawString += value
        rawString += ">"
        return rawString