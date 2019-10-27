import tkinter
import tkinter.filedialog
from menus.SuiteEditorMenu import SuiteEditorMenu
from menus.MenuFactory import MenuFactory
from Interface import Interface
from Editor import Editor
from interfaces.TestSuiteBuilder import TestSuiteBuilder
from Config import _CONFIG_
from interfaces.Alert import Alert

class Application(tkinter.Tk):
    def __init__(self):
        super().__init__()
        _CONFIG_["true_root"] = self

        self.iconbitmap(_CONFIG_["favicon"])

        self.suite = TestSuiteBuilder(title = _CONFIG_["app_title"], root = self)

        self.geometry(str(self.suite.dimensions['width']) + "x" + str(self.suite.dimensions['height']))
        self.title(_CONFIG_["app_title"])

        self.mainloop()


start = Application()

