import tkinter
from Config import _CONFIG_

class Radio(tkinter.Frame):
    # Defines the numerical index of the passed arguments data, and what they store
    # args["data"] = [
    #    0          Each index of the positional arguments
    #    1          represent a title for an option that 
    #    2          can be chosen for the radio button. 
    #    ...        There is presently no limit to radio
    #    N          radio options.
    # ]

    DEFAULT = "<radio|OPTION_1|OPTION_2|OPTION_3|etc.>"

    def __init__(self, args):
        root = args["root"]
        configData = args["config"]
        data = args["data"]
        orig = args["orig"]

        config = { }
        super().__init__(root, config)
    
        if len(data) < 1:
            return

        self.selection = tkinter.IntVar()
        self.selection.set(1)
        self.radios = []

        self.radioFrame = tkinter.Frame(self)
        self.radioFrame.grid(row = 0, column = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

        i = 1
        for option in data:
            radio = tkinter.Radiobutton(
                self.radioFrame,
                text = option,
                indicatoron = 0,
                padx = 0,
                variable = self.selection,
                value = i,
                background = _CONFIG_["color_secondary"]
            )
            radio.grid(row = 0, column = i - 1, padx = 3)

            self.radios.append(radio)

            i += 1

    def get(self):
        return self.selection.get()

    def getRaw(self, value):
        rawString = "<"
        rawString += "radio|"

        for radio in self.radios:
            rawString += radio.cget("text") + "|"

        print(rawString)
        rawString = rawString[0:-1]
        rawString += ">"
        print(rawString)
        return rawString