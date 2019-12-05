import tkinter
from Config import _CONFIG_

class CheckQuit(tkinter.Toplevel):
    def __init__(self, parent, missingCollection):
        super().__init__(parent)
        self.parent = parent

        self.transient(self.parent)
        self.resizable(False, False)
        self.iconbitmap(_CONFIG_["favicon_path"])
        self.geometry("400x300")
        self.title("Missing Collection")

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        self.label = tkinter.Label(self, text = "CONFIRM QUIT?", font = "Helevetica 12 bold underline")
        self.label.grid(row = 0, column = 0, columnspan = 2, pady = 10)

        message = "You attempted to exit the application without setting the collection for '" + str(missingCollection) + "'.\n\n"
        message += "This can occur if you built a suite without saving it, or if you are intentionally leaving the suite unfinished.\n\n"
        message += "Click 'Cancel', and then navigate to:\n"
        message += "      File > Save Suite\n\n"
        message += "To save the current suite, or click 'Quit' to proceed with your exit."
        self.message = tkinter.Message(self, text = message, width = 375, background = "white", borderwidth = 2, relief = "groove")
        self.message.grid(row = 1, column = 0, columnspan = 2, pady = 20)

        self.quitButton = tkinter.Button(self, text = "Quit", padx = 10, command = lambda : self.quit())
        self.quitButton.grid(row = 2, column = 0, pady = 10, padx = (100, 0))

        self.cancelButton = tkinter.Button(self, text = "Cancel", padx = 10, command = lambda : self.cancel())
        self.cancelButton.grid(row = 2, column = 1, pady = 10, padx = (0, 100))

        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda : self.exit())
        self.wait_window(self)

    def quit(self):
        self.parent.quit = True
        self.exit()  

    def cancel(self):
        self.parent.quit = False
        self.exit()

    def exit(self):
        self.destroy()