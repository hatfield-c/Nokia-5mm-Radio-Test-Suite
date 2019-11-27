from core.Model import Model
from core.models.Parameters import Parameters

class ModelFactory:

    types = {
        Model.ID: Model,
        Parameters.ID: Parameters
    }

    def __init__(self, modelType):
        self.modelType = modelType

    def create(self, path):
        bluePrint = ModelFactory.types[self.modelType]
        return bluePrint(path = path)