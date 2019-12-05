import tkinter
from Config import _CONFIG_

class CollectionDropDown(tkinter.Frame):
    # Defines the numerical index of the passed arguments data, and what they store
    POSITIONAL_DATA = [
    #    0          The type of the collection to get data from.
    #    1          Default value already selected.
    ]

    DEFAULT_RUN_STR = "<sequence_select|run|>"
    DEFAULT_BENCH_STR = "<sequence_select|bench|>"

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

        self.collectionType = str(data[0])
        self.defaultSelection = str(data[1])

        self.rebuild()

    def rebuild(self):
        suite = _CONFIG_["app_root"].suite
        builder = suite.getWorkspace(key = self.collectionType)

        if builder is None:
            models = []
        else:
            collection = builder.dataCollection
            models = collection.getModels()
        
        self.selectList = self.buildSelectList(models)
        self.currentOption = tkinter.StringVar()

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
        
        self.dropDown = tkinter.OptionMenu(self, self.currentOption, *options)
        self.dropDown.grid(row = 0, column = 0, sticky = "ew")

        self.refreshButton = tkinter.Button(self, text = u"\u27F3", command = self.rebuild, borderwidth = 0)
        self.refreshButton.grid(row = 0, column = 1, padx = 10)

    def buildSelectList(self, models):
        selectList = []

        for model in models:
            option = str(model.getIndex()) + ":" + str(model.fileName)

            selectList.append(option)

        return selectList

    def get(self):
        option = self.currentOption.get()

        if option is None or option == self.NONE_STR or option == self.NO_DEFAULT_STR:
            return ""
        
        optionSplit = option.split(":")
        modelIndex = optionSplit[0]
        return modelIndex

    def getRaw(self, value):
        rawString = "<"
        rawString += "sequence_select|"
        rawString += self.collectionType + "|"
        rawString += self.currentOption.get()
        rawString += ">"
        return rawString