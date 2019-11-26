import tkinter

class AbstractMenu():
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

    def menuAction(self, actionStr, args):
        pass

    def buildMenu(self, root, menuData):
        self.menuData = menuData
        self.menuBar = tkinter.Menu(root)

        for field in self.menuData:
            if isinstance(self.menuData[field], dict):
                subMenu = tkinter.Menu(self.menuBar, tearoff = 0)

                line = self.menuData[field]
                for subField in line:
                    subMenu.add_command(label = subField, command = lambda action = line[subField] : self.menuAction(actionStr = action, args = { "root": self.root }))

                    if(subField == 'Save As'):
                        subMenu.add_separator()

                self.menuBar.add_cascade(label = field, menu = subMenu)
            else:
                self.menuBar.add_command(label = field, command = lambda action = menuData[field] : self.menuAction(actionStr = action, args = { "root": self.root }))

