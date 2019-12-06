import tkinter
from Config import _CONFIG_
from core.UIFactory import UIFactory
from core.inputs.CollectionDropDown import CollectionDropDown

class SequencePairSelector(tkinter.Frame):

    NONE_STR = "NONE"

    def __init__(self, root, suite):
        self.root = root
        self.suite = suite

        super().__init__(root)
        self.columnconfigure(0, weight = 1)

        self.sequenceDropDown = CollectionDropDown(
            args = {
                "root": self,
                "config": {},
                "data": ["sequences", ""],
                "orig": ""
            }     
        )
        self.sequenceDropDown.grid(row = 0, column = 0, columnspan = 2)
        self.dropDown = tkinter.Frame(self)

        self.rebuild()

    def rebuild(self):
        sequenceBuilder = self.suite.getWorkspace(key = "sequences")

        self.dropDown.destroy()

        if sequenceBuilder is None:
            seqData = { }
        else:
            seqData = sequenceBuilder.compileData()

        curSequence = self.sequenceDropDown.get()

        if curSequence in seqData:
            sequence = seqData[curSequence]
        else:
            sequence = []

        self.pairList = self.buildSelectList(sequence)
        self.currentPair = tkinter.StringVar()
        self.currentPair.set(self.NONE_STR)

        if not self.pairList:
            options = { self.NONE_STR }
        else:
            options = self.pairList
        
        self.dropDown = tkinter.OptionMenu(self, self.currentPair, *options)
        self.dropDown.grid(row = 1, column = 0, sticky = "ew")

        self.refreshButton = tkinter.Button(self, text = u"\u27F3", command = self.rebuild, borderwidth = 0)
        self.refreshButton.grid(row = 1, column = 1, padx = 10)

    def buildSelectList(self, sequence):
        benchCollection = self.suite.getWorkspace("benches").dataCollection
        runCollection = self.suite.getWorkspace("runs").dataCollection

        selectList = []
        for pair in sequence:
            benchIndex = pair["bench"]
            runIndex = pair["run"]

            benchModel = benchCollection.getModel(modelIndex = benchIndex)
            runModel = runCollection.getModel(modelIndex = runIndex)
            
            if benchModel is None or runModel is None:
                continue

            benchPath = benchModel.fileName
            runPath = runModel.fileName

            option = str(benchIndex) + ":" + str(benchPath) + ",   " + str(runIndex) + ":" + str(runPath)
            selectList.append(option)

        return selectList

    def get(self):
        defaultData = { "sequenceIndex": "", "benchIndex": "", "runIndex": ""  }

        sequenceOption = self.sequenceDropDown.get()
        pairOption = self.currentPair.get()

        if sequenceOption is None or sequenceOption == self.NONE_STR:
            return defaultData

        if pairOption is None or pairOption == self.NONE_STR:
            return defaultData
        
        pairSplit = pairOption.split(",   ")
        benchSplit = pairSplit[0].split(":")
        runSplit = pairSplit[1].split(":")

        benchIndex = benchSplit[0]
        runIndex = runSplit[0]

        data = { "sequenceIndex": sequenceOption, "benchIndex": benchIndex, "runIndex": runIndex  }
        return data