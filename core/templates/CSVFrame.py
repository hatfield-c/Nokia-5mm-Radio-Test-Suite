import tkinter
from Config import _CONFIG_
from CSVEditor import CSVEditor
from UIFactory import UIFactory
from templates.Divider import Divider

class CSVFrame(tkinter.Frame):
    def __init__(self, root, model, controls, builder):
        super().__init__(root)
        self.root = root
        self.model = model
        self.controls = controls
        self.builder = builder

        self.configure(borderwidth = 2, relief = "groove")

        details = tkinter.Frame(self)
        headLine = tkinter.Frame(details)

        csvFrame = CSVEditor(
            root = self, 
            model = model,
            dimensions = { 
                "width": self.builder.paramWidth, 
                "height": int(self.builder.dimensions["height"] / 3)
            }, 
            controls = self.controls
        )

        titleLabel = tkinter.Label(
            headLine, 
            text = UIFactory.TruncatePath(path = self.model.getPath(), length = 36),
            font = "Helevetica 14"
        )
        reloadButton = tkinter.Button(
            headLine,
            text = "Reload",
            background = _CONFIG_["color_secondary"],
            command = lambda csvEditor = csvFrame, model = self.model : self.builder.reloadFrame(csvEditor = csvEditor, model = model)
        )
        editButton = tkinter.Button(
            headLine,
            text = "Edit Defaults",
            background = _CONFIG_["color_secondary"],
            command = lambda model = self.model : self.builder.editDefaultValues(model = model)
        )
        removeButton = tkinter.Button(
            headLine, 
            text = "Remove",
            background = _CONFIG_["color_secondary"],
            command = lambda container = self, model = self.model : self.builder.removeFrame(container = container, model = model)
        )
        titleLabel.grid(row = 0, column = 0)
        reloadButton.grid(row = 0, column = 1, padx = 10)
        editButton.grid(row = 0, column = 2)
        removeButton.grid(row = 0, column = 3, padx = 10)

        delimiter = Divider(details, width = self.builder.paramWidth)

        headLine.grid(row = 0, column = 0, padx = 5, sticky = "w")
        delimiter.grid(row = 1, column = 0, padx = 5, pady = 1)

        csvFrame.columnconfigure(0, weight = 1)
        self.builder.paramFrames.append(csvFrame)

        details.grid(row = 0, column = 0, pady = 2, sticky = "w")
        csvFrame.grid(row = 1, column = 0)