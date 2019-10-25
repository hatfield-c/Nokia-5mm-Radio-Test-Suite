from Editor import Editor

class Empty(Editor):
    def __init__(self, title = "", root = None, color = None):
        super().__init__(title = title, root = root)
        self.config(background = color)