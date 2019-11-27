from core.interfaces.Builder import Builder
from core.models.Collection import Collection
from core.models.ModelFactory import ModelFactory
from core.interfaces.EditModel import EditModel
from core.UIFactory import UIFactory
from core.models.Parameters import Parameters
import tkinter

class RunBuilder(Builder):
    def __init__(self, root, csvPath = None):
        builderData = {
            "type": "Run",
            "factory": ModelFactory(modelType = Parameters.ID),
            "controls": [
                "divider",
                "saveAs",
                "divider"
            ]
        }

        super().__init__(title = "Run Builder", root = root, csvPath = csvPath, builderData = builderData)
