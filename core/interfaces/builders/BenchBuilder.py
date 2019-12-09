from Config import _CONFIG_
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
            "mutable": False,
            "default_dir": _CONFIG_["bench_dir"],
            "factory": ModelFactory(
                args = {
                    "type": Parameters.ID, 
                    "fields": self.FIELDS,
                    "default": [
                        { "key": "<label|DEFAULT_TEXT>", "value": "" }
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
                    "addRadio",
                    "addKey",
                    "newEmpty",
                ],
                "render": []
            }
        }

        super().__init__(title = "Bench Builder", root = root, csvPath = csvPath, builderData = builderData)
