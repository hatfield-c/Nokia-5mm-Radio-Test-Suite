import tkinter
import os

from Config import _CONFIG_

from core.CSVObject import CSVObject
from core.DataController import DataController
from core.Interface import Interface
from core.UIFactory import UIFactory

from core.templates.Divider import Divider
from core.models.Parameter import Parameter
from core.models.Parameters import Parameters

class ResultsWindow(Interface):
    def __init__(
        self,
        moduleName,
        sequenceIndex,
        benchIndex,
        unitIndex,
        compiledData,
        resultPath,
        resultData
    ):
        self.data = compiledData
        self.autoPath = self.getResultPath(sequenceIndex, benchIndex, unitIndex)

        sequence = compiledData["sequences"][sequenceIndex]
        bench = compiledData["benches"][benchIndex]
        unit = compiledData["units"][unitIndex]

        sequenceName = sequence["fileName"]
        benchName = bench["fileName"]
        unitName = unit["fileName"]

        title = (
            str(moduleName) + ": " + 
            "[Seq-" + str(sequenceIndex) +"]" +
            "[Bench-" + str(benchIndex) + "-" + str(benchName) + "]" + 
            "[Unit-" + str(unitIndex) + "-" + str(unitName) + "]"
        )
        super().__init__(title = title, dimensions = { "height": 750, "width": 650 })
        self.columnconfigure(0, weight = 1)

        self.titleLabel = tkinter.Label(
            self, 
            text = "TEST UNIT COMPLETE", 
            font = "Helevetica 14 bold underline"
        )
        self.titleLabel.grid(row = 0, column = 0, pady = (20), sticky = "ew")

        scrollWidth = self.dimensions["width"] - 50
        scrollHeight = self.dimensions["height"] - 200

        self.borderContainer = tkinter.Frame(
            self,
            background = "white",
            borderwidth = 2,
            relief = "groove"
        )
        self.borderContainer.grid(row = 1, column = 0)

        self.scrollContainer = tkinter.Frame(self.borderContainer)
        self.scrollContainer.grid(row = 1, column = 0)

        self.scrollFrame = tkinter.Canvas(
            self.scrollContainer, 
            width = scrollWidth, 
            height = scrollHeight,
            background = "white"
        )
        self.scrollFrame.grid_propagate(False)
        self.scrollFrame.grid(row = 0, column = 0, sticky = "news")
        self.container = tkinter.Frame(self.scrollContainer, background = "white")
        
        self.scrollbar = tkinter.Scrollbar(self.scrollContainer, orient = "vertical", command = self.scrollFrame.yview)
        self.scrollbar.grid(row = 0, column = 1, sticky = "ns")
        self.scrollFrame.configure(yscrollcommand = self.scrollbar.set)

        self.horizScrollbar = tkinter.Scrollbar(self.scrollContainer, orient = "horizontal", command = self.scrollFrame.xview)
        self.horizScrollbar.grid(row = 1, column = 0, sticky = "ew")
        self.scrollFrame.configure(xscrollcommand = self.horizScrollbar.set)

        self.resultsFrame = tkinter.Frame(self.container, background = "white")
        self.resultsFrame.grid(row = 0, column = 0, sticky = "ew")

        UIFactory.ScrollBinding(container = self.scrollContainer, scrollableCanvas = self.scrollFrame, child = self.resultsFrame)
        
        self.unitFrame = self.buildUnitFrame(moduleName, sequenceIndex, benchIndex, unitIndex, resultPath)
        self.unitFrame.grid(row = 0, column = 0, sticky = "ew")

        self.divider = Divider(self.resultsFrame, girth = 1, width = scrollWidth)
        self.divider.config(padx = 5)
        self.divider.grid(row = 1, column = 0, sticky = "ew", pady = 10)

        self.resultFrame = self.buildResultFrame(resultData)
        self.resultFrame.grid(row = 2, column = 0, sticky = "ew")

        self.scrollFrame.create_window((0, 0), window = self.container, anchor = "nw")

        self.buttonFrame = self.buildButtonFrame(sequenceIndex, benchIndex, unitIndex, resultData)
        self.buttonFrame.grid(row = 2, column = 0, sticky = "ew", pady = 20)

    def buildUnitFrame(self, moduleName, sequenceIndex, benchIndex, unitIndex, resultPath):
        unitFrame = tkinter.Frame(self.resultsFrame, background = "white")

        unitData = {
            "Module:": moduleName,
            "Suite:": self.data["suite"]["fileName"],
            "Sequence:": sequenceIndex + ":" + self.data["sequences"][sequenceIndex]["fileName"],
            "Bench:": str(benchIndex) + ":" + self.data["benches"][benchIndex]["fileName"],
            "Unit:": str(unitIndex) + ":" + self.data["units"][unitIndex]["fileName"]
        }

        i = 0
        for unitKey in unitData:
            unit = unitData[unitKey]

            keyLabel = tkinter.Label(unitFrame, text = unitKey, font = "Helevetica 12 bold", padx = 10, background = "white")
            keyLabel.grid(row = i, column = 0, sticky = "w")

            valueLabel = tkinter.Label(unitFrame, text = str(unit), font = "Helevetica 12", background = "white")
            valueLabel.grid(row = i, column = 1, padx = (20, 0), sticky = "w")

            i += 1

        if resultPath is not None:

            keyLabel = tkinter.Label(unitFrame, text = "Saved To:", font = "Helevetica 12 bold", padx = 10, background = "white")
            keyLabel.grid(row = i, column = 0, sticky = "w")

            valueLabel = tkinter.Label(unitFrame, text = str(resultPath), font = "Helevetica 12", background = "white")
            valueLabel.grid(row = i, column = 1, padx = (5, 0), sticky = "w")
            i += 1


        resultLabel = tkinter.Label(unitFrame, text = "Results:", font = "Helevetica 12 bold", padx = 10, background = "white")
        resultLabel.grid(row = i, column = 0, sticky = "w", pady = (20, 0))

        return unitFrame

    def buildResultFrame(self, resultData):
        resultFrame = tkinter.Frame(self.resultsFrame, padx = 30, background = "white")

        i = 0
        for row in resultData:
            if isinstance(row, dict):
                entries = list(row.values())
            elif isinstance(row, list):
                entries = row
            else:
                entries = [ row ]

            k = 0
            for entry in entries:
                entryLabel = tkinter.Label(
                    resultFrame, 
                    text = str(entry),
                    font = "Helevatica 10",
                    padx = 3,
                    background = "white"
                )
                entryLabel.grid(row = i, column = k, sticky = "w")
                k += 1

            i += 1

        return resultFrame

    def buildButtonFrame(self, sequenceIndex, benchIndex, unitIndex, resultData):
        buttonFrame = tkinter.Frame(self)
        buttonFrame.columnconfigure(0, weight = 1)
        buttonFrame.columnconfigure(1, weight = 1)

        self.saveButton = tkinter.Button(
            buttonFrame, 
            text = "Save", 
            command = lambda s = sequenceIndex, b = benchIndex, r = unitIndex, d = resultData : self.save(s, b, r, d), 
            font = "Helevetica 14 bold",
            background = _CONFIG_["color_primary"],
            padx = 5
        )
        self.saveButton.grid(row = 0, column = 0, padx = (0, 10))

        self.saveAsButton = tkinter.Button(
            buttonFrame, 
            text = "Save As", 
            command = lambda s = sequenceIndex, b = benchIndex, r = unitIndex, d = resultData : self.saveAs(s, b, r, d), 
            font = "Helevetica 14 bold",
            background = _CONFIG_["color_primary"],
            padx = 5
        )
        self.saveAsButton.grid(row = 0, column = 1)

        return buttonFrame

    def save(self, sequenceIndex, benchIndex, unitIndex, resultData):
        os.makedirs(os.path.dirname(self.autoPath), exist_ok = True)

        csvObj = CSVObject(rowsList = resultData, fields = None, path = self.autoPath)
        DataController.SaveSloppy(fileName = self.autoPath, csvData = csvObj)

    def saveAs(self, sequenceIndex, benchIndex, unitIndex, resultData):
        fileName = tkinter.filedialog.asksaveasfilename(
            initialdir = _CONFIG_["result_dir"], 
            title = "Save Collection As", 
            filetypes = [("csv files", "*.csv")]
        )

        if fileName is None or fileName == "":
            return

        fileName = UIFactory.AddFileExtension(path = fileName, ext = ".csv")

        os.makedirs(os.path.dirname(fileName), exist_ok = True)

        csvObj = CSVObject(rowsList = resultData, fields = None, path = fileName)
        DataController.SaveSloppy(fileName = fileName, csvData = csvObj)

    def getResultPath(self, sequenceIndex, benchIndex, unitIndex):
        benchName = self.data["benches"][benchIndex]["pureName"]
        unitName = self.data["units"][unitIndex]["pureName"]

        path = _CONFIG_["result_dir"]
        path += self.data["suite"]["pureName"] + "/"
        
        fileName = "[Seq-" + str(sequenceIndex) +"][Bench-" + str(benchIndex) + "-" + str(benchName) + "][Unit-" + str(unitIndex) + "-" + str(unitName) + "]"
        fileName += "/data"
        fileIndex = self.getFileIndex(path, fileName)
        fileName += str(fileIndex) + ".csv"
        
        fullPath = path + fileName

        return fullPath

    def getFileIndex(self, path, fileName):
        if not os.path.exists(path + fileName + "0.csv"):
            return 0

        index = 0
        while(os.path.exists(path + fileName + str(index) + ".csv")):
            index += 1

        return index