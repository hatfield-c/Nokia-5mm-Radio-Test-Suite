# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0

import sys
sys.path.insert(0, '')
from Support_Modules import csv_logger as csvr

from ACLR import ACLR_Script as aclr_scpi

class ACLR_Test():

    def __init__(self, parameters, testbench = None, to_log = False):

        #do some math.
        #from the parameters dic
        self.parameters = parameters
        self.testbench = testbench
        self.to_log = to_log

    def run_test(self):
        #call aclr script
        feedback = aclr_scpi.aclr_script(
                        center_freq = self.parameters['Center Frequency(GHz)'],
                        tx_bw_MHz = self.parameters['TX BW(MHz)'],
                        adj_bw_MHz = self.parameters['Adjacent BW(MHz)'],
                        adj_space_MHz = self.parameters['Adjacent Spacing(MHz)'],
                        user_standard = self.parameters['User Std.'],
                        testbench = self.testbench)
        res = []
        res.append(feedback)
        #logger requires a list of the responses.

        if self.to_log is True:
            csvr.log_to_csv(res, self.testbench, "ACLR")

        return feedback



if __name__ == '__main__':

    aclr = ACLR_Test()
