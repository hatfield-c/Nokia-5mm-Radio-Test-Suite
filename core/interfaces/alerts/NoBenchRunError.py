from core.interfaces.Alert import Alert

class NoBenchRunError(Alert):
    def __init__(self, path):
        super().__init__(
            title = "No Bench/Run Error",
            data = {
                "title": "NO BENCH OR RUN FIELD",
                "description": "There was no 'bench' or 'run' field(s) found in the sequence CSV data with path:\n'" + str(path)
            }, 
            dimensions = {
                "height": 150,
                "width": 400
            }
        )