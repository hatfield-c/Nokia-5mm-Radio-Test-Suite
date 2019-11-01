import tkinter
from Interface import Interface

class Editor(Interface):
    def __init__(self, title = "", root = None, dimensions = { "width": 900, "height": 570}, data = None, color = None):
        super().__init__(title = title, root = root, dimensions = dimensions)
        self.grid_propagate(False)
        self.config(background = color)
