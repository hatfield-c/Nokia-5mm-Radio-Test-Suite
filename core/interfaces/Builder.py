import tkinter
from tkinter import simpledialog
from core.UIFactory import UIFactory
from core.Interface import Interface
from core.interfaces.EditModel import EditModel
from core.models.Collection import Collection
from core.models.Parameters import Parameters
from core.models.ModelFactory import ModelFactory
from core.CSVEditor import CSVEditor
from core.templates.CSVFrame import CSVFrame
from core.templates.Divider import Divider
from Config import _CONFIG_

class Builder(Interface):

    DEFAULT_DIMENSIONS = {
        "width": 900,
        "height": 570
    }

    def __init__(
            self, 
            title = "[ NO TITLE GIVEN ]", 
            root = None, 
            csvPath = None,
            builderData = {
                "type": "[ NO TYPE SPECIFIED ]",
                "factory": ModelFactory(modelType = "model"),
                "controls": []
            }, 
            dimensions = DEFAULT_DIMENSIONS
        ):
        super().__init__(title = title, root = root, dimensions = dimensions)
        self.dataCollection = None
        self.modelFrames = []
        self.output = None
        self.builderData = builderData

        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_propagate(False)

        self.headerFrame = tkinter.Frame(self)
        self.scrollFrame = tkinter.Frame(self)
        self.scrollbar = tkinter.Frame(self)
        self.container = tkinter.Frame(self)

        self.rebuild(csvPath)

    def rebuild(self, csvPath):
        if csvPath is None:
            return
        
        self.csvPath = csvPath
        self.dataCollection = Collection(path = self.csvPath, factory = self.builderData["factory"])
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
        modelSet = self.dataCollection.getModels()
        self.modelFrames = []
        
        UIFactory.ScrollBinding(container = self, scrollableCanvas = self.scrollFrame, child = self.collectionFrame)

        i = 0
        for model in modelSet:

            editParametersFrame = self.buildModelFrame(model)
            editParametersFrame.grid(row = i, column = 0, pady = 5, padx = (5, 0))
            i += 1
        
        operationsFrame = tkinter.Frame(self.collectionFrame)

        newModelButton = tkinter.Button(
            operationsFrame, 
            text = "New " + self.builderData["type"], 
            command = lambda : self.addnewModel(), 
            font = "Helvetica 14 bold", 
            background = _CONFIG_["color_secondary"]
        )
        loadModelButton = tkinter.Button(
            operationsFrame, 
            text = "Load " + self.builderData["type"], 
            command = lambda : self.loadModel(), 
            font = "Helvetica 14 bold", 
            background = _CONFIG_["color_secondary"]
        )

        newModelButton.grid(row = 0, column = 0, padx = (0, 10))
        loadModelButton.grid(row = 0, column = 1)

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
        
    def addnewModel(self):
        fileName = tkinter.filedialog.asksaveasfilename(initialdir = _CONFIG_["csv_dir"], title = "Save New " + self.builderData["type"], filetypes = [("csv files", "*.csv")])
        
        if fileName is None or fileName == "":
            return
        
        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        factory = self.builderData["factory"]        
        model = factory.create(path = fileName)
        model.save()

        self.dataCollection.add(model)

        newModelFrame = self.buildModelFrame(model = model)
        newModelFrame.grid(row = len(self.modelFrames) - 1, column = 0, pady = 5, padx = (5, 0))
        
        self.update_idletasks()

    def loadModel(self):
        fileName = tkinter.filedialog.askopenfilename(initialdir = _CONFIG_["csv_dir"], title = "Load " + self.builderData["type"], filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        factory = self.builderData["factory"]

        model = factory.create(path = fileName)
        model.load()

        self.dataCollection.add(model)

        newModelFrame = self.buildModelFrame(model = model)
        newModelFrame.grid(row = len(self.modelFrames) - 1, column = 0, pady = 5, padx = (5, 0))

    def saveCollectionAs(self):
        fileName = tkinter.filedialog.asksaveasfilename(initialdir = _CONFIG_["csv_dir"], title = "Save Collection As", filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        self.dataCollection.setPath(fileName)
        self.dataCollection.save()

        self.rebuild(fileName)

    def loadCollection(self):
        fileName = tkinter.filedialog.askopenfilename(initialdir = _CONFIG_["csv_dir"], title = "Load " + self.builderData["type"] + " Collection", filetypes = [("csv files", "*.csv")])
        
        if fileName is None or fileName == "":
            return
        
        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        self.rebuild(fileName)

    def newCollection(self):
        fileName = tkinter.filedialog.asksaveasfilename(initialdir = _CONFIG_["csv_dir"], title = "Save New Collecion", filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        collection = Collection(path = fileName, factory = self.builderData["factory"])
        collection.save()

        self.rebuild(fileName)

    def compileData(self):
        data = {}

        for modelFrame in self.modelFrames:
            model = modelFrame.getModel()
            frameData = modelFrame.compileData()

            formattedData = model.build(frameData)
            data[model.getIndex()] = formattedData
        
        return data

    def buildModelFrame(self, model):
        return CSVFrame(root = self.collectionFrame, model = model, controls = self.builderData["controls"], builder = self)

    def editDefaultValues(self, model):
        editCsv = EditModel(model = model)
        editCsv.pack()

    def reloadFrame(self, csvEditor, model):
        model.load()
        csvEditor.rebuild(model)

    def removeFrame(self, container, model):
        self.dataCollection.remove(model)
        container.destroy()


