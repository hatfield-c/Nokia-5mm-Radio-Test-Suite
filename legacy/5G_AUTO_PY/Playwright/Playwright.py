#   Anthony Tang
#   Anthony.Tang@nokia.com

#standard library imports
import sys
sys.path = sys.path[0] #remove existing path
import site
rootDir = sys.path[0] #new path from cwd.
site.addsitedir(rootDir + '\\Lib\site-packages')
print(rootDir)

import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
import os

#third party imports
import scp

#local imports
from CommandBlocks import CommandBlocks as cmdblks
import DUTOverseer as dut

class Playwright():

    version = 1.5
    command_block_btns = []
    cold_start = True
    #empty new list for sequence.
    #the sequence list will track the command blocks the way lists do.
    #provide path for that stuff.

    device_ip = '192.168.100.1'
    port_number = int('22')
    usr = 'root'
    pwd = 'umniedziala'

    def __init__(self):
        #execute on main.
        print("Hello")

        root = tk.Tk() #establish window.
        root.title('Playwright %s'% self.version)

        #get res directory of scripts
        root.directory = filedialog.askdirectory(initialdir = "./",
                            title = "Select Command Directory")
        print ("parsing command blocks from " + root.directory)

        self.command_blocks = cmdblks(root.directory)

        #gui things.
        palette = tk.scrolledtext.ScrolledText(root)
        palette.grid(sticky = tk.N + tk.W)

        #scrolled text master box.
        self.masterscript_txtbx = tk.scrolledtext.ScrolledText(
                                        root,
                                        state = tk.NORMAL)
        self.masterscript_txtbx.grid(row = 0, column = 1, sticky = tk.N)

        palette_buttons = {}
        x = 0

        for cmd in self.command_blocks.cmd_palette:
            name = self.command_blocks.cmd_palette[cmd].getName()
            palette_buttons[cmd] = tk.Button(palette,
                                            text = name,
                                            command = lambda i = cmd:
                                                self.add_command_block(i)
                                            )
            palette_buttons[cmd].grid(row = x, sticky = tk.W)
            x = x + 1 #increment button placement.


        #self.cold_start = tk.Checkbutton(palette, text = "Cold Start",
        #                                variable = self.cold_start)
        #self.cold_start.grid(row = x, column = 0, sticky = tk.N)
        #x = x+1

        #cold start needs to be hooked up to correspond to something.
        #Cold start mode should add a ten minute delay between the
        #configuration.

        start_test_btn = tk.Button(root,
                                    text = "SEND SCRIPT", bg = 'light green',
                                    command = lambda :
                                        self.send_script_to_module())
        start_test_btn.grid(row = 1, column = 1, sticky = tk.S + tk.W)

        #button allows you to save active display window as script.
        to_script_btn = tk.Button(root,
                                    text = "SAVE SCRIPT",
                                    bg = 'yellow',
                                    command = lambda:
                                        self.save_script_to_file(root) )
        to_script_btn.grid(row = 2, column = 1, sticky = tk.S + tk.W)

        #lets the GUI happen.
        root.mainloop()


    def add_command_block(self, cmd):

        for line in self.command_blocks.cmd_palette[cmd].cmd_list:
            self.masterscript_txtbx.insert(tk.END, line + '\n')

        #spacer line between command blocks
        self.masterscript_txtbx.insert(tk.END, "\n")


    def save_script_to_file(self, root):

        #run its go time.
        raw_script= self.its_go_time()
        #write raw script to new file.
        #open up a new file that we'll write to.
        root.filename = filedialog.asksaveasfilename(initialdir = "./",
                        title = "Save Script",
                        filetypes = (("shell","*.sh"),("all files","*.*")))

        #write all lines to the new file.
        with open(root.filename, 'w') as f:
            for line in raw_script:
                f.write("%s\n" % line)
        return

    def send_script_to_module(self):

        #TESTING CODE
        return

        raw_script = self.its_go_time()
        ssh = dut.DUTOverseer(self.device_ip,
                                self.port_number,
                                self.usr,
                                self.pwd)
        for line in raw_script:
            ssh.exec_command(line)


    def its_go_time(self):
        #convert the current display into a script to output.
        #add something that ignores anything following the # mark
        #to filter out comments.
        input = (self.masterscript_txtbx.get("1.0", tk.END)).split('\n')
        raw_script = []

        for line in input:
            if line:
                if not (line.startswith("#")):
                    line = line.partition('#')[0].strip() #split off comments
                    raw_script.append(line)

        print(raw_script)
        return raw_script
        #return rawscript, the list of strings that corresponds to the
        #in order master script stripped of invalid text.


#--------------------------------------------------------------------------
#                                  MAIN FUNCTION
#--------------------------------------------------------------------------
if __name__ == "__main__":
    Playwright()
