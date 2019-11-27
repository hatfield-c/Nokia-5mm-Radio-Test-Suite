from core.interfaces.Builder import Builder
from core.models.Collection import Collection
from core.models.ModelFactory import ModelFactory
from core.interfaces.EditModel import EditModel
from core.UIFactory import UIFactory
from core.Model import Model
import tkinter

class SequenceBuilder(Builder):

    FIELDS = [
        "key",
        "value"
    ]

    def __init__(self, root, csvPath = None):
        builderData = {
            "type": "Sequence",
            "factory": ModelFactory(
                args = {
                    "type": Model.ID, 
                    "fields": self.FIELDS
                }
            ),
            "controls": [
                "divider",
                "saveAs",
                "divider"
            ]
        }

        super().__init__(title = "Sequence Builder", root = root, csvPath = csvPath, builderData = builderData)
