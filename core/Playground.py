import tkinter

class parent:
    TES = "a"

    def __init__(self):
        print(self.TES)

class child(parent):
    TES = "b"

    def __init__(self):
        print(self.TES)
        print(parent.TES)

p = parent()
print(p.TES)
c = child()
print(c.TES,"\n")

lis = [p, c]
model = lis[0]
print(model.TES)
model = lis[1]
print(model.TES)

App = tkinter.Tk()

pFrame = tkinter.Frame(App, width = "300", height = "200")
pFrame.grid_rowconfigure(0, weight = 1)
pFrame.grid_columnconfigure(0, weight = 1)

canvas = tkinter.Canvas(pFrame, width = 300, height = 200)
canvas.grid_propagate(False)

frameContainer = tkinter.Frame(canvas)

c1Frame = tkinter.Frame(frameContainer, bg = "green", width = "280", height = "150")
c2Frame = tkinter.Frame(frameContainer, bg = "red", width = "280", height = "150")

scrollbar = tkinter.Scrollbar(pFrame, orient = "vertical", command = canvas.yview)
canvas.configure(yscrollcommand = scrollbar.set)
pFrame.grid_propagate(False)

c1Frame.grid(row = 0, column = 0)
c2Frame.grid(row = 1, column = 0)


#frameContainer.pack()
canvas.grid(row = 0, column = 0, sticky = "news")
scrollbar.grid(row = 0, column = 1, sticky = "ns")

canvas.create_window((0, 0), window = frameContainer, anchor = "nw")
pFrame.grid(row = 0, column = 0)

def setScrollRegion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas.bind("<Configure>", setScrollRegion)

print(canvas.bbox("all"))
canvas.configure(scrollregion = canvas.bbox("all"))

App.geometry("300x200")
#App.resizable(width=False, height=False)
App.mainloop()