from Model import Model

class Suite(Model):
    
    def __init__(self, path):
        super().__init__(path)

        self.path = path
        self.benches = None
        self.runs = None
        self.sequences = None

    def save(self):
        self.data = [
            { "step": "benches", "csv_path": self.benches },
            { "step": "runs", "csv_path": self.runs },
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

            if row["step"] == "runs" :
                self.runs = row["csv_path"]

            if row["step"] == "sequences":
                self.sequences = row["csv_path"]

    def getPath(self):
        return self.path