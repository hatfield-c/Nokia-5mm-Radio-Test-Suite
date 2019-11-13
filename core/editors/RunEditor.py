from Editor import Editor
from models.Collection import Collection
from interfaces.EditParameters import EditParameters
from UIFactory import UIFactory
from models.Parameters import Parameters
import tkinter

class RunEditor(Editor):
    def __init__(self, root, csvPath = None, color = None):
        editorData = {
            "type": "Run",
            "controls": [
                "saveAs",
                "divider",
                "newPoint"
            ]
        }

        super().__init__(title = "Run Editor", root = root, csvPath = csvPath, editorData = editorData)
