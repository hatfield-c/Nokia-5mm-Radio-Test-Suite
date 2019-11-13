class Parameter:
    def __init__(self, key, value, args):
        self.key = key
        self.value = value
        self.args = args

    def getKey(self):
        return self.key

    def getValue(self):
        return self.value

    def getArgs(self):
        return self.args

    def setKey(self):
        self.key = key

    def setValue(self, value):
        self.value = value

    def setArgs(self, args):
        self.args = args