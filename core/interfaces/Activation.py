import tkinter
import traceback
import time
import os

from Config import _CONFIG_
from core.inputs.CollectionDropDown import CollectionDropDown
from core.inputs.activation.SequencePairSelector import SequencePairSelector

from core.Interface import Interface
from core.interfaces.Builder import Builder
from core.interfaces.ResultsWindow import ResultsWindow
from core.models.Parameters import Parameters
from core.models.Parameter import Parameter

from core.interfaces.alerts.NoSequences import NoSequences
from core.interfaces.alerts.SequenceError import SequenceError
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
        self.viewResults.set("1")
        self.autosave.set("0")

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
        self.configFrame.grid(row = 0, column = 1, pady = (0, 5))
        
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
        self.overwriteCheckbox.grid(row = 0, column = 1, padx = (10, 0))

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

        benches = appData["benches"]
        runs = appData["runs"]
        sequences = appData["sequences"]

        if sequences is None or not sequences:
            NoSequences()
            return

        for sequenceIndex in sequences:
            sequence = sequences[sequenceIndex]
            self.activateSequence(sequenceIndex, sequence, benches, runs)

    def oneSequence(self):
        if not self.suite.validCollections():
            alert = MissingCollections()
            alert.pack()
            return

        appData = self.suite.compileData()

        benches = appData["benches"]
        runs = appData["runs"]
        sequences = appData["sequences"]

        if sequences is None or not sequences:
            NoSequences()
            return

        sequenceIndex = self.sequenceDropDown.get()
        sequence = sequences[sequenceIndex]

        self.activateSequence(sequenceIndex, sequence, benches, runs)

    def pair(self):
        if not self.suite.validCollections():
            alert = MissingCollections()
            alert.pack()
            return

        appData = self.suite.compileData()

        benches = appData["benches"]
        runs = appData["runs"]

        pairData = self.pairDropDown.get()

        if (
            pairData["sequenceIndex"] is None or 
            pairData["sequenceIndex"] == "" or
            pairData["benchIndex"] is None or 
            pairData["benchIndex"] == "" or
            pairData["runIndex"] is None or 
            pairData["runIndex"] == ""
        ):
            NoSequences()
            return

        sequenceIndex = pairData["sequenceIndex"]
        pair = { "bench": pairData["benchIndex"], "run": pairData["runIndex"] }

        self.activateSequencePair(sequenceIndex, pair, benches, runs)

    def activateSequence(self, sequenceIndex, sequence, benches, runs):
        viewresults = int(self.viewResults.get())
        autosave = int(self.autosave.get())

        if viewresults == 0 and autosave == 0:
            alert = ActivationConfigError()
            alert.pack()
            return
        
        for pair in sequence:
            try:
                success = self.activateSequencePair(sequenceIndex, pair, benches, runs)
            except Exception:
                traceback.print_exc()
                error = SequenceError(sequenceIndex = sequenceIndex, sequenceData = pair)
                error.pack()
                continue

    def activateSequencePair(self, sequenceIndex, pair, benches, runs):
        viewresults = int(self.viewResults.get())
        autosave = int(self.autosave.get())

        if viewresults == 0 and autosave == 0:
            alert = ActivationConfigError()
            alert.pack()
            return

        resultData = { "No Data": "No data was returned." }

        benchIndex = pair["bench"]
        runIndex = pair["run"]

        bench = benches[benchIndex]
        run = runs[runIndex]

        if "module" not in run:
            alert = NoModuleError(sequenceIndex = sequenceIndex, sequenceData = pair)
            return False

        moduleList = _CONFIG_["modules"]

        if run["module"] not in moduleList:
            alert = ModuleNotFound(moduleName = run["module"], sequenceIndex = sequenceIndex, sequenceData = pair)
            return False

        startTime = time.time()

        try:
            bluePrint = moduleList[run["module"]]
            module = bluePrint(parameters = run, testbench = bench)

            resultData = module.run_test()
        except Exception:
            traceback.print_exc()
            error = ModuleError(moduleName = run["module"], sequenceIndex = sequenceIndex, sequenceData = pair)
            error.pack()
            return False

        endTime = time.time()
        runtime = endTime - startTime
        resultData["MODULE_RUNTIME"] = str(runtime)
        
        resultParameters = {}
        for key in resultData:
            parameter = Parameter(key = key, value = str(resultData[key]))
            resultParameters[key] = parameter

        resultPath = None
        if autosave == 1:
            resultPath = self.getResultPath(sequenceIndex, benchIndex, runIndex)
            resultModel = Parameters(path = resultPath)
            resultModel.setParameters(parameters = resultParameters)
            resultModel.saveParameters()

        if viewresults == 1:
            results = ResultsWindow(
                moduleName = run["module"], 
                sequenceIndex = sequenceIndex, 
                benchIndex = benchIndex,
                runIndex = runIndex,
                resultPath = resultPath,
                resultData = resultData,
                suite = self.suite
            )
            results.pack()

        return True

    def getResultPath(self, sequenceIndex, benchIndex, runIndex):
        collections = self.suite.getDataCollections()
        benchCollection = collections["benches"]
        runCollection = collections["runs"]

        benchModel = benchCollection.getModel(modelIndex = benchIndex)
        runModel = runCollection.getModel(modelIndex = runIndex)

        benchName = benchModel.pureName
        runName = runModel.pureName

        path = _CONFIG_["result_dir"]
        path += self.suite.modelData.pureName + "/"
        
        fileName = "[Seq-" + str(sequenceIndex) +"][Bench-" + str(benchIndex) + "-" + str(benchName) + "][Run-" + str(runIndex) + "-" + str(runName) + "]"
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
