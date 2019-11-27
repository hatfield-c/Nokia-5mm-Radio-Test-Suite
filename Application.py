import tkinter
import tkinter.filedialog
import os
from core.Interface import Interface
from core.interfaces.SuiteManager import SuiteManager
from Config import _CONFIG_
from core.interfaces.Alert import Alert

class Application(tkinter.Tk):
    def __init__(self):
        super().__init__()
        _CONFIG_["app_root"] = self
        _CONFIG_["working_dir"] = os.getcwd()
        _CONFIG_["working_dir"] = _CONFIG_["working_dir"].replace("\\", "/")

        self.iconbitmap(_CONFIG_["favicon_path"])

        self.suite = SuiteManager(title = _CONFIG_["app_title"], root = self)

        self.geometry(str(self.suite.dimensions['width']) + "x" + str(self.suite.dimensions['height']))
        self.title(_CONFIG_["app_title"])

        self.mainloop()


start = Application()