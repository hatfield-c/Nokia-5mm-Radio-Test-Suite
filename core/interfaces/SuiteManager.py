import tkinter

from core.interfaces.builders.BenchBuilder import BenchBuilder
from core.interfaces.builders.RunBuilder import RunBuilder
from core.interfaces.builders.SequenceBuilder import SequenceBuilder
from core.interfaces.Builder import Builder

from core.Interface import Interface
from core.interfaces.Welcome import Welcome
from core.interfaces.Activation import Activation
from core.interfaces.alerts.PathError import PathError

from core.menus.SuiteManagerMenu import SuiteManagerMenu
from core.templates.Nav import Nav

from core.models.Suite import Suite
from core.models.ModelFactory import ModelFactory

from core.UIFactory import UIFactory
from Config import _CONFIG_

class SuiteManager(Interface):
    
    def __init__(self, title = "", root = None, modelData = None, dimensions = { "width": 1100, "height": 620}):
        super().__init__(title = title, root = root, dimensions = dimensions)

        self.modelFactory = ModelFactory(
            args = {
                "type": Suite.ID,
                "fields": [ "step", "csv_path" ],
                "default": [
                    { "step": "benches", "csv_path": "" },
                    { "step": "runs", "csv_path": "" },
                    { "step": "sequences", "csv_path": "" }
                ]
            }
        )

        self.menuBar = SuiteManagerMenu(root = self)
        self.initMenu()
        self.workspace = tkinter.Frame(self)
        self.nav = tkinter.Frame(self)

        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.rebuild(modelData = modelData)

        self.grid(row = 0, sticky = "nsew")

    def rebuild(self, modelData = None):

        if modelData is None:
            self.modelData = self.modelFactory.create(path = None)
        else:
            self.modelData = modelData

        self.workspace.destroy()
        self.nav.destroy()

        self.workspace = tkinter.Frame(self)
        self.workspaces = self.buildWorkspaces()

        self.nav = self.buildNav()

        for space in self.workspaces:
            self.workspaces[space].grid(row = 0, column = 0, sticky = "news")

        self.footer = tkinter.Frame(self.workspace, width = 900, height = 50, background = _CONFIG_["color_primary"])
        footerBorder = tkinter.Frame(self.footer, width = 900, height = 1, background = "grey")
        footerLabel = tkinter.Label(self.footer, text = "Developed by UT Dallas Senior Design Team 904", font = "Helvetica 8 italic", height = 2, background = _CONFIG_["color_primary"])
        footerBorder.pack(pady = (1,0))
        footerLabel.pack()

        self.footer.grid(row = 1, column = 0, sticky = "news")      

        self.nav.grid(row = 0, column = 0, sticky = "nw")
        self.workspace.grid(row = 0, column = 1, sticky = "ne")

    def saveSuite(self, args):
        if self.modelData.getPath() is None:
            self.newSuite(args = args)
            return

        self.modelData.setCollection(key = "benches", value = self.workspaces["benches"].csvPath)
        self.modelData.setCollection(key = "runs", value = self.workspaces["runs"].csvPath)
        self.modelData.setCollection(key = "sequences", value = self.workspaces["sequences"].csvPath)

        try:
            self.modelData.save()
        except Exception:
            PathError(path = self.modelData.getPath(), pathType = self.modelData.ID)

    def saveAsSuite(self, args):
        if self.modelData.getPath() is None:
            self.newSuite(args)
            return

        fileName = tkinter.filedialog.asksaveasfilename(initialdir = _CONFIG_["csv_dir"], title = "Save As", filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        suiteData = self.modelData
        newSuite = self.modelFactory.create(path = fileName)
        newSuite.setData(fields = suiteData.getFields(), data = suiteData.getData())

        try:
            newSuite.save()
        except Exception:
            PathError(path = newSuite.getPath(), pathType = newSuite.ID)
    
        self.rebuild(modelData = newSuite)

    def newSuite(self, args):
        fileName = tkinter.filedialog.asksaveasfilename(initialdir = _CONFIG_["csv_dir"], title = "New Suite File", filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        newSuite = self.modelFactory.create(path = fileName)

        try:
            newSuite.save()
        except Exception:
            PathError(path = newSuite.getPath(), pathType = newSuite.ID)
        
        self.rebuild(modelData = newSuite)

    def editSuite(self, args):
        fileName = tkinter.filedialog.askopenfilename(initialdir = _CONFIG_["csv_dir"], title = "Load Test Suite", filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        suite = self.modelFactory.create(path = fileName)

        try:
            suite.load()
        except Exception:
            PathError(path = suite.getPath(), pathType = suite.ID)
        
        self.rebuild(modelData = suite)

    def compileData(self):
        data = {}

        data["benches"] = self.workspaces["benches"].compileData()
        data["runs"] = self.workspaces["runs"].compileData()
        data["sequences"] = self.workspaces["sequences"].compileData()

        return data

    def buildWorkspaces(self):
        if self.modelData.getPath() is not None:
            runs = RunBuilder(
                root = self.workspace, 
                csvPath = self.modelData.runs
            )
            sequences = SequenceBuilder(
                root = self.workspace, 
                csvPath = self.modelData.sequences
            )
            activation = Activation(
                root = self.workspace, 
                suite = self
            )
            benches = BenchBuilder(
                root = self.workspace, 
                csvPath = self.modelData.benches
            )
        else:
            runs = Welcome(root = self.workspace)
            sequences = Welcome(root = self.workspace)
            activation = Welcome(root = self.workspace)
            benches = Welcome(root = self.workspace)

        workspaces = {
            "runs": runs,
            "sequences": sequences,
            "activation": activation,
            "benches": benches
        }

        return workspaces

    def buildNav(self):
        return Nav(
            self,
            [
                {
                    "csv_file": self.modelData.getPath()
                },
                {
                    "items": [
                        "1. Bench Builder",
                        "2. Run Builder",
                        "3. Sequence Builder",
                        "4. Begin Testing"
                    ],
                    "actions": [
                        lambda : self.workspaces["benches"].lift(),
                        lambda : self.workspaces["runs"].lift(),
                        lambda : self.workspaces["sequences"].lift(),
                        lambda : self.workspaces["activation"].lift()
                    ]
                }
            ]
        )