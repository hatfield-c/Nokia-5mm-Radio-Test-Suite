import tkinter

class Radio(tkinter.Frame):
    # Defines the numerical index of the passed arguments data, and what they store
    POSITIONAL_DATA = [
        # NO POSITIONAL DATA
    ]

    def __init__(self, args):
        root = args["root"]
        config = args["config"]
        data = args["data"]
        default = args["default"]

        super().__init__(root, config)

        self.selection = tkinter.IntVar()
        self.radios = []
        i = 1
        for option in data:
            radio = tkinter.Radiobutton(
                self,
                text = option,
                indicatoron = 0,
                padx = 0,
                variable = self.selection,
                value = i
            )
            radio.grid(row = 0, column = i - 1)

            self.radios.append(radio)

            i += 1
