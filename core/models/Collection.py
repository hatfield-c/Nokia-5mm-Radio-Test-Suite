from Model import Model
from UIFactory import UIFactory
from models.Parameters import Parameters

class Collection(Model):
    
    def __init__(self, path, factory):
        super().__init__(path)
        self.models = []
        self.factory = factory

        self.name = UIFactory.TruncatePath(self.path, 45)

    def getName(self):
        return self.name

    def add(self, model):
        row = {}

        row[self.fields[0]] = model.getPath()

        self.models.append(row)
        super().add(row)

    def remove(self, model):

        row = {}

        row[self.fields[0]] = model.getPath()

        try:
            self.models.remove(row)
        except ValueError:
            pass

        super().remove(row)

    def load(self):
        super().load()

        self.models = []

        for row in self.data:
            if not set(self.fields).issubset(row):
                continue

            path = row[self.fields[0]]

            if path is None:
                continue

            model = self.factory.create(path)
            model.load()

            self.models.append(model)

    def getModels(self):
        return self.models