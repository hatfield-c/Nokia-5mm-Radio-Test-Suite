from core.Model import Model
from core.UIFactory import UIFactory
from core.models.Parameters import Parameters

class Collection(Model):
    
    def __init__(self, path, factory):
        super().__init__(path)
        self.models = []
        self.factory = factory

        self.name = UIFactory.TruncatePath(self.path, 45)

    def add(self, model):
        row = {}

        model.setIndex(self.newIndex())

        row[self.fields[0]] = model.getIndex
        row[self.fields[1]] = model.getPath()

        self.models.append(row)
        super().add(row)

    def remove(self, model):

        row = {}

        row[self.fields[0]] = model.getIndex()
        row[self.fields[1]] = model.getPath()

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

            path = row[self.fields[1]]

            if path is None:
                continue

            model = self.factory.create(path)
            model.load()

            index = row[self.fields[0]]
            model.setIndex(index)

            self.models.append(model)

    def newIndex(self):
        if len(self.models) == 0:
            return 1

        lastModel = self.models[len(self.models) - 1]
        return lastModel.getIndex() + 1

    def getModels(self):
        return self.models

    def getName(self):
        return self.name