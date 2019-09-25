# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0

import sys
sys.path.insert(0, '')
from Support_Modules import csv_logger as csvr

from EIRP import EIRP_Script as eirp_scpi

class EIRP_Test():

    def __init__(self, parameters, testbench = None):

        #do some math.
        #from the parameters dic
        self.parameters = parameters
        self.testbench = testbench

    def run_test(self):
        #call EIRP script
        feedback = eirp_scpi.eirp_script(
                        center_freq = self.parameters['Center Frequency(GHz)'],
                        tx_bw = self.parameters['TX BW'],
                        adj_bw = self.parameters['Adjacent BW'],
                        alt_bw = self.parameters['Alternate BW'],
                        adj_space = self.parameters['Adjacent Spacing'],
                        alt_space = self.parameters['Alternate Spacing'],
                        user_standard = self.parameters['User Std.'],
                        testbench = self.testbench)
        res = []
        res.append(feedback)
        #logger requires a list of the responses.

        if to_log is True:
            csvr.log_to_csv(res, self.testbench, "EIRP_ACLR")

        return feedback



if __name__ == '__main__':

    eirp = EIRP_Test()
