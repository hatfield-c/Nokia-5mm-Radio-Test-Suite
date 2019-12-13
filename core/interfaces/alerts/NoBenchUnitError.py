from core.interfaces.Alert import Alert

class NoBenchUnitError(Alert):
    def __init__(self, path):
        super().__init__(
            title = "No Bench/Unit Error",
            data = {
                "title": "NO BENCH OR UNIT FIELD",
                "description": "There was no 'bench' or 'unit' field(s) found in the sequence CSV data with path:\n'" + str(path)
            }, 
            dimensions = {
                "height": 150,
                "width": 400
            }
        )