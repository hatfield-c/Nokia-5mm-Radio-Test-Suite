from Model import Model
from models.Parameters import Parameters

class ModelFactory:

    types = {
        "model": lambda path : Model(path = path),
        "parameters": lambda path : Parameters(path = path)
    }

    def __init__(self, modelType):
        self.modelType = modelType

    def create(self, path):
        bluePrint = ModelFactory.types[self.modelType]
        return bluePrint(path = path)