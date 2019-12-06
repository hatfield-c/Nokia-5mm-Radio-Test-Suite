from core.interfaces.Alert import Alert

class ConfigError(Alert):
    def __init__(self):
        super().__init__(
            title = "Activation Error",
            data = {
                "title": "ACTIVATION ERROR",
                "description": "Neither 'View Results' nor 'Autosave' was selected in the 'Begin Testing' configuration frame.\n\n" +
                    "One or both of these boxes must be checked in order for this application to do something useful."
            }, 
            dimensions = {
                "height": 150,
                "width": 400
            }
        )