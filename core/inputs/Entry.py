import tkinter

class Entry(tkinter.Entry):
    # Defines the numerical index of the passed arguments data, and what they store
    POSITIONAL_DATA = [
        # NO POSITIONAL DATA
    ]

    def __init__(self, args):
        root = args["root"]
        config = args["config"]
        default = args["default"]

        super().__init__(root, config)
        self.insert(0, default)