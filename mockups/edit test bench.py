import tkinter as tk
from PIL import ImageTk, Image

EditBench = tk.Tk()
EditBench.title("Edit Test Bench: Room Temperature, Straight Beam")
EditBench.iconbitmap("icon.ico")

msg = tk.Label(EditBench, text = "Edit Test Bench", font = ("Arial", 16))
msg.pack(pady = 10)

#
#   ALLOCATION FILE
#

allText = tk.Label(EditBench, text = "Allocation File:", font = ("Arial", 12))
allText.pack(padx = (0, 350))

allField = tk.Entry(EditBench, font = ("Arial", 12), width = 40)
allField.insert(0, "C:\Program Files\Allocation Files\\alloc.a ")
allField.pack(pady = (0, 10))

#
#   BENCH FIELDS
#

fieldText = tk.Label(EditBench, text = "Bench Fields:", font = ("Arial", 12))
fieldText.pack(padx = (0, 350))

fields = tk.Frame(EditBench)
fields.pack(pady = 10)

addField = tk.Button(fields, text = "Add Field (+)", width = 50)
addField.pack()

field1 = tk.Frame(fields)
field1.pack(pady = 10)

f1Label = tk.Entry(field1, width = 11)
f1Label.insert(0, "temp")
f1Label.grid(row = 0)

f1Val = tk.Entry(field1, width = 11)
f1Val.insert(0, "75.0")
f1Val.grid(row = 0, column = 1, padx = 5)

f1Type = tk.Entry(field1, width = 11)
f1Type.insert(0, "float")
f1Type.grid(row = 0, column = 2)

f1Desc = tk.Entry(field1, width = 25)
f1Desc.insert(0, "Temperature of environment")
f1Desc.grid(row = 0, column = 3, padx = 5)

f1Del = tk.Button(field1, text = "Delete", width = 10)
f1Del.grid(row = 0, column = 4)

field2 = tk.Frame(fields)
field2.pack(pady = 10)

f2Label = tk.Entry(field2, width = 11)
f2Label.insert(0, "shape")
f2Label.grid(row = 0)

f1Val = tk.Entry(field2, width = 11)
f1Val.insert(0, "cylinder")
f1Val.grid(row = 0, column = 1, padx = 5)

f2Type = tk.Entry(field2, width = 11)
f2Type.insert(0, "string")
f2Type.grid(row = 0, column = 2)

f2Desc = tk.Entry(field2, width = 25)
f2Desc.insert(0, "Shape of test chamber")
f2Desc.grid(row = 0, column = 3, padx = 5)

f2Del = tk.Button(field2, text = "Delete", width = 10)
f2Del.grid(row = 0, column = 4)

#
#   Buttons
#

saveLoad = tk.Frame(EditBench)
saveLoad.pack(pady = (20, 10))

save = tk.Button(saveLoad, text = "Save", width = 20)
save.grid(row = 0, padx = (0, 10))

load = tk.Button(saveLoad, text = "Load", width = 20)
load.grid(row = 0, column = 2)

#
#   WINDOW
#

EditBench.geometry("500x400")
EditBench.mainloop()