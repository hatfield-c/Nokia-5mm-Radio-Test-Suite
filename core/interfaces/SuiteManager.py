import tkinter
from core.Interface import Interface
from core.interfaces.builders.Empty import Empty
from core.interfaces.builders.BenchBuilder import BenchBuilder
from core.interfaces.builders.RunBuilder import RunBuilder
from core.interfaces.builders.SequenceBuilder import SequenceBuilder
from core.interfaces.Builder import Builder
from core.interfaces.Activation import Activation
from core.menus.SuiteManagerMenu import SuiteManagerMenu
from core.templates.Nav import Nav
from core.models.Suite import Suite
from Config import _CONFIG_

class SuiteManager(Interface):
    
    def __init__(self, title = "", root = None, modelData = None, dimensions = { "width": 1100, "height": 620}):
        super().__init__(title = title, root = root, dimensions = dimensions)
        self.menuBar = SuiteManagerMenu(self)
        self.initMenu()

        self.workspace = None
        self.nav = None
        self.rebuild(modelData = modelData)

        self.grid(row = 0, sticky = "nsew")

    def rebuild(self, modelData = None):

        if modelData is None:
            self.modelData = Suite(path = None)
        else:
            self.modelData = modelData

        if self.workspace is not None:
            self.workspace.destroy()

        if self.nav is not None:
            self.nav.destroy()

        self.workspace = tkinter.Frame(self)

        benches = BenchBuilder(root = self.workspace, csvPath = self.modelData.benches)
        runs = RunBuilder(root = self.workspace, csvPath = self.modelData.runs)
        sequences = SequenceBuilder(root = self.workspace, csvPath = self.modelData.sequences)
        testing = Activation(root = self.workspace, suite = self)
        empty = Empty(root = self.workspace, color = "blue")

        self.workspaces = {
            "benches": benches,
            "runs": runs,
            "sequences": sequences,
            "testing": testing,
            "empty": empty
        }

        if self.modelData.getPath() is None:
            currentFile = ""
        else:
            currentFile = self.modelData.getPath()

        self.nav = Nav(
            self,
            [
                {
                    "csv_file": currentFile
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
                        lambda : self.workspaces["testing"].lift()
                    ]
                }
            ]
        )

        for space in self.workspaces:
            self.workspaces[space].pack()
            if space != "empty":
                self.workspaces[space].place(x = 0, y = 0)

        footer = tkinter.Frame(self.workspace, width = 900, height = 50, background = _CONFIG_["color_primary"])
        footerBorder = tkinter.Frame(footer, width = 900, height = 1, background = "grey")
        footerLabel = tkinter.Label(footer, text = "Developed by UT Dallas Senior Design Team 904", font = "Helvetica 8 italic", height = 2, background = _CONFIG_["color_primary"])
        footerBorder.pack(pady = (1,0))
        footerLabel.pack()

        footer.pack()        
        self.nav.grid(row = 0, column = 0, sticky = "nw")
        self.workspace.grid(row = 0, column = 1, sticky = "ne")

    def save(self):
        self.modelData.setCollection(key = "benches", value = self.workspaces["benches"].csvPath)
        self.modelData.setCollection(key = "runs", value = self.workspaces["runs"].csvPath)
        self.modelData.setCollection(key = "sequences", value = self.workspaces["sequences"].csvPath)
        self.modelData.save()

    def compileData(self):
        data = {}

        data["benches"] = self.workspaces["benches"].compileData()
        data["runs"] = self.workspaces["runs"].compileData()
        data["sequences"] = self.workspaces["sequences"].compileData()

        return data