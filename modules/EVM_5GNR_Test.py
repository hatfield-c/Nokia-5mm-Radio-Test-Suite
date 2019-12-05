# Anthony Tang anthony.tang@nokia.com
# https://gitlabe2.ext.net.nokia.com/anttang/FSW_Automation.git
# Python 3.7.0

#       standard library imports
import sys
#       third party imports

#       local imports
import modules.SCPI_Scripts.EVM_Script as evm_scpi

class EVM_5GNR_Test():

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
                        alloc_file = self.parameters['Allocation Filepath'],
                        correction_file = self.parameters['Correction Filepath'],
                        cell_number = self.parameters['Number Carriers'],
                        qam = self.parameters['QAM PDSCH'])
        res = []
        res.append(feedback)

        # if self.to_log is True:
        #     csvr.log_to_csv(res, self.testbench, "EVM_FREQ_ERR")

        return feedback


if __name__ == '__main__':
    EVM_Test()
