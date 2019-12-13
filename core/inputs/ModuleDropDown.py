import tkinter
import tkinter.ttk
import core.interfaces.Builder

from Config import _CONFIG_

class ModuleDropDown(tkinter.Frame):
    # Defines the numerical index of the passed arguments data, and what they store
    # args["data"] = [
    #    0          Default value already selected.
    # ]

    DEFAULT_STR = "<module|>"

    NONE_STR = "NONE"
    NO_DEFAULT_STR = "DEFAULT NOT FOUND"

    def __init__(self, args):
        root = args["root"]
        configData = args["config"]
        data = args["data"]
        orig = args["orig"]

        config = { }
        super().__init__(root, config)
        self.columnconfigure(0, weight = 1)

        self.defaultSelection = str(data[0])

        self.moduleList = []
        self.dropDown = tkinter.Frame(self)
        self.refreshButton = tkinter.Frame(self)

        self.rebuild()

    def rebuild(self):
        try:
            modules = _CONFIG_["modules"]
            moduleKeys = modules.keys()
            self.selectList = list(moduleKeys)
        except:
            self.selectList = []

        self.currentOption = tkinter.StringVar()

        self.dropDown.destroy()
        self.refreshButton.destroy()

        if self.defaultSelection == "" or self.defaultSelection is None:
            self.currentOption.set(self.NONE_STR)
        elif self.defaultSelection in self.selectList:
            self.currentOption.set(self.defaultSelection)
        else:
            self.currentOption.set(self.NO_DEFAULT_STR)

        if not self.selectList:
            options = { self.NONE_STR }
        else:
            options = self.selectList
        
        
        self.dropDown = tkinter.ttk.Combobox(self, textvariable = self.currentOption, values = options, state = "readonly")
        self.dropDown.grid(row = 0, column = 0, sticky = "ew")

    def get(self):
        option = self.currentOption.get()

        if option is None or option == self.NONE_STR or option == self.NO_DEFAULT_STR:
            return ""
        
        return str(option)

    def getRaw(self, value):
        rawString = "<"
        rawString += "module|"
        rawString += str(self.currentOption.get())
        rawString += ">"
        return rawString