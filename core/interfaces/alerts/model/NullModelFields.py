from core.interfaces.Alert import Alert

class NullModelFields(Alert):
    def __init__(self, path):
        super().__init__(
            title = "Null Fields",
            data = {
                "title": "NULL MODEL FIELDS",
                "description": (
                    "Null fields were detected during a save/load operation for a model associated with the path:\n\t'" + 
                    str(path) + 
                    "'.\nPlease check the field specification of this model and compare it to the associated CSV file."
                )
            }
        )