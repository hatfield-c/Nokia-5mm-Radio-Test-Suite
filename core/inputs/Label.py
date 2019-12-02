import tkinter

class Label(tkinter.Label):

    # Defines the numerical index of the passed arguments data, and what they store
    POSITIONAL_DATA = [
        "text"     #     0
    ]

    def __init__(self, args):
        root = args["root"]
        config = args["config"]
        data = args["data"]

        super().__init__(root, config, text = "[" + data[0] + "]", font = "Helevetica 10 bold")