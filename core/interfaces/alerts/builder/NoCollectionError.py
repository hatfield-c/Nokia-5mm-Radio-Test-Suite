from core.interfaces.Alert import Alert

class NoCollectionError(Alert):
    def __init__(self, builderType):
        super().__init__(
            title = "Collection Missing For: " + str(builderType),
            data = {
                "title": "MISSING COLLECTION",
                "description": "A collection was not found for the '" + str(builderType) + "' Builder.\nPlease set a collection for this builder before attempting this operation."
            }, 
            dimensions = {
                "height": 150,
                "width": 400
            }
        )