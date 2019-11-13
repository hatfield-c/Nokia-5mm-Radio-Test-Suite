from Model import Model
from models.Parameter import Parameter

class Parameters(Model):
    
    def __init__(self, path = ""):
        super().__init__(path)
        self.fieldMap = { 
            "indexField": "key", 
            "valueField": "value" 
        }

        self.clearParameters()

    def load(self):
        super().load()

        if self.fieldMap is None or not self.data:
            return

        if "indexField" not in self.fieldMap or "valueField" not in self.fieldMap:
            return

        if self.fieldMap["indexField"] not in self.data[0] or self.fieldMap["valueField"] not in self.data[0]:
            return

        self.clearParameters()

        for row in self.data:
            self.addParameterFromRow(row)

    def save(self):
        data = []
        
        for key in self.parameters:
            row = {}
            parameter = self.parameters[key]

            row[self.fieldMap["indexField"]] = key
            row[self.fieldMap["valueField"]] = parameter.getValue()

            args = parameter.getArgs()
            for argKey in args:
                row[argKey] = args[argKey]

            data.append(row)

        self.data = data
        super().save()

    def buildParameters(self, rowData):
        self.clearParameters()

        if rowData is None or not rowData:
            return

        fields = []
        for field in rowData[0]:
            fields.append(field)

        self.fields = fields

        for row in rowData:
            self.addParameterFromRow(row)

    def addParameter(self, key, value, args = {}):
        if key in self.parameters:
            self.setParameter(key = key, value = value, args = args)
            return    

        self.parameters[key] = Parameter(key = key, value = value, args = args)

    def addParameterFromRow(self, row):
        if self.fieldMap["indexField"] not in row:
            return

        value = None
        args = {}

        for rowKey in row:
            if rowKey == self.fieldMap["indexField"]:
                continue

            if rowKey == self.fieldMap["valueField"]:
                value = row[rowKey]
            else:
                args[rowKey] = row[rowKey]

        self.addParameter(key = row[self.fieldMap["indexField"]], value = value, args = args)

    def setParameter(self, key, value, args = {}):
        if key not in self.parameters:
            return None
        
        parameter = self.parameters[key]
        parameter.setValue(value)

        if args:
            parameter.setArgs(args)

    def setParameters(self, parameters):
        self.parameters = parameters

    def getParameter(self, key):

        if key not in self.parameters:
            return None
        
        parameter = self.parameters[key]
        return parameter.getValue()

    def getParameters(self):
        return self.parameters

    def clearParameters(self):
        self.parameters = { "name": Parameter(key = "name", value = "", args = {}) }

    def useDefaultFields(self):
        fields = []

        for key in self.fieldMap:
            fields.append(self.fieldMap[key])

        self.fields = fields