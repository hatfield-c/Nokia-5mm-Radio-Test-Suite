from core.inputs.Label import Label
from core.inputs.Entry import Entry
from core.inputs.Radio import Radio
from core.inputs.AllocationFile import AllocationFile
from core.inputs.CollectionDropDown import CollectionDropDown

class InputFactory:

    INPUTS = {
        "entry": Entry,
        "label": Label,
        "radio": Radio,
        "allocation_file": AllocationFile,
        "sequence_select": CollectionDropDown
    }

    OPEN_COMMAND = "<"
    CLOSE_COMMAND = ">"
    ARG_DELIM = "|"

    def __init__(self):
        pass

    def create(self, root, rawString, args = {}):
        if rawString is None or root is None:
            return None

        data = self.parse(rawString)

        if data["id"] not in self.INPUTS:
            return None

        arguments = { 
            "root": root,
            "config": args,
            "orig": data["orig"],
            "data": data["args"]
        }
        bluePrint = self.INPUTS[data["id"]]
        
        return bluePrint(arguments)

    def parse(self, string):
        default = {
            "id": "entry",
            "orig": string,
            "args": [ ]
        }

        if not string.startswith(self.OPEN_COMMAND) or not string.endswith(self.CLOSE_COMMAND):
            return default

        if len(string) < 3:
            return default

        cutString = string[1:-1]
        args = cutString.split(self.ARG_DELIM)

        if args is None or len(args) == 0:
            return default

        inputId = args.pop(0)

        if inputId not in self.INPUTS:
            return default

        data = {
            "id": inputId,
            "orig": string,
            "args": args
        }

        return data