from core.interfaces.Alert import Alert

class ModuleError(Alert):
    def __init__(self, moduleName, sequenceIndex, sequenceData):
        super().__init__(
            title = "Module Error",
            data = {
                "title": "MODULE EXECUTION ERROR",
                "description": (
                    "There has been a non-recoverable error while running test module:\n'" + 
                    "    " + str(moduleName)  + "'\n\n" + 
                    "With sequence data:\n" +
                    "    Index:" + str(sequenceIndex) + "\n" +
                    "    Bench/Run:" + str(sequenceData) + "\n\n" +
                    "This application will abort the execution of this module, and continue to the next sequence."
                )
            }, 
            dimensions = {
                "height": 200,
                "width": 400
            }
        )