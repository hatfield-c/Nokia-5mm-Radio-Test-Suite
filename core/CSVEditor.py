import tkinter
from Config import _CONFIG_
from core.Model import Model
from core.models.ModelFactory import ModelFactory

from core.UIFactory import UIFactory
from core.templates.Divider import Divider
from core.interfaces.alerts.NoKeyError import NoKeyError
from core.interfaces.alerts.NoKeyValueError import NoKeyValueError
from core.interfaces.alerts.NoBenchUnitError import NoBenchUnitError

from core.inputs.Label import Label as InputLabel
from core.inputs.FSWFile import FSWFile
from core.inputs.CollectionDropDown import CollectionDropDown as SequenceSelector
from core.inputs.Radio import Radio

class CSVEditor(tkinter.Frame):

    def __init__(
            self, 
            root, 
            model, 
            dimensions, 
            defaultDir = _CONFIG_["csv_dir"],
            controls = None, 
            subInterface = True
        ):
        super().__init__(root, width = dimensions["width"], height = dimensions["height"])

        self.root = root
        self.subInterface = subInterface
        self.model = model
        self.dimensions = dimensions
        self.defaultDir = defaultDir
        self.controls = controls
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
        self.entryFields = tkinter.Frame(self)

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
        self.entryFields.destroy()

        entriesWidth = int(3 * self.dimensions["width"] / 4)
        controlsWidth = int(self.dimensions["width"] / 4)

        self.scrollCanvas = tkinter.Canvas(self, width = self.dimensions["width"] - 20, height = self.dimensions["height"] - 50)
        self.scrollFrame = tkinter.Frame(self.scrollCanvas)
        
        self.leftColumn = tkinter.Frame(self.scrollFrame)
        self.rightColumn = tkinter.Frame(self.scrollFrame, width = controlsWidth, borderwidth = 1, relief = "raised")

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

        self.entryFields = tkinter.Frame(root)

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
            rowFrame = self.buildModelFrame(root = self.entryFields, rowData = row, entryWidth = entryWidth)
            rowFrame.grid(row = j, column = 0, pady = 2)
            j += 1

        self.entryFields.grid(row = 0, column = 0)

    def buildControls(self, root):
        if self.controls is None:
            return
        
        i = 0
        for control in self.controls:
            if control in CSVEditor._CONTROLS_: 
                title = CSVEditor._CONTROLS_[control]["title"]
                action = CSVEditor._CONTROLS_[control]["action"]

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

    def buildModelFrame(self, root, rowData, entryWidth):
        modelFrame = tkinter.Frame(root, width = entryWidth)

        entryRow = {}
        k = 0
        for entryKey in rowData:
            entry = rowData[entryKey]
            modelFrame.columnconfigure(k, weight = 1)

            entryFrame = tkinter.Entry(modelFrame, width = self.getFieldWidth())
            entryFrame.insert(0, entry)

            entryFrame.grid(row = 0, column = k, padx = 3, sticky = "we")

            entryRow[entryKey] = entryFrame
            k += 1

        self.entries.append(entryRow)

        remove = tkinter.Button(
            modelFrame, 
            text = u"\u274C",
            command = lambda row = entryRow, container = modelFrame : self.removePoint(row = row, container = container),
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
        "load": {
            "title": "Load",
            "action": lambda self, args : self.load()
        },
        "newEmpty": {
            "title": "Empty Point",
            "action": lambda self, args : self.newEmpty(args = args),
        },
        "newFile": {
            "title": "New File",
            "action": lambda self, args : self.newFile()
        },
        "divider": {
            "title": None,
            "action": lambda self, args : self.addDivider(args = args)
        },
        "addKey": {
            "title": "Add Key",
            "action": lambda self, args : self.addKey(args = args)
        },
        "addAllocationFile": {
            "title": "Allocation\nFile",
            "action": lambda self, args : self.addAllocationFile(args = args)
        },
        "addCorrectionFile": {
            "title": "Correction\nFile",
            "action": lambda self, args : self.addCorrectionFile(args = args)
        },
        "addSequenceSelector": {
            "title": "Sequence\nSelector",
            "action": lambda self, args : self.addSequenceSelector(args = args)
        },
        "addRadio": {
            "title": "Add Radio",
            "action": lambda self, args : self.addRadio(args = args)
        },
        "addMobue": {
            "title": "MOBUE\nSetup",
            "action": lambda self, args : self.addMobue(args = args)
        },
        "addAbCategory": {
            "title": "A\\B\nCategories",
            "action": lambda self, args : self.addAbCategory(args = args)
        },
        "addCarrier": {
            "title": "Add\nCarrier",
            "action": lambda self, args : self.addCarrier(args = args)
        }
    }

    def save(self):
        entryData = self.compileData()

        self.model.setData(data = entryData)
        self.model.save()
        
        self.rebuild(self.model)

    def saveAs(self):
        fileName = tkinter.filedialog.asksaveasfilename(
            initialdir = self.defaultDir, 
            title = "Save As", 
            filetypes = [("csv files", "*.csv")]
        )

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        entryData = self.compileData()
        newModel = self.modelFactory.create(path = fileName)
        
        newModel.setData(data = entryData)
        newModel.save()

        self.rebuild(newModel)

    def load(self):
        fileName = tkinter.filedialog.askopenfilename(
            initialdir = self.defaultDir, 
            title = "Open", 
            filetypes = [("csv files", "*.csv")]
        )

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        model = self.modelFactory.create(path = fileName)
        model.load()
        self.rebuild(model = model)

    def newEmpty(self, args):
        entryContainer = args["entry_container"]

        row = self.generateEmptyRow()
        modelFrame = self.buildModelFrame(root = entryContainer, rowData = row, entryWidth = self.getFieldWidth())
        
        gridRow = len(self.entries)
        modelFrame.grid(row = gridRow, column = 0, pady = 2)

    def generateEmptyRow(self):
        emptyRow = {}

        for field in self.model.getFields():
            emptyRow[field] = ""

        return emptyRow

    def newFile(self):
        fileName = tkinter.filedialog.asksaveasfilename(
            initialdir = self.defaultDir, 
            title = "New", 
            filetypes = [("csv files", "*.csv")]
        )

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        newModel = self.modelFactory.create(path = fileName)
        newModel.save()

        self.rebuild(newModel)

    def addKey(self, args):
        if "key" not in self.model.getFields():
            alert = NoKeyError(path = self.model.getPath())
            alert.pack()
            return
        
        entryContainer = args["entry_container"]

        row = self.generateEmptyRow()
        row["key"] = InputLabel.DEFAULT

        modelFrame = self.buildModelFrame(root = entryContainer, rowData = row, entryWidth = self.getFieldWidth())
        
        gridRow = len(self.entries)
        modelFrame.grid(row = gridRow, column = 0, pady = 2)
    
    def addAllocationFile(self, args):
        if "key" not in self.model.getFields() or "value" not in self.model.getFields():
            alert = NoKeyValueError(path = self.model.getPath())
            alert.pack()
            return

        entryContainer = args["entry_container"]

        row = self.generateEmptyRow()
        row["key"] ="<label|Allocation File>"
        row["value"] = FSWFile.DEFAULT_BUILD + "ALLOCATION|>"

        modelFrame = self.buildModelFrame(root = entryContainer, rowData = row, entryWidth = self.getFieldWidth())

        gridRow = len(self.entries)
        modelFrame.grid(row = gridRow, column = 0, pady = 2, sticky = "ew")

    def addCorrectionFile(self, args):
        if "key" not in self.model.getFields() or "value" not in self.model.getFields():
            alert = NoKeyValueError(path = self.model.getPath())
            alert.pack()
            return

        entryContainer = args["entry_container"]

        row = self.generateEmptyRow()
        row["key"] ="<label|Correction File>"
        row["value"] = FSWFile.DEFAULT_BUILD + "s2p|>"

        modelFrame = self.buildModelFrame(root = entryContainer, rowData = row, entryWidth = self.getFieldWidth())

        gridRow = len(self.entries)
        modelFrame.grid(row = gridRow, column = 0, pady = 2, sticky = "ew")

    def addSequenceSelector(self, args):
        if "bench" not in self.model.getFields() or "unit" not in self.model.getFields():
            alert = NoBenchUnitError(path = self.model.getPath())
            alert.pack()
            return

        entryContainer = args["entry_container"]

        row = self.generateEmptyRow()
        row["bench"] = SequenceSelector.DEFAULT_BENCH_STR
        row["unit"] = SequenceSelector.DEFAULT_UNIT_STR

        modelFrame = self.buildModelFrame(root = entryContainer, rowData = row, entryWidth = self.getFieldWidth())

        gridRow = len(self.entries)
        modelFrame.grid(row = gridRow, column = 0, pady = 2, sticky = "ew")

    def addRadio(self, args):
        entryContainer = args["entry_container"]

        row = self.generateEmptyRow()
        keyList = list(row.keys())
        lastKey = keyList[-1]
        row[lastKey] = Radio.DEFAULT

        modelFrame = self.buildModelFrame(root = entryContainer, rowData = row, entryWidth = self.getFieldWidth())

        gridRow = len(self.entries)
        modelFrame.grid(row = gridRow, column = 0, pady = 2, sticky = "ew")

    def addMobue(self, args):
        if "key" not in self.model.getFields() or "value" not in self.model.getFields():
            alert = NoKeyValueError(path = self.model.getPath())
            alert.pack()
            return
        
        entryContainer = args["entry_container"]

        row = self.generateEmptyRow()
        row["key"] = "<label|Resolution Bandwidth(MHz)>"
        modelFrame = self.buildModelFrame(root = entryContainer, rowData = row, entryWidth = self.getFieldWidth())
        gridRow = len(self.entries)
        modelFrame.grid(row = gridRow, column = 0, pady = 2, sticky = "ew")

        row = self.generateEmptyRow()
        row["key"] = "<label|Sweep Time(s)>"
        modelFrame = self.buildModelFrame(root = entryContainer, rowData = row, entryWidth = self.getFieldWidth())
        gridRow = len(self.entries)
        modelFrame.grid(row = gridRow, column = 0, pady = 2, sticky = "ew")

        self.addAbCategory(args)
        self.addCarrier(args)

    def addAbCategory(self, args):
        if "key" not in self.model.getFields() or "value" not in self.model.getFields():
            alert = NoKeyValueError(path = self.model.getPath())
            alert.pack()
            return
        
        entryContainer = args["entry_container"]

        row = self.generateEmptyRow()
        row["key"] = "<label|Category>"
        row["value"] = "<radio|A|B>"
        modelFrame = self.buildModelFrame(root = entryContainer, rowData = row, entryWidth = self.getFieldWidth())
        gridRow = len(self.entries)
        modelFrame.grid(row = gridRow, column = 0, pady = 2, sticky = "ew")

    def addCarrier(self, args):
        if "key" not in self.model.getFields() or "value" not in self.model.getFields():
            alert = NoKeyValueError(path = self.model.getPath())
            alert.pack()
            return
        
        carrierNum = 0
        data = self.compileData()
        for row in data:
            keyVal = row["key"]

            if "Carrier" in keyVal:
                carrierNum += 1

        entryContainer = args["entry_container"]

        row = self.generateEmptyRow()
        row["key"] = "<label|Carrier" + str(carrierNum) + ">"
        row["value"] = "<label|Carrier" + str(carrierNum) + ">"
        modelFrame = self.buildModelFrame(root = entryContainer, rowData = row, entryWidth = self.getFieldWidth())
        gridRow = len(self.entries)
        modelFrame.grid(row = gridRow, column = 0, pady = 2, sticky = "ew")

        row = self.generateEmptyRow()
        row["key"] = "<label|Center Frequency(GHz)" + str(carrierNum) + ">"
        modelFrame = self.buildModelFrame(root = entryContainer, rowData = row, entryWidth = self.getFieldWidth())
        gridRow = len(self.entries)
        modelFrame.grid(row = gridRow, column = 0, pady = 2, sticky = "ew")

        row = self.generateEmptyRow()
        row["key"] = "<label|Channel Bandwidth(MHz)" + str(carrierNum) + ">"
        modelFrame = self.buildModelFrame(root = entryContainer, rowData = row, entryWidth = self.getFieldWidth())
        gridRow = len(self.entries)
        modelFrame.grid(row = gridRow, column = 0, pady = 2, sticky = "ew")

    def addDivider(self, args):
        divider = Divider(args["root"], color = "lightgray")
        divider.grid(row = args["row"], column = 0, pady = 8, padx = 8, sticky = "ew")

    def removePoint(self, row, container):
        if row not in self.entries:
            return

        self.entries.remove(row)
        container.destroy()

