from Config import _CONFIG_
from core.interfaces.Builder import Builder
from core.models.Collection import Collection
from core.models.ModelFactory import ModelFactory
from core.interfaces.EditModel import EditModel
from core.UIFactory import UIFactory
from core.models.Parameters import Parameters
import tkinter

class RunBuilder(Builder):

    FIELDS = [
        "key",
        "value"
    ]

    def __init__(self, root, csvPath = None):
        builderData = {
            "type": "Run",
            "mutable": False,
            "default_dir": _CONFIG_["run_dir"],
            "factory": ModelFactory(
                args = {
                    "type": Parameters.ID, 
                    "fields": self.FIELDS,
                    "default": [
                        { "key": "<label|module>", "value": "DumpInput" }
                    ]
                }
            ),
            "controls": {
                "edit": [
                    "save",
                    "saveAs",
                    "load",
                    "newFile",
                    "divider",
                    "addAllocationFile",
                    "addCorrectionFile",
                    "addMobue",
                    "addAbCategory",
                    "addCarrier",
                    "addRadio",
                    "addKey",
                    "newEmpty"
                ],
                "render": []
            }
        }

        super().__init__(title = "Run Builder", root = root, csvPath = csvPath, builderData = builderData)
