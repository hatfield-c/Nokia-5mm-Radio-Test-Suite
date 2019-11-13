from DataController import DataController
from CSVObject import CSVObject

class Model:

    def __init__(self, path):
        self.path = path
        self.fields = None
        self.data = []

    def getFields(self):
        return self.fields

    def getData(self):
        return self.data

    def getPath(self):
        return self.path

    def setPath(self, path):
        self.path = path

    def setData(self, fields = None, data = None):
        if fields is None:
            fields = self.fields
        
        if data is None:
            return
        
        self.fields = fields
        self.data = data

    def add(self, row):
        if not isinstance(row, dict):
            return

        for field in self.fields:
            if field not in row:
                return 

        self.data.append(row)

    def remove(self, row):
        if not isinstance(row, dict):
            return

        try:
            while True:
                self.data.remove(row)
        except ValueError:
            pass

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
