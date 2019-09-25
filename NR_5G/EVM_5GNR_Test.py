# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0

#       standard library imports
import sys
sys.path.insert(0, '')

#       third party imports

#       local imports
from NR_5G import EVM_Script as evm_scpi
from Support_Modules import csv_logger as csvr


class EVM_Test():

    def __init__(self, parameters = None, testbench = None, to_log = True):

        #EVM test doesnt contain much processing for parameters
        self.parameters = parameters
        self.testbench = testbench
        self.to_log = to_log


    def run_test(self):
        #open parameter package and send it to the script method
        feedback = evm_scpi.evm_script(
                        center_freq = self.parameters['Center Frequency(GHz)'],
                        attenuation = self.parameters['Attenuation(dBm)'],
                        alloc_file = self.parameters['Allocation File'],
                        qam = self.parameters['QAM PDSCH'])
        res = []
        res.append(feedback)

        if self.to_log is True:
            csvr.log_to_csv(res, self.testbench, "EVM_FREQ_ERR")

        return feedback


    def run_test_test(self):
        #C:\\R_S\\Instr\\user\\NR5G\\AllocationFiles\\DL\\Single Carrier\\64QAM_cellID1_papr13_120KHz_100MHz.allocation
        filepath = ('C:\\R_S\\Instr\\user\\NR5G\\AllocationFiles\\DL\\' +
                'Single Carrier\\64QAM_cellID1_papr13_120KHz_100MHz.allocation')
        evm_scpi.evm_script(center_freq = 37050000000,
                            attenuation = 10,
                            alloc_file = filepath)


if __name__ == '__main__':

    EVM_Test()
