import traceback
import tkinter
from tkinter import simpledialog

from core.models.Collection import Collection
from core.models.Parameters import Parameters
from core.models.ModelFactory import ModelFactory

from core.Interface import Interface
from core.interfaces.EditModel import EditModel
from core.interfaces.alerts.PathError import PathError
from core.interfaces.alerts.builder.NoCollectionError import NoCollectionError

from core.templates.CSVFrame import CSVFrame
from core.templates.Divider import Divider

from core.CSVEditor import CSVEditor
from core.UIFactory import UIFactory
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
                "mutable": False,
                "factory": ModelFactory(
                    args = {
                        "type": "model",
                        "fields": [ "key", "value" ]
                    }
                ),
                "controls": {
                    "edit": [
                        "save",
                        "saveAs",
                        "newFile",
                        "divider",
                        "newEmpty"
                    ],
                    "render": []
                }
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
        self.collectionFrame = tkinter.Frame(self)

        self.rebuild(csvPath)

    def rebuild(self, csvPath):

        self.csvPath = csvPath
        self.dataCollection = Collection(path = self.csvPath, factory = self.builderData["factory"])

        try:
            self.dataCollection.load()
        except Exception:
            traceback.print_exc()
            PathError(path = csvPath, pathType = self.builderData["type"] + " " + self.dataCollection.ID)
            self.dataCollection = Collection(path = None, factory = self.builderData["factory"])

        self.headerFrame.destroy()
        self.scrollFrame.destroy()
        self.scrollbar.destroy()
        self.container.destroy()
        self.collectionFrame.destroy()

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
        
        if i == 0:
            placeHolder = tkinter.Frame(self.collectionFrame, width = self.paramWidth)
            placeHolder.grid(row = 0, column = 0, sticky = "we")

        self.operationsFrame = tkinter.Frame(self.container)

        newModelButton = tkinter.Button(
            self.operationsFrame, 
            text = "New " + self.builderData["type"], 
            command = lambda : self.addnewModel(), 
            font = "Helvetica 14 bold", 
            background = _CONFIG_["color_secondary"]
        )
        loadModelButton = tkinter.Button(
            self.operationsFrame, 
            text = "Load " + self.builderData["type"], 
            command = lambda : self.loadModel(), 
            font = "Helvetica 14 bold", 
            background = _CONFIG_["color_secondary"]
        )

        newModelButton.grid(row = 0, column = 0, padx = (0, 10))
        loadModelButton.grid(row = 0, column = 1)

        self.collectionFrame.grid(row = 0, column = 0)
        self.operationsFrame.grid(row = 1, column = 0)

        self.headerFrame.grid(row = 0, column = 0, sticky = "we", columnspan = 2)
        self.scrollFrame.grid(row = 1, column = 0, sticky = "news")
        self.scrollbar.grid(row = 1, column = 1, sticky = "ns")

        self.scrollFrame.create_window((0, 0), window = self.container, anchor = "nw")

        self.headerFrame.lift()

    def buildHeaderFrame(self):
        headerFrame = tkinter.Frame(self, background = _CONFIG_["color_primary"], borderwidth = 2, relief = "raised")
        collectionTitle = tkinter.Label(
            headerFrame, 
            text = self.builderData["type"].upper() + ": " + self.dataCollection.getName(), 
            background = _CONFIG_["color_primary"],
            font = "Helvetica 16 bold",
        )

        saveCollection = tkinter.Button(
            headerFrame, 
            text = u"\uD83D\uDCBE", 
            command = lambda : self.saveCollection(), 
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
    
    def compileData(self):
        data = {}

        for modelFrame in self.modelFrames:
            model = modelFrame.getModel()

            modelData = {
                "index": model.getIndex(),
                "path": model.getPath(),
                "fileName": model.fileName,
                "pureName": model.pureName,
                "fields": model.getFields(),
                "data": modelFrame.compileData()
            }

            data[model.getIndex()] = modelData
        
        return data

    def compileIndexedData(self):
        data = {}

        for modelFrame in self.modelFrames:
            model = modelFrame.getModel()

            modelData = {
                "index": model.getIndex(),
                "path": model.getPath(),
                "fileName": model.fileName,
                "pureName": model.pureName
            }

            csvData = modelFrame.compileData()
            formattedData = model.build(csvData)

            modelData["data"]: formattedData
            data[model.getIndex()] = modelData
        
        return data

    def buildModelFrame(self, model):
        return CSVFrame(
            root = self.collectionFrame, 
            model = model, 
            controls = self.builderData["controls"], 
            builder = self
        )

    def getPath(self):
        if self.dataCollection is None:
            return None

        return self.dataCollection.getPath()

    ################################################
    #                                              #
    #                Button Handlers               #
    #                                              #
    ################################################

    def addnewModel(self):
        if self.dataCollection.getPath() is None or self.dataCollection.getPath() == "":
            alert = NoCollectionError(builderType = self.builderData["type"])
            alert.pack()
            return

        fileName = tkinter.filedialog.asksaveasfilename(initialdir = _CONFIG_["csv_dir"], title = "Save New " + self.builderData["type"], filetypes = [("csv files", "*.csv")])
        
        if fileName is None or fileName == "":
            return
        
        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        factory = self.builderData["factory"]        
        model = factory.create(path = fileName)

        try:
            model.save()
        except Exception:
            traceback.print_exc()
            PathError(path = fileName, pathType = model.ID)
            return
        
        self.dataCollection.add(model)

        newModelFrame = self.buildModelFrame(model = model)
        newModelFrame.grid(row = len(self.modelFrames) - 1, column = 0, pady = 5, padx = (5, 0))

    def loadModel(self):
        if self.dataCollection.getPath() is None or self.dataCollection.getPath() == "":
            alert = NoCollectionError(builderType = self.builderData["type"])
            alert.pack()
            return

        fileName = tkinter.filedialog.askopenfilename(initialdir = _CONFIG_["csv_dir"], title = "Load " + self.builderData["type"], filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        factory = self.builderData["factory"]

        model = factory.create(path = fileName)

        try:
            model.load()
        except Exception:
            traceback.print_exc()
            PathError(path = fileName, pathType = model.ID)
            return
    
        self.dataCollection.add(model)

        newModelFrame = self.buildModelFrame(model = model)
        newModelFrame.grid(row = len(self.modelFrames) - 1, column = 0, pady = 5, padx = (5, 0))

    def saveCollection(self):
        if self.dataCollection.getPath() is None:
            self.saveCollectionAs()
            return

        try:
            self.dataCollection.save()
        except Exception:
            traceback.print_exc()
            PathError(path = self.dataCollection.getPath(), pathType = self.dataCollection.ID)
            return
        

    def saveCollectionAs(self):
        fileName = tkinter.filedialog.asksaveasfilename(initialdir = _CONFIG_["csv_dir"], title = "Save Collection As", filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        origPath = self.dataCollection.getPath()
        try:
            self.dataCollection.setPath(fileName)
            self.dataCollection.save()
        except Exception:
            traceback.print_exc()
            PathError(path = fileName, pathType = self.dataCollection.ID)
            self.dataCollection.setPath(origPath)

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

    def editDefaultValues(self, model):
        editCsv = EditModel(
            model = model, 
            controls = self.builderData["controls"]["edit"]
        )
        editCsv.pack()

    def reloadFrame(self, csvEditor, model):
        model.load()
        csvEditor.rebuild(model)

    def removeFrame(self, container, model):
        self.dataCollection.remove(model)
        self.modelFrames.remove(container.csvFrame)
        container.destroy()


