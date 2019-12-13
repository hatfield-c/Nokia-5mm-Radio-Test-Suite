import tkinter
import tkinter.filedialog
import os

from Config import _CONFIG_
from core.interfaces.SuiteManager import SuiteManager

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
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", lambda : self.exit())

        self.mainloop()

    def exit(self):
        shouldExit = self.suite.checkQuit()
        
        if not shouldExit:
            return
        
        self.destroy()

start = Application()