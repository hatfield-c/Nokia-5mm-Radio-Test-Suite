from core.Model import Model
from core.UIFactory import UIFactory

class Suite(Model):

    ID = "suite"
    
    def __init__(self, path):
        super().__init__(path)

        self.path = path
        self.benches = None
        self.units = None
        self.sequences = None

    def getCollection(self, key):
        if key == "benches":
            return self.benches

        if key == "units":
            return self.units

        if key == "sequences":
            return self.sequences

        return None

    def setCollection(self, key, value):
        value = UIFactory.RelativePath(value)

        if key == "benches":
            self.benches = value

        if key == "units":
            self.units = value

        if key == "sequences":
            self.sequences = value

    def save(self):
        self.data = [
            { "step": "benches", "csv_path": self.benches },
            { "step": "units", "csv_path": self.units },
            { "step": "sequences", "csv_path": self.sequences }
        ]

        super().save()

    def load(self):
        super().load()
        
        for row in self.data:
            if not set(self.fields).issubset(row):
                continue

            if row["step"] == "benches":
                self.benches = row["csv_path"]

            if row["step"] == "units" :
                self.units = row["csv_path"]

            if row["step"] == "sequences":
                self.sequences = row["csv_path"]

    def getPath(self):
        return self.path