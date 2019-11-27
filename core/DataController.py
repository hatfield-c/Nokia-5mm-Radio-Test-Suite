import csv
from core.CSVObject import CSVObject
from Config import _CONFIG_

class DataController:

    @staticmethod
    def Load(fileName, loadChildData = False):
        fileName = DataController.FullPath(path = fileName)

        with open(fileName) as csvFile:
            itemList = []
            fileReader = csv.reader(csvFile)
            
            keys = next(fileReader)
            fileKey = 0

            for line in fileReader:
                item = {}
                for value, key in zip(line, keys):
                    item[key] = value
                    if(key == _CONFIG_["csv_path_key"] and loadChildData):
                        item[_CONFIG_["csv_child_data_key"]] = DataController.Load(item[key], loadChildData)

                itemList.append(item)

            if _CONFIG_["csv_path_key"] in keys and loadChildData:
                keys.append(_CONFIG_["csv_child_data_key"])

            csvData = CSVObject(itemList, keys, path = fileName)
            return csvData

    @staticmethod
    def Save(fileName, csvData):
        fileName = DataController.FullPath(path = fileName)

        with open(fileName, "w", newline=_CONFIG_["csv_newline"]) as csvFile:
            fileWriter = csv.writer(csvFile)

            fields = csvData.getFields()
            fileWriter.writerow(fields)

            for row in csvData.getAll():
                rowData = []
                for field in fields:
                    rowData.append(row[field])

                fileWriter.writerow(rowData)

    @staticmethod
    def FullPath(path = None):
        if path is None:
            return _CONFIG_["working_dir"] + "/"

        if ":/" in path:
            return path

        
        return _CONFIG_["working_dir"] + "/" + path
