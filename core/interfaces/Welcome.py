from core.interfaces.Builder import Builder
from core.Interface import Interface
from Config import _CONFIG_
import tkinter

class Welcome(Interface):
    def __init__(self, title = "Welcome", root = None):
    
        super().__init__(title = title, root = root, dimensions = Builder.DEFAULT_DIMENSIONS)

        self.grid_propagate(False)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)

        self.container = tkinter.Frame(self)
        
        self.container.columnconfigure(0, weight = 1)
        
        
        logoPath = _CONFIG_["icon_path"]
        img = tkinter.PhotoImage(file = logoPath)
        self.icon = tkinter.Label(
            self.container, 
            image = img, 
            background = _CONFIG_["color_primary"],
            borderwidth = 8,
            relief = "groove"
        )
        
        self.icon.image = img
        self.icon.grid(row = 0, column = 0, pady = (40, 20))

        self.welcomeLabel = tkinter.Label(
            self.container,
            text = "WELCOME!",
            font = "Helevetica 16 bold"
        )
        self.welcomeLabel.grid(row = 1, column = 0, pady = (0, 25))

        msg = (
            "\nWelcome to the Nokia" + u"\u2122" + " Automated Test Suite Manager.\n\n" + 
            "This application uses a centralized Test Suite CSV File that references other CSV files which contain unit parameter data.\n" + 
            "Please load a Test Suite CSV File to begin using this application, or generate one by building a new Test Suite.\n\n" + 
            "To load a Suite, navigate on the menu bar to 'File > Load Test Suite'.\n" + 
            "To build a new Suite, navigate on the menubar to 'File > New Test Suite'.\n\n" +
            "Please test responsibly. Do not attempt to operate a motor vehicle while testing.\n"
        )

        self.msgContainer = tkinter.Frame(
            self.container,
            background = "white",
            borderwidth = 2,
            relief = "groove"
        )
        self.msgContainer.grid(row = 2, column = 0)

        self.msgLabel = tkinter.Label(
            self.msgContainer, 
            text = msg, 
            font = "Helevetica 11",
            background = "white"
        )
        self.msgLabel.grid(row = 0, column = 0, padx = 10, pady = 5)
        
        self.container.grid(row = 0, column = 0, sticky = "nsew")
        