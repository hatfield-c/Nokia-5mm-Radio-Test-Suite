from core.Model import Model
from core.models.Parameters import Parameters
from core.models.Suite import Suite

class ModelFactory:

    types = {
        Model.ID: Model,
        Parameters.ID: Parameters,
        Suite.ID : Suite
    }

    def __init__(self, args):
        self.modelType = args["type"]
        self.fields = args["fields"]

        if "default" in args:
            self.defaultEntries = args["default"]
        else:
            empty = {}

            for field in self.fields:
                empty[field] = ""

            self.defaultEntries = [ empty ]

    def create(self, path):
        bluePrint = ModelFactory.types[self.modelType]
        model = bluePrint(path = path)
        
        model.setFields(self.fields)

        if self.defaultEntries is not None:
            model.setData(data = self.defaultEntries)

        return model