import tkinter

class Label(tkinter.Label):

    # Defines the numerical index of the passed arguments data, and what they store
    POSITIONAL_DATA = [
        "text"     #     0
    ]

    DEFAULT = "<label|DEFAULT_TEXT>"

    def __init__(self, args):
        root = args["root"]
        configData = args["config"]
        data = args["data"]
        orig = args["orig"]

        config = { }
        self.text = data[0]
        super().__init__(root, config, text = "[" + data[0] + "]", font = "Helevetica 10 bold")

    def get(self):
        return self.text

    def getRaw(self, value):
        rawString = "<"
        rawString += "label|"
        rawString += value
        rawString += ">"
        return rawString