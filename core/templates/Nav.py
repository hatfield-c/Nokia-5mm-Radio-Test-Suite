import tkinter
from Config import _CONFIG_
from templates.Divider import Divider
from PIL import ImageTk, Image

class Nav(tkinter.Frame):
    def __init__(self, root, data):
        tkinter.Frame.__init__(self, master = root, relief = "ridge", borderwidth = 1, width = 200, height = 601, background = _CONFIG_["color_primary"])
        self.grid_propagate(False)

        self.mainPanel = tkinter.Frame(self, width = 200, height = 150, background = _CONFIG_["color_primary"])
        self.delimiter = Divider(self, width = 200) #tkinter.Frame(self, width = 200, height = 1, bg = "black")
        self.steps = tkinter.Frame(self, width = 200, height = 450, background = _CONFIG_["color_primary"])

        self.mainPanel.grid_propagate(False)
        self.steps.grid_propagate(False)

        self.mainPanel.pack()
        self.delimiter.pack(pady = 10)
        self.steps.pack()

        self.buildMainPanel(data)
        self.buildStepsPanel(data)

    def buildMainPanel(self, data):
        img = ImageTk.PhotoImage(Image.open("media/logo.png"))
        self.logo = tkinter.Label(self.mainPanel, image = img, background = _CONFIG_["color_primary"])
        self.logo.image = img
        self.logo.pack()

        self.mainLabel = tkinter.Label(self.mainPanel, text = "TEST SUITE MANAGER\nv." + _CONFIG_["version"], font = "Helvetica 10 bold", background = _CONFIG_["color_primary"])
        self.mainLabel.pack(pady = (0, 10))

        self.fileLabel = tkinter.Label(self.mainPanel, text = "Current Suite:", background = _CONFIG_["color_primary"])
        self.fileLabel.pack(anchor = "w")

        self.fileField = tkinter.Entry(self.mainPanel, width = 32, justify = "right")
        self.fileField.insert(0, data[0]["csv_file"])
        self.fileField.xview_moveto(1)
        self.fileField.pack(pady = (0, 5))

    def buildStepsPanel(self, data):
        self.stepLabel = tkinter.Label(self.steps, text = "Suite Builder:", background = _CONFIG_["color_primary"])
        self.stepLabel.pack(anchor = "w", pady = (10, 0))

        self.stepList = tkinter.Frame(self.steps, bg = "white", relief = "ridge", borderwidth = 2, width = 200, height = 370)
        self.stepList.grid_propagate(False)
        self.stepList.columnconfigure(0, weight = 1)
        self.stepList.pack()

        i = 0
        self.stepsData = []
        for step, action in zip(data[1]["items"], data[1]["actions"]):
            editorButton = tkinter.Button(self.stepList, text = step, command = action, bg = "white", borderwidth = 0)
            editorButton.grid(row = i, column = 0, sticky = "w")
            self.stepsData.append(editorButton)
            i += 1

        self.navFooter = tkinter.Frame(self, width = 200, height = 29, background = _CONFIG_["color_primary"])
        self.navFooter.pack()