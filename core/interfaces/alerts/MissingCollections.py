from core.interfaces.Alert import Alert

class MissingCollections(Alert):
    def __init__(self):
        super().__init__(
            title = "Missing Collection",
            data = {
                "title": "MISSING COLLECTION",
                "description": "A data collection was detected to be missing.\n\n" +
                    "This can occur if you have built a Suite, but have not saved it yet.\n\n" +
                    "Please try saving the Suite, as well as the data collection of each Builder."
            }, 
            dimensions = {
                "height": 150,
                "width": 400
            }
        )