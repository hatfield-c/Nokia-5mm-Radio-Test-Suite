import tkinter

class Divider(tkinter.Frame):

    def __init__(self, root, girth = 1, width = None, color = "black"):
        super().__init__(root, width = width, height = girth, bg = color)