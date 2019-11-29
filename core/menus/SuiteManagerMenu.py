from core.menus.AbstractMenu import AbstractMenu
from core.DataController import DataController
from core.models.Suite import Suite
from core.UIFactory import UIFactory
from Config import _CONFIG_
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
            "saveSuite": lambda : self.root.saveSuite(args),
            "saveAsSuite": lambda : self.root.saveAsSuite(args),
            "newSuite": lambda : self.root.newSuite(args),
            "editSuite": lambda : self.root.editSuite(args)
        }

        action = switcher.get(actionStr, None)
        action()

    def about(self, args):
        print("About!")
