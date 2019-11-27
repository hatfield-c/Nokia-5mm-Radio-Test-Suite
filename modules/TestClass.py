class TestClass:
    def __init__(self, parameters, testbench):
        self.parameters = parameters
        self.testbench = testbench

    def run_test(self):
        result = str(self.parameters) + "\n\n" + str(self.testbench) + "\n\n\n"
        return result

