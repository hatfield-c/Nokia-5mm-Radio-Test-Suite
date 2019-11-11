from Interface import Interface
from CSVEditor import CSVEditor
from models.Parameters import Parameters
import tkinter

class EditParameters(Interface):

    def __init__(self, title = "Edit Data", dimensions = { "width": 700, "height": 500}, model = None):
        super().__init__(title = title, dimensions = dimensions)

        if model is None:
            return

        self.csvFrame = CSVEditor(root = self, dimensions = dimensions, paramModel = model)
        self.csvFrame.grid(row = 0, column = 0)