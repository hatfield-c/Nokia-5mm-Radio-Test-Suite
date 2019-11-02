import tkinter
from PIL import ImageTk, Image

class Nav(tkinter.Frame):
    def __init__(self, root, data):
        tkinter.Frame.__init__(self, master = root, relief = "ridge", borderwidth = 1, width = 200, height = 600)
        self.grid_propagate(False)

        self.mainPanel = tkinter.Frame(self, width = 200, height = 150)
        self.delimiter = tkinter.Frame(self, width = 200, height = 1, bg = "black")
        self.steps = tkinter.Frame(self, width = 200, height = 450)

        self.mainPanel.grid_propagate(False)
        self.steps.grid_propagate(False)

        self.mainPanel.pack()
        self.delimiter.pack(pady = 10)
        self.steps.pack()

        self.buildMainPanel(data)
        self.buildStepsPanel(data)

    def buildMainPanel(self, data):
        img = ImageTk.PhotoImage(Image.open("media/logo.png"))
        self.logo = tkinter.Label(self.mainPanel, image = img)
        self.logo.image = img
        self.logo.pack()

        self.mainLabel = tkinter.Label(self.mainPanel, text = "TEST SUITE BUILDER\nv0.05", font = "Helvetica 10 bold")
        self.mainLabel.pack(pady = (0, 10))

        self.fileLabel = tkinter.Label(self.mainPanel, text = "Current Suite:")
        self.fileLabel.pack(anchor = "w")

        self.fileField = tkinter.Entry(self.mainPanel, width = 32, justify = "right")
        self.fileField.insert(0, data[0]["csv_file"])
        self.fileField.xview_moveto(1)
        self.fileField.pack(pady = (0, 5))

    def buildStepsPanel(self, data):
        self.stepLabel = tkinter.Label(self.steps, text = "Suite Builder:")
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

        self.navFooter = tkinter.Frame(self, width = 200, height = 29)
        self.navFooter.pack()