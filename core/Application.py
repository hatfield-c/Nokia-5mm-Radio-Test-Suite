import tkinter
import os
import tkinter.filedialog
from menus.SuiteEditorMenu import SuiteEditorMenu
from menus.MenuFactory import MenuFactory
from Interface import Interface
from Editor import Editor
from interfaces.SuiteBuilder import SuiteBuilder
from Config import _CONFIG_
from interfaces.Alert import Alert

class Application(tkinter.Tk):
    def __init__(self):
        super().__init__()
        _CONFIG_["app_root"] = self
        _CONFIG_["working_dir"] = os.getcwd()
        _CONFIG_["working_dir"] = _CONFIG_["working_dir"].replace("\\", "/")

        self.iconbitmap(_CONFIG_["favicon"])

        self.suite = SuiteBuilder(title = _CONFIG_["app_title"], root = self)

        self.geometry(str(self.suite.dimensions['width']) + "x" + str(self.suite.dimensions['height']))
        self.title(_CONFIG_["app_title"])

        self.mainloop()


start = Application()

