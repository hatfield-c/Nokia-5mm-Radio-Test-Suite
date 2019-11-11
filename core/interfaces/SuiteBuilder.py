import tkinter
from Interface import Interface
from editors.Empty import Empty
from editors.BenchEditor import BenchEditor
from Editor import Editor
from menus.SuiteEditorMenu import SuiteEditorMenu
from templates.Nav import Nav
from models.Suite import Suite
from Config import _CONFIG_

class SuiteBuilder(Interface):
    
    def __init__(self, title = "", root = None, modelData = None, dimensions = { "width": 1100, "height": 620}):
        super().__init__(title = title, root = root, dimensions = dimensions)
        self.menuBar = SuiteEditorMenu(self)
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

        benches = BenchEditor(root = self.workspace, csvPath = self.modelData.benches)
        runs = Editor(root = self.workspace, csvPath = None, color = "orange")
        sequences = Editor(root = self.workspace, csvPath = None, color = "red")
        testing = Empty(root = self.workspace, color = "lightgreen")
        empty = Editor(root = self.workspace, color = "blue")

        workspaces = {
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
                        lambda : workspaces["benches"].lift(),
                        lambda : workspaces["runs"].lift(),
                        lambda : workspaces["sequences"].lift(),
                        lambda : workspaces["testing"].lift()
                    ]
                }
            ]
        )

        for space in workspaces:
            workspaces[space].pack()
            if space != "empty":
                workspaces[space].place(x = 0, y = 0)

        footer = tkinter.Frame(self.workspace, width = 900, height = 50, background = _CONFIG_["color_primary"])
        footerBorder = tkinter.Frame(footer, width = 900, height = 1, background = "grey")
        footerLabel = tkinter.Label(footer, text = "Developed by UT Dallas Senior Design Team 904", font = "Helvetica 8 italic", height = 2, background = _CONFIG_["color_primary"])
        footerBorder.pack(pady = (1,0))
        footerLabel.pack()

        footer.pack()        
        self.nav.grid(row = 0, column = 0, sticky = "nw")
        self.workspace.grid(row = 0, column = 1, sticky = "ne")