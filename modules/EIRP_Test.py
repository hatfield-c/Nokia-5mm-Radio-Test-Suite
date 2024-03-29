# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0

import sys
#from legacy.Support_Modules import csv_logger as csvr

import modules.SCPI_Scripts.EIRP_Script as eirp_scpi
import core.DataController as Helper

class EIRP_Test():

    def __init__(self, parameters, testbench = None):
        
        flatParameters = parameters
        flatTestbench = testbench
        parameters = Helper.DataController.GetDictionary(flatParameters)
        testbench = Helper.DataController.GetDictionary(flatTestbench)

        #do some math.
        #from the parameters dic
        self.parameters = parameters
        self.testbench = testbench

    def run_test(self):
        #call EIRP script
        feedback = eirp_scpi.eirp_script(
                        center_freq = self.parameters['Center Frequency(GHz)'],
                        tx_bw = self.parameters['TX BW(MHz)'],
                        adj_bw = self.parameters['Adjacent BW(MHz)'],
                        adj_space = self.parameters['Adjacent Spacing(MHz)'],
                        user_standard = self.parameters['User Std.'],
                        testbench = self.testbench)
        res = []
        res.append(feedback)
        #logger requires a list of the responses.

        return feedback



if __name__ == '__main__':

    eirp = EIRP_Test()
