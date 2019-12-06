from core.interfaces.Alert import Alert

class ModuleNotFound(Alert):
    def __init__(self, moduleName, sequenceIndex, sequenceData):
        super().__init__(
            title = "Module Not Found",
            data = {
                "title": "MODULE NOT FOUND",
                "description": (
                    "A sequence attempted to load a module which is not registered with the application:\n" + 
                    "    module: '" + str(moduleName)  + "'\n\n" + 
                    "Sequence data:\n" +
                    "    Sequence Index: " + str(sequenceIndex) + "\n" +
                    "    Bench/Run Pair: " + str(sequenceData) + "\n\n" +
                    "This application will abort the execution of this module, and continue to the next sequence pair."
                )
            }, 
            dimensions = {
                "height": 200,
                "width": 400
            }
        )