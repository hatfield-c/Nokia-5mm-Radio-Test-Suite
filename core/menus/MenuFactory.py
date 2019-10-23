import tkinter

class MenuFactory():
    def __init__(self, root, menuData):
        self.menuData = menuData
        self.root = root
        self.menuBar = None

        self.buildMenu(self.root, self.menuData)

    def getMenu(self):
        self.buildMenu(self.root, self.menuData)
        return self.menuBar

    def setMenuData(self, menuData):
        self.menuData = menuData

    def setInterface(self, interface):
        self.root = interface.root
        self.buildMenu(self.root, self.menuData)

    def setRoot(self, root):
        self.root = root
        self.buildMenu(self.root, self.menuData)

    def menuAction(self, action, args):
        pass

    def buildMenu(self, root, menuData):
        self.menuBar = tkinter.Menu(root)
        for field in menuData:
            if isinstance(menuData[field], dict):
                subMenu = tkinter.Menu(self.menuBar, tearoff = 0)

                line = menuData[field]
                for subField in line:
                    subMenu.add_command(label = subField, command = lambda : self.menuAction(line[subField], None))

                self.menuBar.add_cascade(label = field, menu = subMenu)
            else:
                self.menuBar.add_command(label = field, command = lambda : self.menuAction(menuData[field], None))

