import tkinter
from models.Parameters import Parameters
from templates.Divider import Divider
from Config import _CONFIG_
from UIFactory import UIFactory

class CSVEditor(tkinter.Frame):
    
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
        "newPoint": {
            "title": "New Point",
            "action": lambda self, args : self.newParameter(args = args),
        },
        "newFile": {
            "title": "New File",
            "action": lambda self, args : self.newFile()
        },
        "divider": {
            "title": None,
            "action": lambda self, args : self.addDivider(args = args)
        }
    }

    def __init__(self, root, paramModel, dimensions, controls = None, subInterface = True):
        super().__init__(root, width = dimensions["width"], height = dimensions["height"])

        self.root = root
        self.subInterface = subInterface
        self.paramModel = paramModel
        self.dimensions = dimensions
        self.controls = controls

        self.buttons = []
        self.entries = []
        self.fieldLabels = []

        self.scrollCanvas = tkinter.Frame(self)
        self.scrollFrame = tkinter.Frame(self)
        self.scrollBar = tkinter.Frame(self)

        self.grid_propagate(False)
        self.rebuild(self.paramModel)

    def rebuild(self, paramModel):
        if(paramModel is None):
            return

        self.paramModel = paramModel

        if not self.subInterface:
            self.root.rebuild(model = paramModel)

        self.buttons = []
        self.entries = []
        self.fieldLabels = []

        self.scrollCanvas.destroy()
        self.scrollFrame.destroy()
        self.scrollBar.destroy()

        entriesWidth = int(3 * self.dimensions["width"] / 4)
        controlsWidth = int(self.dimensions["width"] / 4)

        self.scrollCanvas = tkinter.Canvas(self, width = self.dimensions["width"] - 20, height = self.dimensions["height"])
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
        for field in self.paramModel.getFields():
            label = tkinter.Label(rowFrame, text = field, background = _CONFIG_["color_secondary"])
            label.grid(row = 0, column = fNum, sticky = "ew")

            self.fieldLabels.append(label)
            rowFrame.columnconfigure(fNum, weight = 1)
            fNum += 1
        
        rowFrame.grid(row = 0, column = 0, sticky = "ew")

        j = 1
        for row in self.paramModel.getData():
            rowFrame = self.buildParameterFrame(root = self.entryFields, rowData = row, entryWidth = entryWidth)
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

    def buildParameterFrame(self, root, rowData, entryWidth):
        paramFrame = tkinter.Frame(root, width = entryWidth)

        entryRow = {}
        k = 0
        for entryKey in rowData:
            entry = rowData[entryKey]
            paramFrame.columnconfigure(k, weight = 1)

            entryFrame = tkinter.Entry(paramFrame, width = self.getFieldWidth())
            entryFrame.insert(0, entry)

            entryFrame.grid(row = 0, column = k, padx = 3, sticky = "we")

            entryRow[entryKey] = entryFrame
            k += 1

        self.entries.append(entryRow)

        remove = tkinter.Button(
            paramFrame, 
            text = u"\u274C",
            command = lambda row = entryRow, container = paramFrame : self.removeParameter(row = row, container = container),
            borderwidth = 0
        )
        remove.grid(row = 0, column = k)

        return paramFrame

    def compileData(self):
        data = []

        for row in self.entries:
            dataRow = {}
            for entryKey in row:
                dataRow[entryKey] = row[entryKey].get()

            data.append(dataRow)

        return data

    def save(self):
        entryData = self.compileData()

        self.paramModel.buildParameters(rowData = entryData)
        self.paramModel.save()
        
        self.rebuild(self.paramModel)

    def saveAs(self):
        fileName = tkinter.filedialog.asksaveasfilename(initialdir = _CONFIG_["csv_dir"], title = "Save As", filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        entryData = self.compileData()
        newModel = Parameters(path = fileName)
        
        newModel.buildParameters(rowData = entryData)
        newModel.save()

    def load(self):
        fileName = tkinter.filedialog.askopenfilename(initialdir = _CONFIG_["csv_dir"], title = "Open", filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        paramModel = Parameters(path = fileName)
        paramModel.load()
        self.rebuild(paramModel = paramModel)

    def newParameter(self, args):
        entryContainer = args["entry_container"]

        row = self.generateEmptyRow()
        paramFrame = self.buildParameterFrame(root = entryContainer, rowData = row, entryWidth = self.getFieldWidth())
        
        gridRow = len(self.entries)
        paramFrame.grid(row = gridRow, column = 0, pady = 2)

    def generateEmptyRow(self):
        emptyRow = {}

        for field in self.paramModel.getFields():
            emptyRow[field] = ""

        return emptyRow

    def newFile(self):
        fileName = tkinter.filedialog.asksaveasfilename(initialdir = _CONFIG_["csv_dir"], title = "New", filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")
        newModel = Parameters(path = fileName)
        newModel.useDefaultFields()
        newModel.save()

        self.rebuild(newModel)

    def addDivider(self, args):
        divider = Divider(args["root"], color = "lightgray")
        divider.grid(row = args["row"], column = 0, pady = 8, padx = 8, sticky = "ew")

    def removeParameter(self, row, container):
        if row not in self.entries:
            return

        self.entries.remove(row)
        container.destroy()

    def getFieldWidth(self):
        if(len(self.paramModel.getFields()) > 0):
            return int((3 * self.dimensions["width"]) / (len(self.paramModel.getFields()) * 23))
        else:
            return self.dimensions["width"]

    def getFields(self):
        return self.paramModel.getFields()

    def getName(self):
        return self.paramModel.getParameter("name")

    def getTitle(self):
        return self.paramModel.getParameter("name")