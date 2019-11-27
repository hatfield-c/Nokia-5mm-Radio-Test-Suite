from core.Model import Model
from core.models.Parameters import Parameters

class ModelFactory:

    types = {
        Model.Id: lambda path : Model(path = path),
        Parameters.Id: lambda path : Parameters(path = path)
    }

    def __init__(self, modelType):
        self.modelType = modelType

    def create(self, path):
        bluePrint = ModelFactory.types[self.modelType]
        return bluePrint(path = path)