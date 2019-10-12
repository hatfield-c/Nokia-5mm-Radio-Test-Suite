#   Anthony Tang
#   Anthony.Tang@nokia.com

import sys
import os


class BlockClass():

    def __init__(self, filename, cmd_list):
        self.name = os.path.splitext(os.path.basename(filename))[0]
        self.cmd_list = cmd_list
        #for line in cmd_list:
        #    print(line)

    #send all instruction in the block class as defined by the cmd_list.
    def send_block(self):
        for cmd in self.cmd_list:
            os.system(cmd)

    def getScript(self):
        return self.cmd_list

    def getName(self):
        return self.name
