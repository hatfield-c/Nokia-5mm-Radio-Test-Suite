import tkinter
import core.interfaces.Builder

from Config import _CONFIG_
from core.UIFactory import UIFactory
from core.interfaces.Builder import Builder
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
        self.sequenceDropDown.grid(row = 0, column = 0, columnspan = 2, padx = (3, 0), pady = (3, 0), sticky = "ew")
        self.dropDown = tkinter.Frame(self)

        self.rebuild()

    def rebuild(self):
        sequenceBuilder = self.suite.getWorkspace(key = "sequences")

        self.dropDown.destroy()

        if not isinstance(sequenceBuilder, core.interfaces.Builder.Builder):
            seqData = { }
        else:
            seqData = sequenceBuilder.compileData()

        curSequence = self.sequenceDropDown.get()

        if curSequence in seqData:
            sequence = seqData[curSequence]
        else:
            sequence = { }


        self.pairList = self.buildSelectList(sequence)
        self.currentPair = tkinter.StringVar()
        self.currentPair.set(self.NONE_STR)

        if not self.pairList:
            options = { self.NONE_STR }
        else:
            options = self.pairList
        
        self.dropDown = tkinter.ttk.Combobox(self, textvariable = self.currentPair, values = options, state = "readonly")
        self.dropDown.grid(row = 1, column = 0, sticky = "ew", padx = (3, 0))

        self.refreshButton = tkinter.Button(self, text = u"\u27F3", command = self.rebuild, borderwidth = 0)
        self.refreshButton.grid(row = 1, column = 1, padx = 10, pady = (5, 3))

    def buildSelectList(self, sequence):
        benchWorkspace = self.suite.getWorkspace("benches")
        unitWorkspace = self.suite.getWorkspace("units")

        if not isinstance(benchWorkspace, core.interfaces.Builder.Builder) or not isinstance(unitWorkspace, core.interfaces.Builder.Builder):
            benchData = {}
            unitData = {}
        else:
            benchData = benchWorkspace.compileData()
            unitData = unitWorkspace.compileData()

        selectList = []

        if "data" not in sequence:
            return selectList
        
        for pair in sequence["data"]:
            if "bench" not in pair or "unit" not in pair:
                    continue

            if pair["bench"] == "" or pair["unit"] == "":
                continue

            benchIndex = pair["bench"]
            unitIndex = pair["unit"]
            
            benchPath = benchData[benchIndex]["fileName"]
            unitPath = unitData[unitIndex]["fileName"]

            option = str(benchIndex) + ":" + str(benchPath) + ",   " + str(unitIndex) + ":" + str(unitPath)
            selectList.append(option)

        return selectList

    def get(self):
        defaultData = { "sequenceIndex": "", "benchIndex": "", "unitIndex": ""  }

        sequenceOption = self.sequenceDropDown.get()
        pairOption = self.currentPair.get()

        if sequenceOption is None or sequenceOption == self.NONE_STR:
            return defaultData

        if pairOption is None or pairOption == self.NONE_STR:
            return defaultData
        
        pairSplit = pairOption.split(",   ")
        benchSplit = pairSplit[0].split(":")
        unitSplit = pairSplit[1].split(":")

        benchIndex = benchSplit[0]
        unitIndex = unitSplit[0]

        data = { "sequenceIndex": sequenceOption, "benchIndex": benchIndex, "unitIndex": unitIndex  }
        return data