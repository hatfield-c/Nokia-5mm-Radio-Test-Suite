from core.interfaces.Builder import Builder
from core.models.Collection import Collection
from core.models.ModelFactory import ModelFactory
from core.interfaces.EditModel import EditModel
from core.UIFactory import UIFactory
from core.models.Parameters import Parameters
import tkinter

class BenchBuilder(Builder):
    def __init__(self, root, csvPath = None):
        builderData = {
            "type": "Bench",
            "factory": ModelFactory(modelType = Parameters.Id),
            "controls": [
                "divider",
                "saveAs",
                "divider"
            ]
        }

        super().__init__(title = "Bench Builder", root = root, csvPath = csvPath, builderData = builderData)
