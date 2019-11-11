import tkinter
from templates.Divider import Divider
from Config import _CONFIG_
from UIFactory import UIFactory

class CSVEditor(tkinter.Frame):
    
    def __init__(self, root, paramModel, dimensions, controls = None):
        if(root is None):
            self.subInterface = False
        else:
            self.subInterface = True
        
        super().__init__(root, width = dimensions["width"], height = dimensions["height"])

        self.paramModel = paramModel
        self.dimensions = dimensions
        self.controls = controls
        self.buttons = []
        self.fieldLabels = []

        self.scrollCanvas = tkinter.Frame(self)
        self.scrollFrame = tkinter.Frame(self)
        self.scrollBar = tkinter.Frame(self)

        self.rebuild(self.paramModel)

    def rebuild(self, paramModel):
        if(paramModel is None):
            return

        self.paramModel = paramModel

        self.scrollCanvas.destroy()
        self.scrollFrame.destroy()
        self.scrollBar.destroy()

        if(len(paramModel.getFields()) > 0):
            self.fieldWidth = int((3 * self.dimensions["width"]) / (len(paramModel.getFields()) * 23))
        else:
            self.fieldWidth = self.dimensions["width"]

        self.grid_propagate(False)
        
        entriesWidth = int(3 * self.dimensions["width"] / 4)
        controlsWidth = int(self.dimensions["width"] / 4)

        self.scrollCanvas = tkinter.Canvas(self, width = self.dimensions["width"] - 20, height = self.dimensions["height"])
        self.scrollFrame = tkinter.Frame(self.scrollCanvas)
        
        self.leftColumn = tkinter.Frame(self.scrollFrame)
        self.rightColumn = tkinter.Frame(self.scrollFrame, width = controlsWidth)

        self.scrollBar = tkinter.Scrollbar(self, orient = "vertical", command = self.scrollCanvas.yview)
        self.scrollCanvas.configure(yscrollcommand = self.scrollBar.set)

        UIFactory.ScrollBinding(container = self, scrollableCanvas = self.scrollCanvas, child = self.scrollFrame, subInterface = self.subInterface)

        self.buildEntries(root = self.leftColumn)
        self.buildControls(root = self.rightColumn)

        self.leftColumn.grid(row = 0, column = 0, pady = 5, padx = 5, sticky = "n")
        self.rightColumn.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "n")
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.scrollCanvas.grid(row = 0, column = 0, sticky = "nw")
        self.scrollBar.grid(row = 0, column = 1, sticky = "nse")
        
        self.scrollCanvas.create_window((0, 0), window = self.scrollFrame, anchor = "w")

    def buildEntries(self, root):
        entryWidth = int(3 * self.dimensions["width"] / 4)

        entryFields = tkinter.Frame(root)

        fNum = 0
        rowFrame = tkinter.Frame(entryFields, width = entryWidth, background = _CONFIG_["color_secondary"])
        for field in self.paramModel.getFields():
            label = tkinter.Label(rowFrame, text = field, background = _CONFIG_["color_secondary"])
            label.grid(row = 0, column = fNum, sticky = "ew")

            self.fieldLabels.append(label)
            rowFrame.columnconfigure(fNum, weight = 1)
            fNum += 1
        
        rowFrame.grid(row = 0, column = 0, sticky = "ew")

        j = 1
        for row in self.paramModel.getData():
            rowFrame = tkinter.Frame(entryFields, width = entryWidth)

            k = 0
            for entryKey in row:
                entry = row[entryKey]
                rowFrame.columnconfigure(k, weight = 1)

                entryFrame = tkinter.Entry(rowFrame, width = self.fieldWidth)
                entryFrame.insert(0, entry)

                entryFrame.grid(row = 0, column = k, padx = 3, sticky = "we")
                k += 1

            remove = tkinter.Button(
                rowFrame, 
                text = u"\u274C", 
                borderwidth = 0
            )
            remove.grid(row = 0, column = k)
            rowFrame.grid(row = j, column = 0, pady = 2)
            j += 1

        entryFields.grid(row = 0, column = 0)

    def buildControls(self, root):
        if self.controls is None:
            return

        i = 0
        for buttonKey in self.controls:
            if(buttonKey == "_DIVIDER_"):
                divider = Divider(root, color = "grey")
                divider.grid(row = i, column = 0, pady = 8, sticky = "ew")
            else:
                action = self.controls[buttonKey]["action"]
                button = tkinter.Button(
                    root, 
                    text = self.controls[buttonKey]["title"], 
                    command = lambda model = self.paramModel, action = action : action(model =  model)
                )
                self.buttons.append(button)
                button.grid(row = i, column = 0, pady = 2)

            i += 1

    def getFields(self):
        return self.paramModel.getFields()

    def getName(self):
        return self.paramModel.getParameter("name")

    def getTitle(self):
        return self.paramModel.getParameter("name")