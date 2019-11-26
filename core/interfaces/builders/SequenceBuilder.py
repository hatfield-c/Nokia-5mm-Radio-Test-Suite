from interfaces.Builder import Builder
from models.Collection import Collection
from models.ModelFactory import ModelFactory
from interfaces.EditModel import EditModel
from UIFactory import UIFactory
from models.Parameters import Parameters
import tkinter

class SequenceBuilder(Builder):
    def __init__(self, root, csvPath = None):
        builderData = {
            "type": "Sequence",
            "factory": ModelFactory(modelType = "model"),
            "controls": [
                "saveAs",
                "divider",
                "newPoint"
            ]
        }

        super().__init__(title = "Sequence Builder", root = root, csvPath = csvPath, builderData = builderData)
