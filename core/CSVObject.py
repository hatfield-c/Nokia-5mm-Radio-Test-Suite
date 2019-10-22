import copy

class CSVObject:
    
    def __init__(self, rowsList, fields):
        self.rows = rowsList
        self.fields = fields

    def __str__(self):
        resultStr = ""
        resultStr += "CSVObject:" + str(id(self)) + "{\n"
        resultStr += "    Fields: " + str(self.fields) + "\n"
        for row in self.rows:
            resultStr += "    " + str(row) + "\n"

        resultStr += "}"

        return resultStr

    def getFields(self):
        return self.fields    

    def dropField(self, field):
        if field not in self.fields:
            return None

        newFields = copy.deepcopy(self.fields)
        newFields.remove(field)

        newRows = copy.deepcopy(self.rows)

        for row in newRows:
            row.pop(field, None)

        return CSVObject(newRows, newFields)
        
    def getRow(self, rowId):
        return self.rows[rowId]

    def getAll(self, noChildren = False):
        if noChildren:
            childlessCsv = self.dropField('child_data')
            return childlessCsv.getAll()
        else:
            return self.rows

    def pop(self, rowId):
        return self.rows.pop(rowId)

    def setRow(self, rowId, row):
        self.rows[rowId] = row

    def setField(self, rowId, field, value):
        self.rows[rowId][field] = value

    def setAllFields(self, field, value):
        for row in self.rows:
            row[field] = value

