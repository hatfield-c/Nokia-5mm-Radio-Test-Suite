#   Anthony Tang
#   Anthony.Tang@nokia.com

import sys
import os
import BlockClass as blocks
from pathlib import Path


class CommandBlocks():

    cmd_palette = {}

    #sends the dictionary
    def send_config(self, conf_num):
        for line in (self.configurations[conf_num]):
            os.system(line)

    #both directions for the doubly linked list that CommandBlocks
    #intends to implement
    def __init__(self, command_directory):

        #read every file in directory.
        #filename acts as the name of the command.
        #read contents in as list. send these all to the block class.
        for filename in Path(command_directory).glob('*.sh'):
            #file name acts as the name of the command.
            script = self.read_in_script(filename)
            self.cmd_palette[filename] = blocks.BlockClass(filename, script)

        # for cmd in self.cmd_palette:
        #     print(cmd)
        #     print(self.cmd_palette[cmd].cmd_list)


    def read_in_script(self, filename):
        print(filename)
        script = []
        #ty stack overflow.
        #reads ignoring comments #
        for line in open(filename, 'r'):
            li=line.strip()
            if not li.startswith("#"):
                script.append(li)
        return script
