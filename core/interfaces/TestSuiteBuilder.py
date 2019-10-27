import tkinter
from Interface import Interface
from editors.Empty import Empty
from Editor import Editor
from menus.SuiteEditorMenu import SuiteEditorMenu
from Nav import Nav
from CSVObject import CSVObject

class TestSuiteBuilder(Interface):
    
    def __init__(self, title = "", root = None, data = None, dimensions = { "width": 1100, "height": 620}):
        super().__init__(title = title, root = root, dimensions = dimensions)
        self.menuBar = SuiteEditorMenu(self)
        self.initMenu()

        self.workspace = None
        self.nav = None
        self.rebuild(data = data)

        self.grid(row = 0, sticky = "nsew")

    def rebuild(self, data = None):

        if data is None:
            self.data = CSVObject(rowsList = [], fields = {}, path = "")
        else:
            self.data = data


        if self.workspace is not None:
            self.workspace.destroy()

        if self.nav is not None:
            self.nav.destroy()

        self.workspace = tkinter.Frame(self)

        benches = Editor(root = self.workspace, data = self.data, color = "green")
        runs = Editor(root = self.workspace, data = self.data, color = "orange")
        sequences = Editor(root = self.workspace, data = self.data, color = "red")
        testing = Editor(root = self.workspace, data = self.data, color = "lightgreen")
        empty = Editor(root = self.workspace, color = "blue")

        workspaces = {
            "benches": benches,
            "runs": runs,
            "sequences": sequences,
            "testing": testing,
            "empty": empty
        }

        self.nav = Nav(
            self,
            [
                {
                    "csv_file": self.data.getPath()
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

        footer = tkinter.Frame(self.workspace, width = 900, height = 50)
        footerLabel = tkinter.Label(footer, text = "Developed by UT Dallas Senior Design Team 904", font = "Helvetica 8 italic", height = 2)
        footerLabel.pack()

        footer.pack()        
        self.nav.grid(row = 0, column = 0, sticky = "nw")
        self.workspace.grid(row = 0, column = 1, sticky = "ne")