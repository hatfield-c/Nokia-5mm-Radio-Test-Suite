from interfaces.Builder import Builder
from models.Collection import Collection
from models.ModelFactory import ModelFactory
from interfaces.EditModel import EditModel
from UIFactory import UIFactory
from models.Parameters import Parameters
import tkinter

class RunBuilder(Builder):
    def __init__(self, root, csvPath = None):
        builderData = {
            "type": "Run",
            "factory": ModelFactory(modelType = Parameters.Id),
            "controls": [
                "divider",
                "saveAs",
                "divider"
            ]
        }

        super().__init__(title = "Run Builder", root = root, csvPath = csvPath, builderData = builderData)
