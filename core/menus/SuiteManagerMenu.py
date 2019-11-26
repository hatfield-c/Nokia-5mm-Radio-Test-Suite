from menus.AbstractMenu import AbstractMenu
from Config import _CONFIG_
from DataController import DataController
from models.Suite import Suite
from UIFactory import UIFactory
import tkinter

class SuiteManagerMenu(AbstractMenu):
    def __init__(self, root = None):
        self.menuData = {
            "File": {
                "Save Suite": "saveSuite",
                "Save As": "saveAsSuite",
                "New Test Suite": "newSuite",
                "Load Test Suite": "editSuite"
            },
            "About": "about"
        }

        super().__init__(root, self.menuData)

    def menuAction(self, actionStr, args):
        switcher = {
            "about": lambda : self.about(args),
            "saveSuite": lambda : self.saveSuite(args),
            "saveAsSuite": lambda : self.saveAsSuite(args),
            "newSuite": lambda : self.newSuite(args),
            "editSuite": lambda : self.editSuite(args)
        }

        action = switcher.get(actionStr, None)
        action()

    def about(self, args):
        print("About!")

    def saveSuite(self, args):
        suite = args["root"]
        suite.save()

    def saveAsSuite(self, args):
        fileName = tkinter.filedialog.asksaveasfilename(initialdir = _CONFIG_["csv_dir"], title = "Save As", filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        suiteData = args["root"].modelData
        newSuite = Suite(fileName)
        newSuite.setData(fields = suiteData.getFields(), data = suiteData.getData())
        newSuite.save()

        self.root.rebuild(modelData = newSuite)

    def newSuite(self, args):
        fileName = tkinter.filedialog.asksaveasfilename(initialdir = _CONFIG_["csv_dir"], title = "New Suite File", filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        data = Suite(path = fileName)
        data.save()
        self.root.rebuild(modelData = data)

    def editSuite(self, args):
        fileName = tkinter.filedialog.askopenfilename(initialdir = _CONFIG_["csv_dir"], title = "Load Test Suite", filetypes = [("csv files", "*.csv")])

        if fileName is None or fileName == "":
            return

        data = Suite(fileName)
        data.load()
        self.root.rebuild(modelData = data)

