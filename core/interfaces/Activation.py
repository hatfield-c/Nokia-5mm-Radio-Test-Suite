import tkinter
import traceback
import time
import os

from Config import _CONFIG_
from core.CSVObject import CSVObject
from core.DataController import DataController

from core.inputs.CollectionDropDown import CollectionDropDown
from core.inputs.activation.SequencePairSelector import SequencePairSelector

from core.Interface import Interface
from core.interfaces.Builder import Builder
from core.interfaces.ResultsWindow import ResultsWindow
from core.interfaces.DUT import DUT

from core.interfaces.alerts.NoSequences import NoSequences
from core.interfaces.alerts.SequenceError import SequenceError
from core.interfaces.alerts.SequenceNotFound import SequenceNotFound
from core.interfaces.alerts.ModuleError import ModuleError
from core.interfaces.alerts.NoModuleError import NoModuleError
from core.interfaces.alerts.ModuleNotFound import ModuleNotFound
from core.interfaces.alerts.MissingCollections import MissingCollections
from core.interfaces.alerts.activation.ConfigError import ConfigError as ActivationConfigError

class Activation(Interface):
    def __init__(self, root, suite):
        super().__init__(root = root, title = "Begin Testing", dimensions = Builder.DEFAULT_DIMENSIONS)
        self.suite = suite
        self.viewResults = tkinter.IntVar()
        self.autosave = tkinter.IntVar()
        self.dut = tkinter.IntVar()
        self.viewResults.set("1")
        self.autosave.set("0")
        self.dut.set("1")
        self.maxLoops = 999

        self.grid_propagate(False)
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        self.container = tkinter.Frame(self)
        self.container.rowconfigure(0, weight = 1)
        self.container.rowconfigure(1, weight = 1)
        self.container.columnconfigure(0, weight = 1)
        self.container.grid(row = 0, stick = "nwse")

        imgPath = _CONFIG_["activate_path"]
        img = tkinter.PhotoImage(file = imgPath)
        self.logo = tkinter.Label(
            self, 
            image = img, 
            background = "black",
            borderwidth = 4,
            relief = "groove"
        )
        self.logo.image = img
        self.logo.grid(row = 0, column = 0, pady = (5, 0), sticky = "n")

        self.buttonRow = tkinter.Frame(
            self.container, 
            pady = 10,
            background ="white", 
            borderwidth = 2, 
            relief = "groove"
        )
        self.buttonRow.grid(row = 1, column = 0, padx = 21, pady = (0, 7), sticky = "ews")

        self.buttonRow.rowconfigure(0, weight = 1)
        self.buttonRow.rowconfigure(1, weight = 1)
        self.buttonRow.columnconfigure(0, weight = 1)
        self.buttonRow.columnconfigure(1, weight = 1)
        self.buttonRow.columnconfigure(2, weight = 1)

        self.configFrame = tkinter.Frame(
            self.buttonRow,
            background = _CONFIG_["blue_primary"],
            borderwidth = 2,
            relief = "groove",
            padx = 5,
            pady =5
        )
        self.configFrame.grid(row = 0, column = 0, columnspan = 4, pady = (0, 5))
        
        self.verboseCheckbox = tkinter.Checkbutton(
            self.configFrame, 
            text = "View Results", 
            variable = self.viewResults,
            borderwidth = 2,
            relief = "groove"
        )
        self.verboseCheckbox.grid(row = 0, column = 0)

        self.overwriteCheckbox = tkinter.Checkbutton(
            self.configFrame, 
            text = "Autosave", 
            variable = self.autosave,
            borderwidth = 2,
            relief = "groove"
        )
        self.overwriteCheckbox.grid(row = 0, column = 1, padx = (10, 10))

        self.dutCheckBox = tkinter.Checkbutton(
            self.configFrame,
            text = "DUT",
            variable = self.dut,
            borderwidth =2,
            relief = "groove"
        )
        self.dutCheckBox.grid(row = 0, column = 2)

        self.loopFrame = tkinter.Frame(self.configFrame, borderwidth = 2, relief = "groove")
        self.loopFrame.grid(row = 0, column = 3, padx = (10, 0))

        self.loopEntry = tkinter.Entry(self.loopFrame, width = 3)
        self.loopEntry.insert(0, "1")
        self.loopEntry.grid(row = 0, column = 0, padx = 5)

        self.loopLabel = tkinter.Label(self.loopFrame, text = "Loop")
        self.loopLabel.grid(row = 0, column = 1, padx = (0, 5))

        self.activateButton = tkinter.Button(
            self.buttonRow, 
            text = "Activate All\nSequences", 
            command = lambda : self.activateSequences(), 
            font = "Helevetica 12 bold",
            background = _CONFIG_["color_secondary"]
        )
        self.activateButton.grid(row = 1, column = 0)

        self.oneSequenceContainer = tkinter.Frame(
            self.buttonRow, 
            background = _CONFIG_["blue_primary"], 
            borderwidth = 2, 
            relief = "groove",
            padx = 5,
            pady = 5
        )
        self.oneSequenceContainer.grid(row = 1, column = 1, padx = 30)

        self.sequenceButton = tkinter.Button(
            self.oneSequenceContainer, 
            text = "Activate Sequence", 
            command = lambda : self.oneSequence(), 
            font = "Helevetica 12 bold",
            background = _CONFIG_["color_secondary"]
        )
        self.sequenceButton.grid(row = 0, column = 0, pady = (0, 10))

        self.sequenceDropDown = CollectionDropDown(
            args = {
                "root": self.oneSequenceContainer,
                "config": {},
                "data": ["sequences", ""],
                "orig": ""
            }     
        )
        self.sequenceDropDown.config(borderwidth = 2, relief = "groove")
        self.sequenceDropDown.grid(row = 1, column = 0)

        self.pairContainer = tkinter.Frame(
            self.buttonRow,
            background = _CONFIG_["blue_primary"],
            borderwidth = 2,
            relief = "groove",
            padx = 5,
            pady = 5
        )
        self.pairContainer.grid(row = 1, column = 2)

        self.pairButton = tkinter.Button(
            self.pairContainer, 
            text = "Activate Pair", 
            command = lambda : self.pair(), 
            font = "Helevetica 12 bold",
            background = _CONFIG_["color_secondary"]
        )
        self.pairButton.grid(row = 0, column = 0, pady = (0, 10))

        self.pairDropDown = SequencePairSelector(self.pairContainer, self.suite)
        self.pairDropDown.config(borderwidth = 2, relief = "groove")
        self.pairDropDown.grid(row = 1, column = 0)

    def activateSequences(self):
        if not self.suite.validCollections():
            alert = MissingCollections()
            alert.pack()
            return

        viewresults = int(self.viewResults.get())
        autosave = int(self.autosave.get())

        if viewresults == 0 and autosave == 0:
            alert = ActivationConfigError()
            alert.pack()
            return
        
        appData = self.suite.compileData()
        sequences = appData["sequences"]

        if sequences is None or not sequences:
            NoSequences()
            return

        loopCount = self.getLoopCount()
        loopIndex = 0

        while loopIndex < loopCount:
            for sequenceIndex in sequences:
                self.activateSequence(appData, sequenceIndex)

            loopIndex += 1

    def oneSequence(self):
        if not self.suite.validCollections():
            alert = MissingCollections()
            alert.pack()
            return

        appData = self.suite.compileData()

        sequences = appData["sequences"]
        sequenceIndex = self.sequenceDropDown.get()

        if sequences is None or not sequences :
            alert = NoSequences()
            alert.pack()
            return

        if sequenceIndex is None or sequenceIndex not in sequences:
            alert = SequenceNotFound(sequenceIndex = sequenceIndex)
            alert.pack()
            return

        loopCount = self.getLoopCount()
        loopIndex = 0

        while loopIndex < loopCount:
            self.activateSequence(appData, sequenceIndex)

            loopIndex += 1

    def pair(self):
        if not self.suite.validCollections():
            alert = MissingCollections()
            alert.pack()
            return

        pairData = self.pairDropDown.get()

        if (
            pairData["sequenceIndex"] is None or 
            pairData["sequenceIndex"] == "" or
            pairData["benchIndex"] is None or 
            pairData["benchIndex"] == "" or
            pairData["unitIndex"] is None or 
            pairData["unitIndex"] == ""
        ):
            NoSequences()
            return

        appData = self.suite.compileData()

        sequenceIndex = pairData["sequenceIndex"]
        benchIndex = pairData["benchIndex"]
        unitIndex = pairData["unitIndex"]

        loopCount = self.getLoopCount()
        loopIndex = 0

        while loopIndex < loopCount:
            self.activateSequencePair(appData, sequenceIndex, benchIndex, unitIndex)

            loopIndex += 1

    def activateSequence(self, appData, sequenceIndex):
        viewresults = int(self.viewResults.get())
        autosave = int(self.autosave.get())

        if viewresults == 0 and autosave == 0:
            alert = ActivationConfigError()
            alert.pack()
            return
        
        sequence = appData["sequences"][sequenceIndex]

        for pair in sequence["data"]:
            try:
                if "bench" not in pair or "unit" not in pair:
                    continue

                if pair["bench"] == "" or pair["unit"] == "":
                    continue

                benchIndex = pair["bench"]
                unitIndex = pair["unit"]
                success = self.activateSequencePair(appData, sequenceIndex, benchIndex, unitIndex)
            except Exception:
                traceback.print_exc()
                error = SequenceError(sequenceIndex = sequenceIndex, sequenceData = pair)
                error.pack()
                continue

    def activateSequencePair(self, appData, sequenceIndex, benchIndex, unitIndex):
        viewresults = int(self.viewResults.get())
        autosave = int(self.autosave.get())
        dut = int(self.dut.get())

        if viewresults == 0 and autosave == 0:
            alert = ActivationConfigError()
            alert.pack()
            return False

        resultData = { "No Data": "No data was returned." }

        sequences = appData["sequences"]
        benches = appData["benches"]
        units = appData["units"]

        sequence = sequences[sequenceIndex]
        bench = benches[benchIndex]
        unit = units[unitIndex]

        moduleList = _CONFIG_["modules"]
        moduleName = self.getModule(unit["data"])

        if moduleName is None:
            alert = NoModuleError(
                sequenceIndex = sequenceIndex + ":" + sequence["pureName"], 
                sequenceData = "(" + bench["index"] + ":" + bench["pureName"] + ",   " + unit["index"] + ":" + unit["pureName"] + ")"
            )
            alert.pack()
            return False

        if moduleName not in moduleList:
            alert = ModuleNotFound(
                moduleName = moduleName, 
                sequenceIndex = sequenceIndex + ":" + sequence["pureName"], 
                sequenceData = "(" + bench["index"] + ":" + bench["pureName"] + ",   " + unit["index"] + ":" + unit["pureName"] + ")"
            )
            alert.pack()
            return False

        startTime = time.time()

        if dut == 1:
            dutWindow = DUT(parent = self)

        try:
            bluePrint = moduleList[moduleName]
            module = bluePrint(parameters = unit["data"], testbench = bench["data"])

            resultData = module.run_test()
        except Exception:
            traceback.print_exc()
            error = ModuleError(
                moduleName = moduleName, 
                sequenceIndex = sequenceIndex + ":" + sequence["pureName"], 
                sequenceData = "(" + bench["index"] + ":" + bench["pureName"] + ",   " + unit["index"] + ":" + unit["pureName"] + ")"
            )
            error.pack()
            return False

        endTime = time.time()
        runtime = endTime - startTime

        if isinstance(resultData, dict):
            resultData = DataController.GetList(data = resultData)
        elif not isinstance(resultData, list):
            resultData = [ resultData ]

        runtimeRow = { "key": "MODULE_RUNTIME", "value": str(runtime) }
        resultData.append(runtimeRow)

        resultPath = None
        if autosave == 1:
            resultPath = self.getResultPath(appData, sequenceIndex, benchIndex, unitIndex)
            
            csvObj = CSVObject(rowsList = resultData, fields = None, path = resultPath)
            DataController.SaveSloppy(fileName = resultPath, csvData = csvObj)

        if viewresults == 1:
            results = ResultsWindow(
                moduleName = moduleName,
                sequenceIndex = sequenceIndex, 
                benchIndex = benchIndex,
                unitIndex = unitIndex,
                compiledData = appData,
                resultPath = resultPath,
                resultData = resultData
            )
            results.pack()

        return True

    def getModule(self, unitData):
        for row in unitData:
            if "key" not in row or "value" not in row:
                return None

            if row["key"] == "module":
                return row["value"]

        return None

    def getResultPath(self, appData, sequenceIndex, benchIndex, unitIndex):
        bench = appData["benches"][benchIndex]
        unit = appData["units"][unitIndex]

        benchName = bench["pureName"]
        unitName = unit["pureName"]

        path = _CONFIG_["result_dir"]
        path += self.suite.modelData.pureName + "/"
        
        fileName = "[Seq-" + str(sequenceIndex) +"][Bench-" + str(benchIndex) + "-" + str(benchName) + "][Unit-" + str(unitIndex) + "-" + str(unitName) + "]"
        fileName += "/data"
        fileIndex = self.getFileIndex(path, fileName)
        fileName += str(fileIndex) + ".csv"
        
        fullPath = path + fileName
        os.makedirs(os.path.dirname(fullPath), exist_ok = True)

        return fullPath

    def getFileIndex(self, path, fileName):
        if not os.path.exists(path + fileName + "0.csv"):
            return 0

        index = 0
        while(os.path.exists(path + fileName + str(index) + ".csv")):
            index += 1

        return index

    def getLoopCount(self):
        loopCount = self.loopEntry.get()

        if loopCount == None or loopCount == "":
            loopCount = 0

        try:
            loopCount = int(loopCount)
        except:
            loopCount = 0

        if loopCount < 1:
            loopCount = 0

        if loopCount > 999:
            loopCount = self.maxLoops

        return loopCount
