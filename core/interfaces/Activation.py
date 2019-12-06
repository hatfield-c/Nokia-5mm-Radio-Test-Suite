import tkinter
import traceback
import time

from Config import _CONFIG_
from core.inputs.CollectionDropDown import CollectionDropDown
from core.inputs.activation.SequencePairSelector import SequencePairSelector

from core.Interface import Interface
from core.interfaces.Builder import Builder
from core.interfaces.Alert import Alert

from core.interfaces.alerts.NoSequences import NoSequences
from core.interfaces.alerts.SequenceError import SequenceError
from core.interfaces.alerts.ModuleError import ModuleError
from core.interfaces.alerts.NoModuleError import NoModuleError
from core.interfaces.alerts.ModuleNotFound import ModuleNotFound


class Activation(Interface):
    def __init__(self, root, suite):
        super().__init__(root = root, title = "Begin Testing", dimensions = Builder.DEFAULT_DIMENSIONS)
        self.suite = suite
        self.verbose = tkinter.IntVar()
        self.verbose.set("0")

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
        self.logo.grid(row = 0, column = 0, pady = 10, sticky = "n")

        self.buttonRow = tkinter.Frame(
            self.container, 
            pady = 10,
            background ="white", 
            borderwidth = 2, 
            relief = "groove"
        )
        self.buttonRow.grid(row = 1, column = 0, padx = 21, pady = (0, 10), sticky = "ews")

        self.buttonRow.rowconfigure(0, weight = 1)
        self.buttonRow.rowconfigure(1, weight = 1)
        self.buttonRow.columnconfigure(0, weight = 1)
        self.buttonRow.columnconfigure(1, weight = 1)
        self.buttonRow.columnconfigure(2, weight = 1)

        self.verboseFrame = tkinter.Frame(
            self.buttonRow,
            background = _CONFIG_["blue_primary"],
            borderwidth = 2,
            relief = "groove",
            padx = 5,
            pady =5
        )
        self.verboseFrame.grid(row = 0, column = 1)
        
        self.verboseCheckbox = tkinter.Checkbutton(
            self.verboseFrame, 
            text = "Success Pop-up Windows", 
            variable = self.verbose,
            borderwidth = 2,
            relief = "groove"
        )
        self.verboseCheckbox.grid(row = 0, column = 0)

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
        appData = self.suite.compileData()

        benches = appData["benches"]
        runs = appData["runs"]
        sequences = appData["sequences"]

        sequenceIndex = self.sequenceDropDown.get()
        sequence = sequences[sequenceIndex]

        self.activateSequence(sequenceIndex, sequence, benches, runs)

    def pair(self):
        appData = self.suite.compileData()

        benches = appData["benches"]
        runs = appData["runs"]

        pairData = self.pairDropDown.get()
        sequenceIndex = pairData["sequenceIndex"]
        pair = { "bench": pairData["benchIndex"], "run": pairData["runIndex"] }

        self.activateSequencePair(sequenceIndex, pair, benches, runs)

    def activateSequence(self, sequenceIndex, sequence, benches, runs):
        for pair in sequence:
            try:
                success = self.activateSequencePair(sequenceIndex, pair, benches, runs)
            except Exception:
                traceback.print_exc()
                error = SequenceError(sequenceIndex = sequenceIndex, sequenceData = pair)
                error.pack()
                continue

    def activateSequencePair(self, sequenceIndex, pair, benches, runs):
        result = { "No Data": "No data was returned." }

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

            result = module.run_test()
        except Exception:
            traceback.print_exc()
            error = ModuleError(moduleName = run["module"], sequenceIndex = sequenceIndex, sequenceData = pair)
            error.pack()
            return False

        endTime = time.time()
        runtime = endTime - startTime

        string = str(result)

        isVerbose = self.verbose.get()

        if int(isVerbose) == 1:
            alert = Alert(title = "Success!", data = { "title": "SUCCESS!", "description": string })
            alert.pack()

        return True

        