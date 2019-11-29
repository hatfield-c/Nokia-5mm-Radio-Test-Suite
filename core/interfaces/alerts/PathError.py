from core.interfaces.Alert import Alert

class PathError(Alert):
    def __init__(self, path, pathType = "model"):
        super().__init__(
            title = str(pathType) + " Path Error",
            data = {
                "title": "PATH ERROR",
                "description": "There was an issue loading/saving " + str(pathType) + " data with the path '" + str(path) + "'"
            }, 
            dimensions = {
                "height": 150,
                "width": 400
            }
        )