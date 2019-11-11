from Model import Model

class Parameters(Model):
    
    def __init__(self, path = ""):
        self.fields = ["key", "value"]
        super().__init__(path)
        self.fullData = { "name": "" }

    def load(self):
        super().load()

        self.fullData = { "name": "" }

        for row in self.data:
            self.fullData[row["key"]] = row["value"]

    def save(self):
        data = []

        for key in self.fullData:
            row = {"key": key, "value": self.fullData[key]}
            data.append(row)

        self.data = data
        print(self.data)
        super().save()

    def setParameter(self, key, value):
        self.fullData[key] = value

    def getParameter(self, key = None):

        if key is None:
            return self.fullData
        
        if key in self.fullData:
            return self.fullData[key]

        return {}

