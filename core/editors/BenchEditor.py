from Editor import Editor
from models.Collection import Collection
from interfaces.EditParameters import EditParameters
from UIFactory import UIFactory
from models.Parameters import Parameters
import tkinter

class BenchEditor(Editor):
    def __init__(self, root, csvPath = None, color = None):
        self.editorData = {
            "type": "Bench",
            "controls": {
                "_DIVIDER_": {
                    "title": "_DIVIDER_",
                    "action": lambda model : self.nothing()
                },
                "saveBenchAs": {
                    "title": "Save As",
                    "action": lambda model : self.saveBenchAs()
                },
                "newPoint": {
                    "title": "New Point",
                    "action": lambda model : self.newPoint()
                }
            }
        }

        super().__init__(title = "Bench Editor", root = root, csvPath = csvPath, editorData = self.editorData)

    def loadBench(self):
        pass

    def editBench(self, model):
        editCsv = EditParameters(model = model)
        editCsv.pack()

    def removeBench(self):
        pass

    def saveBenchAs(self):
        pass

    def newPoint(self):
        pass
