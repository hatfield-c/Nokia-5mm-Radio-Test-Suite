from menus.MenuFactory import MenuFactory
from Config import _CONFIG_
from DataController import DataController
from CSVObject import CSVObject
import tkinter

class SuiteEditorMenu(MenuFactory):
    def __init__(self, root = None):
        self.menuData = {
            "File": {
                "New Test Suite": "newSuite",
                "Load Test Suite": "editSuite"
            },
            "About": "about"
        }

        MenuFactory.__init__(self, root, self.menuData)

    def menuAction(self, actionStr, args):
        switcher = {
            "about": lambda : self.about(args),
            "newSuite": lambda : self.newSuite(args),
            "editSuite": lambda : self.editSuite(args)
        }

        action = switcher.get(actionStr, None)
        action()

    def about(self, args):
        print("About!")

    def newSuite(self, args):
        fileName = tkinter.filedialog.asksaveasfilename(initialdir = _CONFIG_["csv_dir"], title = "NEW SUITE FILE", filetypes = [("csv files", "*.csv")])
        
        if ".csv" not in fileName:
            fileName += ".csv"

        data = CSVObject(rowsList = None, fields = None, path = fileName)
        self.root.rebuild(data = data)

    def editSuite(self, args):
        fileName = tkinter.filedialog.askopenfilename(initialdir = _CONFIG_["csv_dir"], title = "LOAD TEST SUITE", filetypes = [("csv files", "*.csv")])

        data = DataController.Load(fileName)
        self.root.rebuild(data = data)

