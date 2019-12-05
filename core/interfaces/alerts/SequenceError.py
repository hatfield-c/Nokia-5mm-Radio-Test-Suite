from core.interfaces.Alert import Alert

class SequenceError(Alert):
    def __init__(self, sequenceIndex, sequenceData):
        super().__init__(
            title = "Sequence Error",
            data = {
                "title": "SEQUENCE ERROR",
                "description": (
                    "There has been a non-recoverable error while attempting to activate the Sequence with ID '" + 
                    str(sequenceIndex)  + 
                    "'\n\n" + 
                    "Sequence Data:\n" +
                    "    " + str(sequenceData) + "\n\n" +
                    "This application will attempt to retrieve the result data if possible, and then continue to the next sequence pair."
                )
            }, 
            dimensions = {
                "height": 200,
                "width": 400
            }
        )