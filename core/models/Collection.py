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
        model.setIndex(self.newIndex())
        self.models.append(model)

    def remove(self, model):
        try:
            self.models.remove(model)
        except ValueError:
            pass

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

    def save(self):
        data = []

        for model in self.models:
            row = { self.fields[0]: model.getIndex(), self.fields[1]: model.getPath() }
            data.append(row)

        self.setData(data = data)
        super().save()

    def newIndex(self):
        if len(self.models) == 0:
            return 1

        lastModel = self.models[len(self.models) - 1]
        lastIndex = int(lastModel.getIndex())
        return str(lastIndex + 1)

    def getModels(self):
        return self.models

    def getName(self):
        return self.name