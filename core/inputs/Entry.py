import tkinter

class Entry(tkinter.Entry):
    # Defines the numerical index of the passed arguments data, and what they store
    # args["data"] = [
    #   NO POSITIONAL DATA
    # ]

    def __init__(self, args):
        root = args["root"]
        configData = args["config"]
        data = args["data"]
        orig = args["orig"]

        config = { }
        super().__init__(root, config)
        self.insert(0, orig)

    def getRaw(self, value):
        return value