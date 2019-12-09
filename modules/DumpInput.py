import time

class DumpInput:
    def __init__(self, parameters, testbench):
        self.parameters = parameters
        self.testbench = testbench

    def run_test(self):
        time.sleep(3)
        result = self.parameters
        result.extend(self.testbench)
        return result

