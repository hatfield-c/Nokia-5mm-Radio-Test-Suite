from Editor import Editor
import tkinter
#from Tkinter import *

class Empty(Editor):
    def __init__(self, root =None ):
        super().__init__(title = "", root = root)

        self.container = tkinter.Frame(self, width = self.dimensions["width"],
         height = self.dimensions["height"])

        # Make your changes here,
        ##########################################
        self.deleteThis = tkinter.Label(self.container,
         text = "\tWELCOME TO THE NOKIA TEST AUTOMATION SUITE.\n\n"
         + "This suite will allow for Test Bench Configuration and Building.\n"
         + "\tTo get started, choose a Bench builder and enter appropriate data in the required fields.\n"
         + "\t\t\tWhen Bulding a bench, you can enter new values or load previously saved values and make changes.\n"
         +" Once fields are filled, Run and Sequence the builder.\n"
         +" Then begin your Test. ")

        self.deleteThis.pack()#side = LEFT)
        ##########################################

        self.container.grid(row = 0, column = 0, pady = 20, padx = 20)
