import csv
from CSVObject import CSVObject

class DataController:

    @staticmethod
    def Load(fileName, loadChildData = False):
        with open("core/" + fileName) as csvFile:
            itemList = []
            fileReader = csv.reader(csvFile)
            
            keys = next(fileReader)
            fileKey = 0

            for line in fileReader:
                item = {}
                for value, key in zip(line, keys):
                    item[key] = value
                    if(key == "csv_path" and loadChildData):
                        item["child_data"] = DataController.Load(item[key], loadChildData)

                itemList.append(item)

            if "csv_path" in keys:
                keys.append("child_data")

            csvData = CSVObject(itemList, keys)
            return csvData

    @staticmethod
    def Save(fileName, csvData):
        with open("core/" + fileName, "w", newline="") as csvFile:
            fileWriter = csv.writer(csvFile)

            fields = csvData.getFields()
            fileWriter.writerow(fields)

            for row in csvData.getAll():
                rowData = []
                for field in fields:
                    rowData.append(row[field])

                fileWriter.writerow(rowData)




                
csv_data = DataController.Load("test.csv", True)
print(csv_data)

csv_write = CSVObject([{"res1": 0.501, "res2": "success"}, {"res1": -1, "res2": "failure"}], ["res1", "res2"])
DataController.Save("results.csv", csv_write)

results_data = DataController.Load("results.csv")
print(results_data)

print(csv_data.dropField('child_data'))