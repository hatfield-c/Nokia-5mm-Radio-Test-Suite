from core.interfaces.Builder import Builder

class Empty(Builder):
    def __init__(self, title = "", root = None, color = None):
        super().__init__(title = title, root = root)
        self.config(background = color)