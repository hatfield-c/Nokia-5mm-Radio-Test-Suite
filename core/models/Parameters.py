from core.Model import Model
from core.models.Parameter import Parameter

class Parameters(Model):

    DefaultName = "NO_NAME"
    ID = "parameters"
    
    def __init__(self, path = ""):
        super().__init__(path)
        self.fieldMap = { 
            "indexField": "key", 
            "valueField": "value" 
        }

        self.clearParameters()

    def build(self, data):
        self.clearParameters()

        if data is None or not data:
            return

        fields = []
        for field in data[0]:
            fields.append(field)

        self.fields = fields

        for row in data:
            self.addParameterFromRow(row)

        return self.compileParameters()

    def addParameter(self, key, value, args = {}):
        if key in self.parameters:
            self.setParameter(key = key, value = value, args = args)
            return    

        if key is not None and value is not None:
            self.parameters[key] = Parameter(key = key, value = value, args = args)

    def addParameterFromRow(self, row):

        value = None
        key = None
        args = {}

        for rowKey in row:
            if rowKey == self.fieldMap["indexField"]:
                continue

            if rowKey == self.fieldMap["valueField"]:
                    value = row[rowKey]
            else:
                args[rowKey] = row[rowKey]

        key = row[self.fieldMap["indexField"]]
        
        self.addParameter(key = key, value = value, args = args)

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

    def clearParameters(self):
        self.parameters = { }

    def useDefaultFields(self):
        fields = []

        for key in self.fieldMap:
            fields.append(self.fieldMap[key])

        self.fields = fields

    def compileParameters(self):
        data = { "args": { } }

        for paramKey in self.parameters:
            parameter = self.parameters[paramKey]
            
            data[parameter.getKey()] = parameter.getValue()

            if len(parameter.getArgs()) > 0:
                data["args"][parameter.getKey()] = parameter.getArgs()

        return data

    def saveParameters(self):
        fields = [ "key", "value" ]
        data = []

        for paramKey in self.parameters:
            row = {}
            parameter = self.parameters[paramKey]

            row["key"] = parameter.getKey()
            row["value"] = parameter.getValue()

            args = parameter.getArgs()

            if len(args) > 0:
                for argKey in args:
                    arg = args[argKey]

                    row[argKey] = arg

                    if argKey not in fields:
                        fields.append(argKey)
            
            data.append(row)

        self.fields = fields
        self.data = data
        self.save()

    def toString(self):
        vals = "<path: " + self.path + " " + self.getPath() + ">\n"

        for paramKey in self.parameters:
            valStr = self.parameters[paramKey].toString()
            vals += valStr + "\n"

        return str(vals)

    def getParameters(self):
        return self.parameters

    def getShortPath(self):
        return self.shortPath

    def getFileName(self):
        return self.fileName