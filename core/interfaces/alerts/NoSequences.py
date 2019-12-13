from core.interfaces.Alert import Alert

class NoSequences(Alert):
    def __init__(self):
        super().__init__(
            title = "No Configured Sequences",
            data = {
                "title": "NO CONFIGURED SEQUENCES",
                "description": "There were no detected valid sequences to be activated. Please check that bench/unit pairings exist as required."
            }
        )