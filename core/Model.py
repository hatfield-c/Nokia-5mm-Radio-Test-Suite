from DataController import DataController
from CSVObject import CSVObject

class Model:

    def __init__(self, path):
        self.path = path
        self.data = []

        try:
            if self.fields is None:
                self.fields = []
        except AttributeError:
            self.fields = []

    def getFields(self):
        return self.fields

    def getData(self):
        return self.data

    def getPath(self):
        return self.path

    def setData(self, fields, data):
        self.fields = fields
        self.data = data

    def add(self, row):
        if not isinstance(row, dict):
            return

        for field in self.fields:
            if field not in row:
                return 

        self.data.append(row)

    def load(self):
        if self.path is None:
            return

        csvData = DataController.Load(self.path)
        self.fields = csvData.getFields()
        self.data = csvData.getAll()

    def save(self):
        if self.path is None:
            return
        
        csvData = CSVObject(self.data, self.fields, self.path)
        DataController.Save(self.path, csvData)
