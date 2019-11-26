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

    def setKey(self, key):
        self.key = key

    def setValue(self, value):
        self.value = value

    def setArgs(self, args):
        self.args = args

    def toString(self):
        string = ""

        if self.value is not None:
            string += "[Key: " + self.key + "] "
            string += "[Value: " + self.value + "] "
        else:
            string += "[Key: None] "
            string += "[Value: None] "

        for argKey in self.args:
            string  += "[" + argKey + ": " + self.args[argKey] + "] "

        return string

        