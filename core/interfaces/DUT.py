from Config import _CONFIG_


import tkinter

class DUT(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.transient(self.parent)
        self.geometry("400x200")
        self.title("DUT")
        self.iconbitmap(_CONFIG_["favicon_path"])

        self.columnconfigure(0, weight = 1)

        self.label = tkinter.Label(self, text = "DEVICE UNDER TESTING", font = "Helevetica 12 bold underline")
        self.label.grid(row = 0, column = 0, pady = 10)
        
        self.msg = tkinter.Message(
            self, 
            text = "Please setup test bench as needed, and then press 'Continue' to proceed with the test sequence.",
            background = "white",
            width = 350,
            padx = 5,
            pady = 5
        )
        self.msg.grid(row = 1, column = 0, pady = (20, 0))

        self.submitButton = tkinter.Button(self, text = "Continue", padx = 10, command = lambda : self.close())
        self.submitButton.grid(row = 2, column = 0, pady = 20)

        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda : self.close())
        self.wait_window(self)  

    def close(self):
        self.destroy()