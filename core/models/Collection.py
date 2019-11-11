from Model import Model
from UIFactory import UIFactory
from models.Parameters import Parameters

class Collection(Model):
    
    def __init__(self, path):
        super().__init__(path)
        self.models = {}

        self.name = UIFactory.TruncatePath(self.path, 45)

    def getName(self):
        return self.name

    def add(self, parameters):
        row = {}

        row[self.fields[0]] = parameters.getParameter("name")
        row[self.fields[1]] = parameters.getPath()

        super().add(row)

    def load(self):
        super().load()

        self.models = {}

        for row in self.data:
            if not set(self.fields).issubset(row):
                continue

            path = row["csv_path"]

            if path is None:
                continue

            parameters = Parameters(path)
            parameters.load()
            name = parameters.getParameter(key = "name")
            self.models[name] = parameters

    def getModels(self):
        return self.models