import tkinter
from menus.SuiteEditorMenu import SuiteEditorMenu
from menus.MenuFactory import MenuFactory

class Interface(tkinter.Frame):
    def __init__(self, title = "", root = None, menuBar = None, dimensions = "200x200"):
        self.title = title
        self.menuBar = menuBar

        if(root is None):
            self.root = tkinter.Toplevel()
            self.root.iconbitmap("media/icon.ico")
            self.root.geometry(dimensions)
            self.root.title(self.title)
        else:
            self.root = root
        
        tkinter.Frame.__init__(self, master=self.root)

        if self.menuBar is not None:
            self.menuBar.setRoot(self)
            self.root.config(menu = self.menuBar.getMenu())
        
        self.grid()

    def toWindow(self):
        Interface(title = self.title, menuBar = self.menuBar)

    def getRoot(self):
        return self.root

    def getFrame(self):
        return self.frame

    def getTitle(self):
        return self.title
