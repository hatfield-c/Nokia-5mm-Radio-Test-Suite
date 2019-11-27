from core.interfaces.Builder import Builder
from core.models.Collection import Collection
from core.models.ModelFactory import ModelFactory
from core.interfaces.EditModel import EditModel
from core.UIFactory import UIFactory
from core.models.Parameters import Parameters
import tkinter

class BenchBuilder(Builder):

    FIELDS = [
        "key",
        "value"
    ]

    def __init__(self, root, csvPath = None):
        builderData = {
            "type": "Bench",
            "factory": ModelFactory(
                args = {
                    "type": Parameters.ID, 
                    "fields": self.FIELDS
                }
            ),
            "controls": [
                "divider",
                "saveAs",
                "divider"
            ]
        }

        super().__init__(title = "Bench Builder", root = root, csvPath = csvPath, builderData = builderData)
