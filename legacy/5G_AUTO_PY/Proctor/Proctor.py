#   Anthony Tang
#   Anthony.Tang@nokia.com

#standard library imports
import sys
import tkinter as tk
import os
from tkinter import filedialog
from tkinter import scrolledtext

#third party imports

#local imports
import TestClass


class Proctor():

    version = 0.1
    test_dic = {}
    active_test_mode = 0


    def __init__(self):

        #proctor gui startup.
        root = tk.Tk() #establish window.
        root.title('Proctor %s'% self.version)

        #create a pulldown menu
        mainframe = tk.Frame(root)
        mainframe.grid(column = 0, row = 0)

        #get res directory of scripts
        root.directory = filedialog.askdirectory(initialdir = "./",
                                title = "Select Tests Directory")
        print ("Reading in tests " + root.directory)
        directory_path = root.directory

        #gui should contain a drop down menu that corresponds to the test_dic
        #dictionary, the dictionary of available tests found in
        #provided directory.

        #make buttons dynamically with the keys of the the testdic.
        #gui things.
        test_board = tk.Frame(root)
        test_board.grid(sticky = tk.N + tk.W, row = 0, column = 0)
        test_buttons = {}

        self.test_specs = tk.Frame(root)
        self.test_specs.grid(sticky = tk.E + tk.N, row = 0, column = 1)

        #iterate though all files in the command directory.
        for filename in os.listdir(directory_path):
            #make a Test_Class in the testype dictionary with the
            #filename as the type.
            name, extension = filename.split('.')
            self.test_dic[name] = TestClass.TestClass(filename,
                                                        directory_path,
                                                        self.test_specs)

        index = 0
        for cmd in self.test_dic.keys():
            test_buttons[cmd] = tk.Radiobutton(test_board,
                                            text = cmd,
                                            variable = self.active_test_mode,
                                            value = cmd,
                                            command = lambda i = cmd:
                                                self.switchup_testmode(i)
                                            )
            test_buttons[cmd].grid(row = index, sticky = tk.W)
            index = index + 1 #increment button placement.


        root.mainloop()


    def switchup_testmode(self, cmd):
        #make whatever the buttons are be the keys.
        #test_board
        pass


if __name__ == "__main__":

    Proctor()
