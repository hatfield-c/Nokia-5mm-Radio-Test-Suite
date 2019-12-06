from core.interfaces.Alert import Alert

class NoModuleError(Alert):
    def __init__(self, sequenceIndex, sequenceData):
        super().__init__(
            title = "No Module Error",
            data = {
                "title": "NO MODULE",
                "description": (
                    "No module was detected in the following sequence pair:\n" + 
                    "    Sequence Index: " + str(sequenceIndex) + "\n" +
                    "    Bench/Run Pair: " + str(sequenceData) + "\n\n" +
                    "This application will abort the execution of this sequence pair, and continue to the next set."
                )
            }, 
            dimensions = {
                "height": 200,
                "width": 400
            }
        )