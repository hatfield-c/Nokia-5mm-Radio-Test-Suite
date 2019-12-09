from Config import _CONFIG_
from core.interfaces.Builder import Builder
from core.models.Collection import Collection
from core.models.ModelFactory import ModelFactory
from core.interfaces.EditModel import EditModel
from core.UIFactory import UIFactory
from core.Model import Model
import tkinter

class SequenceBuilder(Builder):

    FIELDS = [
        "bench",
        "run"
    ]

    def __init__(self, root, csvPath = None):
        builderData = {
            "type": "Sequence",
            "mutable": True,
            "default_dir": _CONFIG_["sequence_dir"],
            "factory": ModelFactory(
                args = {
                    "type": Model.ID, 
                    "fields": self.FIELDS,
                    "default": [
                        { "bench": "<sequence_select|bench|NONE>", "run": "<sequence_select|run|NONE>" }
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
                    "newEmpty",
                    "addSequenceSelector"
                ],
                "render": [
                    "save",
                    "saveAs",
                    "divider",
                    "newSequencePair"
                ]
            }
        }

        super().__init__(title = "Sequence Builder", root = root, csvPath = csvPath, builderData = builderData)
