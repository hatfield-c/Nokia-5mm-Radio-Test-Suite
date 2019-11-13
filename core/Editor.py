import tkinter
from tkinter import simpledialog
from UIFactory import UIFactory
from Interface import Interface
from interfaces.EditParameters import EditParameters
from models.Collection import Collection
from models.Parameters import Parameters
from CSVEditor import CSVEditor
from templates.Divider import Divider
from Config import _CONFIG_

class Editor(Interface):
    def __init__(self, title = "", root = None, csvPath = None, dimensions = { "width": 900, "height": 570}, editorData = None, color = None):
        super().__init__(title = title, root = root, dimensions = dimensions)
        self.dataCollection = None
        self.paramFrames = []
        self.output = None
        self.editorData = editorData

        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_propagate(False)

        self.headerFrame = tkinter.Frame(self)
        self.scrollFrame = tkinter.Frame(self)
        self.scrollbar = tkinter.Frame(self)
        self.container = tkinter.Frame(self)

        self.config(background = color)

        self.rebuild(csvPath)

    def rebuild(self, csvPath):
        if csvPath is None:
            return
        
        self.csvPath = csvPath
        self.dataCollection = Collection(path = self.csvPath)
        self.dataCollection.load()

        self.headerFrame.destroy()
        self.scrollFrame.destroy()
        self.scrollbar.destroy()
        self.container.destroy()

        self.paramWidth = self.dimensions["width"] - 50
        self.headerFrame = self.buildHeaderFrame()

        self.scrollFrame = tkinter.Canvas(self, width = self.paramWidth, height = self.dimensions["height"] - 40)
        self.scrollFrame.grid_propagate(False)
        self.container = tkinter.Frame(self)
        
        self.scrollbar = tkinter.Scrollbar(self, orient = "vertical", command = self.scrollFrame.yview)
        self.scrollFrame.configure(yscrollcommand = self.scrollbar.set)

        self.collectionFrame = tkinter.Frame(self.container, background = "white")
        parameterSet = self.dataCollection.getModels()
        self.paramFrames = []
        
        UIFactory.ScrollBinding(container = self, scrollableCanvas = self.scrollFrame, child = self.collectionFrame)

        i = 0
        for setKey in parameterSet:
            parameters = parameterSet[setKey]

            editParametersFrame = self.buildParameterFrame(parameters, self.paramWidth)
            editParametersFrame.grid(row = i, column = 0, pady = 5, padx = (5, 0))
            i += 1
        
        operationsFrame = tkinter.Frame(self.collectionFrame)

        newParameter = tkinter.Button(
            operationsFrame, 
            text = "New " + self.editorData["type"], 
            command = lambda : self.addnewParameters(), 
            font = "Helvetica 14 bold", 
            background = _CONFIG_["color_secondary"]
        )
        loadParameter = tkinter.Button(
            operationsFrame, 
            text = "Load " + self.editorData["type"], 
            command = lambda : self.loadParameters(), 
            font = "Helvetica 14 bold", 
            background = _CONFIG_["color_secondary"]
        )

        newParameter.grid(row = 0, column = 0, padx = (0, 10))
        loadParameter.grid(row = 0, column = 1)

        operationsFrame.grid(row = i + 1, column = 0)

        self.collectionFrame.grid(row = 0, column = 0)

        self.headerFrame.grid(row = 0, column = 0, sticky = "ew", columnspan = 2)
        self.scrollFrame.grid(row = 1, column = 0, sticky = "news")
        self.scrollbar.grid(row = 1, column = 1, sticky = "ns")

        self.scrollFrame.create_window((0, 0), window = self.container, anchor = "nw")

        self.headerFrame.lift()

    def buildHeaderFrame(self):
        headerFrame = tkinter.Frame(self, background = _CONFIG_["color_primary"], borderwidth = 2, relief = "raised")
        collectionTitle = tkinter.Label(
            headerFrame, 
            text = "Collection: " + self.dataCollection.getName(), 
            background = _CONFIG_["color_primary"],
            font = "Helvetica 16 bold",
        )

        saveCollection = tkinter.Button(
            headerFrame, 
            text = u"\uD83D\uDCBE", 
            command = lambda : self.dataCollection.save(), 
            font = "Helvetica 14", 
            borderwidth = 0, 
            background = _CONFIG_["color_primary"]
        )
        saveAsCollection = tkinter.Button(
            headerFrame, 
            text = "SAVE AS", 
            command = lambda : self.saveCollectionAs(), 
            font = "Helvetica 10"
        )
        loadCollection = tkinter.Button(
            headerFrame, 
            text = "LOAD", 
            command = lambda : self.loadCollection(), 
            font = "Helvetica 10"
        )
        newCollection = tkinter.Button(
            headerFrame, 
            text = "NEW", 
            command = lambda : self.newCollection(), 
            font = "Helvetica 10"
        )

        collectionTitle.grid(row = 0, column = 0, padx = 3, pady = 2)
        saveCollection.grid(row = 0, column = 1, padx = 5, pady = (0,5), sticky = "n")
        saveAsCollection.grid(row = 0, column = 2)
        loadCollection.grid(row = 0, column = 3, padx = 5)
        newCollection.grid(row = 0, column = 4)

        return headerFrame
        
    def buildParameterFrame(self, parameters, width):
        editParametersFrame = tkinter.Frame(self.collectionFrame)
        editParametersFrame.configure(borderwidth = 2, relief = "groove")

        details = tkinter.Frame(editParametersFrame)
        headLine = tkinter.Frame(details)

        csvFrame = CSVEditor(
            root = editParametersFrame, 
            paramModel = parameters,
            dimensions = { 
                "width": width, 
                "height": int(self.dimensions["height"] / 3)
            }, 
            controls = self.editorData["controls"]
        )

        titleLabel = tkinter.Label(
            headLine, 
            text = UIFactory.TruncatePath(path = parameters.getParameter("name"), length = 13) + ":   " + UIFactory.TruncatePath(path = parameters.getPath(), length = 23),
            font = "Helevetica 14"
        )
        reloadButton = tkinter.Button(
            headLine,
            text = "Reload",
            background = _CONFIG_["color_secondary"],
            command = lambda csvEditor = csvFrame, parameters = parameters : self.reloadFrame(csvEditor = csvEditor, parameters = parameters)
        )
        editButton = tkinter.Button(
            headLine,
            text = "Edit Defaults",
            background = _CONFIG_["color_secondary"],
            command = lambda parameters = parameters : self.editDefaultValues(parameters = parameters)
        )
        removeButton = tkinter.Button(
            headLine, 
            text = "Remove",
            background = _CONFIG_["color_secondary"],
            command = lambda container = editParametersFrame, parameters = parameters : self.removeFrame(container = container, parameters = parameters)
        )
        titleLabel.grid(row = 0, column = 0)
        reloadButton.grid(row = 0, column = 1, padx = 10)
        editButton.grid(row = 0, column = 2)
        removeButton.grid(row = 0, column = 3, padx = 10)

        delimiter = Divider(details, width = width)

        headLine.grid(row = 0, column = 0, padx = 5, sticky = "w")
        delimiter.grid(row = 1, column = 0, padx = 5, pady = 1)

        csvFrame.columnconfigure(0, weight = 1)
        self.paramFrames.append(csvFrame)

        details.grid(row = 0, column = 0, pady = 2, sticky = "w")
        csvFrame.grid(row = 1, column = 0)

        return editParametersFrame

    def addnewParameters(self):
        fileName = tkinter.filedialog.asksaveasfilename(initialdir = _CONFIG_["csv_dir"], title = "Save New " + self.editorData["type"], filetypes = [("csv files", "*.csv")])
        
        if fileName is None or fileName == "":
            return
        
        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")
        parametersName = simpledialog.askstring(title = "Bench Name", prompt = "Please enter a name for the bench.")

        if parametersName is None or parametersName == "":
            return

        paramModel = Parameters(path = fileName)
        paramModel.setParameter(key = "name", value = parametersName)
        paramModel.save()

        newParamFrame = self.buildParameterFrame(parameters = paramModel, width = self.paramWidth)
        newParamFrame.grid(row = len(self.paramFrames) - 1, column = 0, pady = 5, padx = (5, 0))

        self.dataCollection.add(paramModel)
        self.update_idletasks()

    def loadParameters(self):
        fileName = tkinter.filedialog.askopenfilename(initialdir = _CONFIG_["csv_dir"], title = "Load " + self.editorData["type"], filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        paramModel = Parameters(path = fileName)
        paramModel.load()

        newParamFrame = self.buildParameterFrame(parameters = paramModel, width = self.paramWidth)
        newParamFrame.grid(row = len(self.paramFrames) - 1, column = 0, pady = 5, padx = (5, 0))

        self.dataCollection.add(paramModel)

    def saveCollectionAs(self):
        fileName = tkinter.filedialog.asksaveasfilename(initialdir = _CONFIG_["csv_dir"], title = "Save Collection As", filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        self.dataCollection.setPath(fileName)
        self.dataCollection.save()

        self.rebuild(fileName)

    def loadCollection(self):
        fileName = tkinter.filedialog.askopenfilename(initialdir = _CONFIG_["csv_dir"], title = "Load " + self.editorData["type"] + " Collection", filetypes = [("csv files", "*.csv")])
        
        if fileName is None or fileName == "":
            return
        
        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        self.rebuild(fileName)

    def newCollection(self):
        fileName = tkinter.filedialog.asksaveasfilename(initialdir = _CONFIG_["csv_dir"], title = "Save New Collecion", filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        collection = Collection(path = fileName)
        collection.save()

        self.rebuild(fileName)

    def editDefaultValues(self, parameters):
        editCsv = EditParameters(model = parameters)
        editCsv.pack()

    def reloadFrame(self, csvEditor, parameters):
        parameters.load()
        csvEditor.rebuild(parameters)

    def removeFrame(self, container, parameters):
        self.dataCollection.remove(parameters)
        container.destroy()

    def compileData(self):
        pass


