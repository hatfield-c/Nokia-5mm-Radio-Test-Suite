from Model import Model
from models.Parameter import Parameter

# Move some functionality from Parameters to the Model class, so that any data gathering performed on parameters can be performed on the model
# Then, edit the Builder class to instantiate its own models based on a model factory, which is set by classes which extend the Builder class
# Specify the SequenceBuilder class to use a generic Model, and the other classes to use a Parameters model, and then the application should be able to
# save/load both indexed and flat data

class Parameters(Model):

    defaultName = "NO_NAME"
    
    def __init__(self, path = ""):
        super().__init__(path)
        self.fieldMap = { 
            "indexField": "key", 
            "valueField": "value" 
        }

        self.clearParameters()

    def loadOld(self):
        super().load()
        
        if self.fieldMap is None or not self.data:
            return

        self.clearParameters()

        if self.fieldMap["indexField"] in self.fields and self.fieldMap["valueField"] in self.fields:
            self.indexed = True
        else:
            self.indexed = False

        for row in self.data:
            self.addParameterFromRow(row)

        if self.getParameter("name") is not None:
            self.name = self.getParameter("name")
        else:
            self.name = self.shortPath


    def saveOld(self):
        data = []

        for key in self.parameters:
            row = {}
            parameter = self.parameters[key]

            if self.indexed:
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

        if key is not None and value is not None:
            self.parameters[key] = Parameter(key = key, value = value, args = args)
        else:
            index = str(len(self.parameters))
            self.parameters[index] = Parameter(key = None, value = None, args = args)

    def addParameterFromRow(self, row):

        value = None
        key = None
        args = {}

        for rowKey in row:

            if (self.fieldMap["indexField"] in row) and (self.fieldMap["valueField"] in row):
                if rowKey == self.fieldMap["valueField"]:
                    value = row[rowKey]
            else:
                args[rowKey] = row[rowKey]

        if value is not None and self.fieldMap["indexField"] in row:
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
        self.indexed = False
        self.name = None

    def useDefaultFields(self):
        fields = []

        for key in self.fieldMap:
            fields.append(self.fieldMap[key])

        self.fields = fields

    def toString(self):
        vals = "<path: " + self.path + " " + self.getPath() + ">\n"

        for paramKey in self.parameters:
            valStr = self.parameters[paramKey].toString()
            vals += valStr + "\n"

        return str(vals)

    def getParameters(self):
        return self.parameters

    def getName(self):
        return self.name

    def getShortPath(self):
        return self.shortPath

    def getFileName(self):
        return self.fileName