import tkinter
from core.inputs.InputFactory import InputFactory
from core.inputs.CollectionDropDown import CollectionDropDown
from core.Model import Model
from core.models.ModelFactory import ModelFactory
from core.templates.Divider import Divider
from Config import _CONFIG_
from core.UIFactory import UIFactory
from core.interfaces.alerts.NoBenchRunError import NoBenchRunError

class CSVRenderer(tkinter.Frame):

    def __init__(
        self, 
        root, 
        model, 
        dimensions, 
        controls = None, 
        subInterface = True,
        mutable = False
    ):
        super().__init__(root, width = dimensions["width"], height = dimensions["height"])

        self.root = root
        self.subInterface = subInterface
        self.mutable = mutable
        self.model = model
        self.dimensions = dimensions
        self.controls = controls
        self.inputFactory = InputFactory()
        self.modelFactory = ModelFactory(
            args = {
                "type": self.model.ID, 
                "fields": model.getFields()
            }
        )

        self.buttons = []
        self.entries = []
        self.fieldLabels = []

        self.scrollCanvas = tkinter.Frame(self)
        self.scrollFrame = tkinter.Frame(self)
        self.scrollBar = tkinter.Frame(self)

        self.grid_propagate(False)
        self.rebuild(self.model)

    def rebuild(self, model):
        if(model is None):
            return
        
        self.model = model

        if not self.subInterface:
            self.root.rebuild(model = model)

        self.buttons = []
        self.entries = []
        self.fieldLabels = []

        self.scrollCanvas.destroy()
        self.scrollFrame.destroy()
        self.scrollBar.destroy()

        entriesWidth = int(3 * self.dimensions["width"] / 4)
        controlsWidth = int(self.dimensions["width"] / 4)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        self.scrollCanvas = tkinter.Canvas(self, width = self.dimensions["width"] - 20, height = self.dimensions["height"])
        self.scrollFrame = tkinter.Frame(self.scrollCanvas)
        self.scrollFrame.columnconfigure(0, weight = 1)
        self.alignmentFrame = tkinter.Frame(self.scrollFrame, width = self.dimensions["width"] - 20)
        self.alignmentFrame.grid(row = 0, column = 0, columnspan = 2)
        
        self.leftColumn = tkinter.Frame(self.scrollFrame, width = entriesWidth)
        self.rightColumn = tkinter.Frame(self.scrollFrame, width = controlsWidth, borderwidth = 1, relief = "raised")

        self.scrollBar = tkinter.Scrollbar(self, orient = "vertical", command = self.scrollCanvas.yview)
        self.scrollCanvas.configure(yscrollcommand = self.scrollBar.set)

        UIFactory.ScrollBinding(container = self, scrollableCanvas = self.scrollCanvas, child = self.scrollFrame, subInterface = self.subInterface)

        self.buildEntries(root = self.leftColumn)
        self.buildControls(root = self.rightColumn)

        self.leftColumn.grid(row = 1, column = 0, pady = 5, padx = 5, sticky = "new")
        self.rightColumn.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = "n")

        self.scrollCanvas.grid(row = 0, column = 0, sticky = "nw")
        self.scrollBar.grid(row = 0, column = 1, sticky = "nse")
        
        self.scrollCanvas.create_window((0, 0), window = self.scrollFrame, anchor = "w")

    def buildEntries(self, root):
        root.columnconfigure(0, weight = 1)
        entryWidth = int(3 * self.dimensions["width"] / 4)

        self.entryFields = tkinter.Frame(root)
        self.entryFields.columnconfigure(0, weight = 1)

        fNum = 0
        rowFrame = tkinter.Frame(self.entryFields, width = entryWidth, background = _CONFIG_["color_secondary"])
        for field in self.model.getFields():
            label = tkinter.Label(rowFrame, text = field, background = _CONFIG_["color_secondary"])
            label.grid(row = 0, column = fNum, sticky = "ew")

            self.fieldLabels.append(label)
            rowFrame.columnconfigure(fNum, weight = 1)
            fNum += 1
        
        rowFrame.grid(row = 0, column = 0, sticky = "ew")

        j = 1
        for row in self.model.getData():
            rowFrame = self.buildModelFrame(root = self.entryFields, rowData = row, parentWidth = entryWidth)
            rowFrame.grid(row = j, column = 0, pady = 2, sticky = "ew")
            j += 1

        self.entryFields.grid(row = 0, column = 0, sticky = "ew")

    def buildControls(self, root):
        if self.controls is None:
            return

        i = 0
        for control in self.controls:
            if control in CSVRenderer._CONTROLS_: 
                title = CSVRenderer._CONTROLS_[control]["title"]
                action = CSVRenderer._CONTROLS_[control]["action"]

                args = {
                    "root": root,
                    "entry_container": self.entryFields,
                    "row": i
                }

                if title is None:
                    action(self = self, args = args)

                    i += 1
                    continue

                button = tkinter.Button(
                    root, 
                    text = title, 
                    command = lambda self = self, action = action : action(self = self, args = args)
                )
                self.buttons.append(button)
                button.grid(row = i, column = 0, pady = 4, padx = 8)

                i += 1

    def buildModelFrame(self, root, rowData, parentWidth):
        columnWidth = int(parentWidth / 3)
        modelFrame = tkinter.Frame(root, width = parentWidth)

        inputRow = {}
        k = 0
        for inputKey in rowData:
            inputString = rowData[inputKey]
            modelFrame.columnconfigure(k, weight = 1)

            inputWidget = self.inputFactory.create(
                root = modelFrame, 
                rawString = inputString, 
                args = { 
                    "dimensions": self.dimensions, 
                    "rowWidth": parentWidth,
                    "charWidth": self.getFieldWidth(),
                    "columnWidth": columnWidth
                }
            )
            inputWidget.grid(row = 0, column = k, padx = 3, sticky = "ew")
            inputRow[inputKey] = inputWidget

            k += 1

        i = 0
        for inputKey in rowData:
            alignmentFrame = tkinter.Frame(modelFrame, width = columnWidth)
            alignmentFrame.grid(row = 1, column = i, padx = 3)

            i += 1

        self.entries.append(inputRow)

        if self.mutable:
            remove = tkinter.Button(
                modelFrame, 
                text = u"\u274C",
                command = lambda row = inputRow, container = modelFrame : self.removePoint(row = row, container = container),
                borderwidth = 0
            )
            remove.grid(row = 0, column = k)

        return modelFrame

    def compileData(self):
        data = []

        for row in self.entries:
            dataRow = {}
            for entryKey in row:
                dataRow[entryKey] = row[entryKey].get()

            data.append(dataRow)

        return data

    def compileRawData(self):
        data = []

        for row in self.entries:
            dataRow = {}
            for entryKey in row:
                currentVal = row[entryKey].get()
                dataRow[entryKey] = row[entryKey].getRaw(currentVal)

            data.append(dataRow)

        return data

    def getFieldWidth(self):
        if(len(self.model.getFields()) > 0):
            return int((3 * self.dimensions["width"]) / (len(self.model.getFields()) * 23))
        else:
            return self.dimensions["width"]

    def getFields(self):
        return self.model.getFields()

    def getModel(self):
        return self.model

    ################################################
    #                                              #
    #                Button Handlers               #
    #                                              #
    ################################################

    _CONTROLS_ = {
        "save": {
            "title": "Save",
            "action": lambda self, args : self.save()
        },
        "saveAs": { 
            "title": "Save As",
            "action": lambda self, args : self.saveAs()
        },
        "newSequencePair": {
            "title": "New Pair",
            "action": lambda self, args : self.newSequencePair(args = args),
        },
        "divider": {
            "title": None,
            "action": lambda self, args : self.addDivider(args = args)
        }
    }

    def save(self):
        entryData = self.compileRawData()

        self.model.setData(data = entryData)
        self.model.save()
        
        self.rebuild(self.model)

    def saveAs(self):
        fileName = tkinter.filedialog.asksaveasfilename(initialdir = _CONFIG_["csv_dir"], title = "Save As TEST", filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        entryData = self.compileRawData()
        newModel = self.modelFactory.create(path = fileName)
        
        newModel.setData(data = entryData)
        newModel.save()

        self.rebuild(newModel)

    def newSequencePair(self, args):
        if "bench" not in self.model.getFields() or "run" not in self.model.getFields():
            alert = NoBenchRunError(path = self.model.getPath())
            return

        entryContainer = args["entry_container"]

        row = self.generateEmptyRow()
        row["bench"] = CollectionDropDown.DEFAULT_BENCH_STR
        row["run"] = CollectionDropDown.DEFAULT_RUN_STR 

        modelFrame = self.buildModelFrame(root = entryContainer, rowData = row, parentWidth = self.getFieldWidth())

        gridRow = len(self.entries)
        modelFrame.grid(row = gridRow, column = 0, pady = 2, sticky = "ew")

    def generateEmptyRow(self):
        emptyRow = {}

        for field in self.model.getFields():
            emptyRow[field] = ""

        return emptyRow

    def addDivider(self, args):
        divider = Divider(args["root"], color = "lightgray")
        divider.grid(row = args["row"], column = 0, pady = 8, padx = 8, sticky = "ew")

    def removePoint(self, row, container):
        if row not in self.entries:
            return

        self.entries.remove(row)
        container.destroy()
