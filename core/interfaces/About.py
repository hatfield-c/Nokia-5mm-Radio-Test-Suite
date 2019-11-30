from core.Interface import Interface
from Config import _CONFIG_
import tkinter

class About(Interface):
    def __init__(self):
        super().__init__(title = "About", dimensions = { "height": 590, "width": 600 })
        self.grid_propagate(False)
        self.columnconfigure(0, weight = 0)

        self.dummy = tkinter.Frame(self, width = self.dimensions["width"])
        self.dummy.grid(row = 0, column = 0)

        self.label = tkinter.Label(self, text = "Nokia" + u"\u2122" + " Automated Test Suite Manager v" + _CONFIG_["version"], font = "Helvetica 14 bold")
        self.label.grid(row = 1, column = 0, pady = (5, 0))

        self.copyright = tkinter.Label(self, text = u"\u00A9" + "2019 by Team #904", font = "Helevetica 8 italic")
        self.copyright.grid(row = 2, column = 0, pady = (0, 5))

        logoPath = _CONFIG_["flare_path"]
        img = tkinter.PhotoImage(file = logoPath)
        self.logo = tkinter.Label(
            self, 
            image = img, 
            background = _CONFIG_["color_primary"],
            borderwidth = 8,
            relief = "groove"
        )
        self.logo.image = img
        self.logo.grid(row = 3, column = 0, pady = 10)

        devData = {
            "names": [
                "Cody Hatfield",
                "Anthony Tang",
                "Sakari Kirvilampi",
                "Joshua Obanor"
            ],
            "delim": u"\u2B29",
            "netid": [
                "cxh124730",
                "ajt161230",
                "sjk150130",
                "jeo160230"
            ]
        }

        self.container = tkinter.Frame(
            self,
            background = "white",
            borderwidth = 2,
            relief = "groove"
        )

        devContainer = tkinter.Frame(self.container, background = "white")
        devTitle = tkinter.Label(devContainer, text = " Developers ", background = "white", font = "Helevetica 10 bold underline")
        names = tkinter.Frame(devContainer, background = "white")
        delims = tkinter.Frame(devContainer, background = "white")
        netid = tkinter.Frame(devContainer, background = "white")

        self.container.grid(row = 4, column = 0)
        devContainer.grid(row = 0)
        devTitle.grid(row = 0, column = 0, columnspan = 3)        
        names.grid(row = 1, column = 0, pady = 10, padx = (10, 0))
        delims.grid(row = 1, column = 1, pady = 10)
        netid.grid(row = 1, column = 2, pady = 10, padx = (0, 10))

        i = 0
        for name, net in zip(devData["names"], devData["netid"]):
            nameLabel = tkinter.Label(names, text = name, background = "white")
            delimLabel = tkinter.Label(delims, text = devData["delim"], background = "white")
            netidLabel = tkinter.Label(netid, text = net, background = "white")

            nameLabel.grid(row = i, column = 0)
            delimLabel.grid(row = i, column = 0)
            netidLabel.grid(row = i, column = 0)

            i += 1

        desc = (
            "This application was developed in partnership between The University of Texas at " + 
            "Dallas Senior Design Team #904, and the Las Collinas, Texas branch of Nokia Inc.\n\n" +
            "All software and media created by Team #904 for the application is henceforth indefinitely licensed to Nokia Inc. " +
            "and its subsidiaries. These licensed entities are entitled to use this software and media for its intended and limited " +
            "purpose of implementing automated test suites. Any repurpose of said software or media outside of this use will be considered " +
            "to fall outside the given rights of the aforementioned license, and compensation may be sought for the appropriate developers."
        )
        description = tkinter.Message(self.container, text = desc, width = 550, background = "white")
        description.grid(row = i, column = 0, padx = 10)

        self.button = tkinter.Button(self, text = "Close", font = "Helevetica 12 bold", command = lambda : self.root.destroy())
        self.button.grid(row = 5, column = 0, pady = 10)

        self.pack()