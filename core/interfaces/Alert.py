import tkinter
from Interface import Interface

class Alert(Interface):
    def __init__(self, title = "Alert", data = { "title": "ALERT", "description": "Something happened." }, dimensions = { "height": 300, "width": 400 }):
        super(title = title, dimensions = dimensions)

        self.label = tkinter.Label(self, text = data["title"], font = "Helvetica 14 bold")
        self.message = tkinter.Message(self, text = data["description"])
