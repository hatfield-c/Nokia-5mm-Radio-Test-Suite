from modules.M_OBUE_Test import M_OBUE_Test

class M_OBUE_Standard:

    def __init__(self, parameters, testbench):
        self.parameters = parameters
        self.testbench = testbench

        carrierList = []
        for paramKey in self.parameters:
            paramVal = self.parameters[paramKey]
            paramVal = str(paramVal)

            strBegin = paramVal.find("Carrier")

            if strBegin < 0:
                continue

            length = len("Carrier")
            strEnd = strBegin + length + 1
            carrierString = paramVal[strBegin:strEnd]
            carrierNum = carrierString[-1]

            carrierData = self.extractCarrierData(carrierNum)

            if carrierData is not None:
                carrierList.append(carrierData)
        
        self.carriers = carrierList

    def run_test(self):
        childModule = M_OBUE_Test(
            parameters = self.parameters, 
            carrier_list = self.carriers, 
            testbench = self.testbench
        )
        return childModule.run_test()

    def extractCarrierData(self, carrierNum):
        centerFreq = None
        for paramKey in self.parameters:
            paramVal = str(self.parameters[paramKey])
            strBegin = paramKey.find("Center Frequency(GHz)")
            
            if strBegin < 0:
                continue

            length = len("Center Frequency(GHz)")
            strEnd = strBegin + length + 1
            freqStr = paramKey[strBegin:strEnd]
            freqNum = freqStr[-1]

            if freqNum == carrierNum:
                centerFreq = paramVal

        if centerFreq is None:
            return None

        bandwidth = None
        for paramKey in self.parameters:
            paramVal = str(self.parameters[paramKey])
            strBegin = paramKey.find("Channel Bandwidth(MHz)")

            if strBegin < 0:
                continue

            length = len("Channel Bandwidth(MHz)")
            strEnd = strBegin + length + 1
            bandStr = paramKey[strBegin:strEnd]
            bandNum = bandStr[-1]

            if bandNum == carrierNum:
                bandwidth = paramVal

        if bandwidth is None:
            return None

        return { "Center Frequency(GHz)": centerFreq, "Channel Bandwidth(MHz)": bandwidth }