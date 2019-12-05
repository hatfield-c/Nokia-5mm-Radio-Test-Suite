import tkinter
import traceback
import time

from Config import _CONFIG_
from core.Interface import Interface

from core.interfaces.Builder import Builder
from core.interfaces.Alert import Alert
from core.interfaces.alerts.NoSequences import NoSequences
from core.interfaces.alerts.SequenceError import SequenceError
from core.interfaces.alerts.ModuleError import ModuleError

class Activation(Interface):
    def __init__(self, root, suite):
        super().__init__(root = root, title = "Begin Testing", dimensions = Builder.DEFAULT_DIMENSIONS)
        self.suite = suite

        self.grid_propagate(False)
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        self.container = tkinter.Frame(self)
        self.container.rowconfigure(0, weight = 1)
        self.container.columnconfigure(0, weight = 1)
        self.container.grid(row = 0, stick = "nwse")

        activateButton = tkinter.Button(self.container, text = "Activate Sequences", command = lambda : self.activateSequences())
        activateButton.grid(row = 0)

    def activateSequences(self):
        appData = self.suite.compileData()

        benches = appData["benches"]
        runs = appData["runs"]
        sequences = appData["sequences"]

        if sequences is None or not sequences:
            NoSequences()
            return

        results = []
        for sequenceIndex in sequences:
            sequence = sequences[sequenceIndex]

            for pair in sequence:
                try:
                    benchIndex = pair["bench"]
                    runIndex = pair["run"]

                    bench = benches[benchIndex]
                    run = runs[runIndex]
                    startTime = time.time()

                    try:
                        bluePrint = _CONFIG_["modules"][run["module"]]
                        module = bluePrint(parameters = run, testbench = bench)

                        result = module.run_test()
                    except Exception:
                        traceback.print_exc()
                        error = ModuleError(moduleName = run["module"], sequenceIndex = sequenceIndex, sequenceData = pair)
                        error.pack()
                        continue

                    endTime = time.time()

                    results.append(result)
                    runtime = endTime - startTime

                except Exception:
                    traceback.print_exc()
                    error = SequenceError(sequenceIndex = sequenceIndex, sequenceData = pair)
                    error.pack()
                    continue

        string = str(results)

        alert = Alert(title = "Success!", data = { "title": "SUCCESS!", "description": string })
        alert.pack()
