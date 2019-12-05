from core.interfaces.Alert import Alert

class NoKeyError(Alert):
    def __init__(self, path):
        super().__init__(
            title = "No Key Error",
            data = {
                "title": "NO KEY FIELD",
                "description": "There was no 'key' field found in the CSV data with path:\n'" + str(path)
            }, 
            dimensions = {
                "height": 150,
                "width": 400
            }
        )