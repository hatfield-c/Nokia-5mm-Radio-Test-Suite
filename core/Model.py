from core.DataController import DataController
from core.CSVObject import CSVObject

class Model:

    Id = "model"

    def __init__(self, path):
        self.setPath(path)
        self.fields = None
        self.data = []
        self.index = None

    def build(self, data):
        return data

    def getFields(self):
        return self.fields

    def getData(self):
        return self.data

    def getPath(self):
        return self.path

    def getIndex(self):
        return self.index

    def setIndex(self, index):
        self.index = index

    def setPath(self, path):
        self.path = path

        if self.path is not None:
            pathSplit = self.path.split("/")
            self.fileName = pathSplit[len(pathSplit) - 1]

            pathLen = len(self.path)
            if pathLen >= 32:
                self.shortPath = self.path[pathLen - 32:pathLen]
            else:
                self.shortPath = self.path
        else:
            self.fileName = None
            self.shortPath = None

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
