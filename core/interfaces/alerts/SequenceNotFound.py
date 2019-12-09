from core.interfaces.Alert import Alert

class SequenceNotFound(Alert):
    def __init__(self, sequenceIndex):
        super().__init__(
            title = "Sequence Not Found",
            data = {
                "title": "SEQUENCE WAS NOT FOUND",
                "description": (
                    "The application could not locate the following sequence in its loaded data:\n" + 
                    "   '" + str(sequenceIndex) + "'\n\n" + 
                    "This is highly unusualy behavior, and is non-recoverable. As such the next sequence will be loaded."
                )
            }, 
            dimensions = {
                "height": 200,
                "width": 400
            }
        )