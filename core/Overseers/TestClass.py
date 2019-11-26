class TestClass:
    def __init__(self, parameters, bench):
        self.parameters = parameters
        self.bench = bench

    def activate(self):
        result = str(self.parameters) + "\n\n" + str(self.bench) + "\n\n\n"
        return result

