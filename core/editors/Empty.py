from Editor import Editor
import tkinter

class Empty(Editor):
    def __init__(self, root = None):
        super().__init__(title = "", root = root)
        
        self.container = tkinter.Frame(self, width = self.dimensions["width"], height = self.dimensions["height"])

        # Make your changes here, 
        ##########################################
        self.deleteThis = tkinter.Label(self.container, text = "WELCOME YO")

        self.deleteThis.pack()
        ##########################################

        self.container.grid(row = 0, column = 0, pady = 20, padx = 20)

