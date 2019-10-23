from menus.MenuFactory import MenuFactory
import tkinter

class SuiteEditorMenu(MenuFactory):
    def __init__(self, root = None):
        self.menuData = {
            "File": {
                "New Test Suite": "editSuite",
                "Load Test Suite": "editSuite"
            },
            "About": "about"
        }

        MenuFactory.__init__(self, root, self.menuData)

    def menuAction(self, actionStr, args):
        switcher = {
            "about": lambda : self.about(args),
            "editSuite": lambda : self.editSuite(args)
        }

        action = switcher.get(actionStr, None)
        action()

    def about(self, args):
        print("About!")

    def editSuite(self, args):
        print("Edit!")
