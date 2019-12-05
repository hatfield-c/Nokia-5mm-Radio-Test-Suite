from core.interfaces.Alert import Alert

class NoKeyValueError(Alert):
    def __init__(self, path):
        super().__init__(
            title = "No Key/Value Error",
            data = {
                "title": "NO KEY OR VALUE FIELD",
                "description": "There was no 'key' or 'value' field(s) found in the CSV data with path:\n'" + str(path)
            }, 
            dimensions = {
                "height": 150,
                "width": 400
            }
        )