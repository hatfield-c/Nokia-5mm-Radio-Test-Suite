import core.DataController as Helper

from modules.DumpInput import DumpInput

class M_OBUE_Dump:

    def __init__(self, parameters, testbench):
        self.flatData = parameters
        self.parameters = Helper.DataController.GetDictionary(self.flatData)

        self.testbench = testbench
        self.MAX_CARRIERS = 8

        self.carriers = self.extract_carrier_vals(self.parameters)

    def run_test(self):
        self.parameters = self.flatData

        carrierData = { "key": "Carrier Data", "value": self.carriers }
        self.parameters.append(carrierData)

        childModule = DumpInput(
            parameters = self.parameters, 
            testbench = self.testbench
        )
        return childModule.run_test()

    def extract_carrier_vals(self, parameters):
        carrier_list = []

        #iterate through carriers
        for carrier_num in range(0, self.MAX_CARRIERS):
            c_key = ("Carrier%d"%carrier_num)
            fc_key = ("Center Frequency(GHz)%d"%carrier_num)
            bw_key = ("Channel Bandwidth(MHz)%d"%carrier_num)
            carrier = {}

            if fc_key in parameters:
                if parameters[fc_key] is not None and parameters[fc_key] != "":
                    carrier["Center Frequency(GHz)"] = parameters[fc_key]
                
                parameters.pop(fc_key)

                if bw_key in parameters:
                    if parameters[bw_key] is not None and parameters[bw_key] != "":
                        carrier["Channel Bandwidth(MHz)"] = parameters[bw_key]
                    
                    parameters.pop(bw_key)

            if c_key in parameters:
                parameters.pop(c_key)

            if carrier:
                carrier_list.append(carrier)

        return carrier_list