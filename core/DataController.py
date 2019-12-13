import csv
import core.CSVObject
import Config

class DataController:

    @staticmethod
    def Load(fileName, loadChildData = False):
        fileName = DataController.FullPath(path = fileName)

        with open(fileName) as csvFile:
            itemList = []
            fileReader = csv.reader(csvFile)
            
            keys = next(fileReader)

            for line in fileReader:
                item = {}
                for value, key in zip(line, keys):
                    item[key] = str(value).strip()
                    if(key == Config._CONFIG_["csv_path_key"] and loadChildData):
                        item[Config._CONFIG_["csv_child_data_key"]] = DataController.Load(item[key], loadChildData)

                itemList.append(item)

            if Config._CONFIG_["csv_path_key"] in keys and loadChildData:
                keys.append(Config._CONFIG_["csv_child_data_key"])

            csvData = core.CSVObject.CSVObject(itemList, keys, path = fileName)
            return csvData

    @staticmethod
    def Save(fileName, csvData):
        fileName = DataController.FullPath(path = fileName)

        with open(fileName, "w", newline=Config._CONFIG_["csv_newline"]) as csvFile:
            fileWriter = csv.writer(csvFile)

            fields = csvData.getFields()
            fileWriter.writerow(fields)

            for row in csvData.getAll():
                rowData = []
                for field in fields:
                    rowData.append(str(row[field]).strip())

                fileWriter.writerow(rowData)

    @staticmethod
    def SaveSloppy(fileName, csvData):
        fileName = DataController.FullPath(path = fileName)
        rowData = csvData.getAll()

        if not isinstance(rowData, list):
            rowData = DataController.GetList(rowData)

        with open(fileName, "w", newline=Config._CONFIG_["csv_newline"]) as csvFile:
            fileWriter = csv.writer(csvFile)

            for row in csvData.getAll():
                rowData = []

                if isinstance(row, dict):
                    for rowKey in row:
                        rowData.append(str(row[rowKey]).strip())
                elif isinstance(row, list):
                    for item in row:
                        rowData.append(str(item).strip())
                else:
                    rowData.append(str(row).strip())

                fileWriter.writerow(rowData)

    @staticmethod
    def FullPath(path = None):
        if path is None:
            return Config._CONFIG_["working_dir"] + "/"

        if ":/" in path:
            return path

        
        return Config._CONFIG_["working_dir"] + "/" + path

    #
    #   Takes a list of dictionaries, such as what is returned by the DataController.Load() method,
    #   and attempts to create a new dictionary by treating each list-element as a row of data. 
    #   The keys of each list-element dictionary (row) are searched to see if they match the given 
    #   keyIndex and the given valueIndex. This data is then used as the key-value pairings of the new 
    #   dictionary which is returned.
    #
    #   Returns an empty dictionary if no matching key/values were found, or if an error occurs.
    #
    @staticmethod
    def GetDictionary(data, keyIndex = "key", valueIndex = "value"):
        indexed = { }

        try:
            for row in data:
                if keyIndex not in row or valueIndex not in row:
                    continue

                indexed[row[keyIndex]] = row[valueIndex]
        except:
            pass

        return indexed

    #
    #   Takes a dictionary, and returns a list of dictionaries where each list-element dictionary uses the given keyIndex
    #   to point to the key of the original dictionary, and the valueIndex to point to the value of the original
    #   dictionary. Essentially the opposite of the DataController.GetDictionary() method.
    #
    @staticmethod
    def GetList(data, keyIndex = "key", valueIndex = "value"):
        data = []

        try:
            for key in data:
                row = { keyIndex: key, valueIndex: data[key] }
                data.append(row)
        except:
            pass

        return data