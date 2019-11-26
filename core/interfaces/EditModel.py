from Interface import Interface
from CSVEditor import CSVEditor
from UIFactory import UIFactory
from models.Parameters import Parameters
from templates.Divider import Divider
import tkinter

class EditModel(Interface):

    def __init__(self, title = "Edit Data", dimensions = { "width": 770, "height": 500}, model = None):
        super().__init__(title = title, dimensions = dimensions)

        self.model = model
        self.dimensions = dimensions

        self.delimiter = tkinter.Frame(self)
        self.titleLabel = tkinter.Frame(self)
        self.csvFrame = tkinter.Frame(self)

        self.controls = [
            "newFile",
            "load",
            "saveAs",
            "divider",
            "save",
            "newPoint",
        ]

        self.delimiter = Divider(self)
        self.csvFrame = CSVEditor(
            root = self, 
            dimensions = self.dimensions, 
            model = self.model, 
            controls = self.controls,
            subInterface = False
        )

        self.delimiter.grid(row = 1, column = 0, padx = 5, pady = 1, sticky = "ew")
        self.csvFrame.grid(row = 2, column = 0)

        self.rebuild(model)

    def rebuild(self, model):
        self.model = model

        self.titleLabel.destroy()

        if self.model is None:
            textStr = "[No File Detected]"
        else:
            textStr = UIFactory.TruncatePath(
                path = self.model.getPath(), 
                length = 50
            )

        self.titleLabel = tkinter.Label(
            self, 
            text = textStr,
            font = "Helevetica 14"
        )
        self.titleLabel.grid(row = 0, column = 0, padx = 6, sticky = "w")
        