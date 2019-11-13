import tkinter
from Config import _CONFIG_

class Interface(tkinter.Frame):
    def __init__(self, title = "", root = None, menuBar = None, dimensions = None):
        self.title = title
        self.menuBar = menuBar
        self.dimensions = dimensions
        
        if(root is None):
            self.root = tkinter.Toplevel()
            self.root.iconbitmap(_CONFIG_["favicon"])
            self.root.geometry(str(self.dimensions['width']) + "x" + str(self.dimensions['height']))
            self.root.title(self.title)
        else:
            self.root = root
        
        if(self.dimensions is not None):
            super().__init__(master=self.root, width = dimensions["width"], height = dimensions["height"])
        else:
            super().__init__(master=self.root)
        
    def initMenu(self):
        if self.menuBar is not None:
            self.menuBar.setRoot(self)
            self.root.config(menu = self.menuBar.getMenu())

    def toWindow(self):
        Interface(title = self.title, menuBar = self.menuBar).initMenu()

    def getRoot(self):
        return self.root

    def getTitle(self):
        return self.title

    def nothing(self):
        pass
