import tkinter as tk
from PIL import ImageTk, Image

EditBench = tk.Tk()
EditBench.title("Test Results: Room Temperature, Straight Beam | 10,000 MHz, obue")
EditBench.iconbitmap("icon.ico")

msg = tk.Label(EditBench, text = "Results", font = ("Arial", 16))
msg.pack(pady = 10)

#
#   RESULTS
#

cols = tk.Frame(EditBench)
cols.pack(pady = 10)

col1 = tk.Frame(cols)
col1.grid(row = 0)

col2 = tk.Frame(cols)
col2.grid(row = 0, column = 1, padx = 10)

col3 = tk.Frame(cols)
col3.grid(row = 0, column = 2)

#
#    COL1
#

col1Label = tk.Label(col1, text = "    Bench Data    ", font = ("Arial", 16))
col1Label.pack(pady = 10)

benchData = tk.Message(col1, width = 150, bg = "lightgrey", text = "temp: 75.0\nshape: cylinder\n \n ")
benchData.pack()

#
#    COL2
#

col2Label = tk.Label(col2, text = "    Test Data    ", font = ("Arial", 16))
col2Label.pack(pady = 10)

testData = tk.Message(col2, bg = "lightgrey", text = "freq: 10000.00\nmod: obue\n \n ")
testData.pack()

#
#    COL3
#

col3Label = tk.Label(col3, text = "    Results    ", font = ("Arial", 16))
col3Label.pack(pady = 10)

resultData = tk.Message(col3, bg = "lightgrey", text = "noise: +/- 0.05\nsignals sent: 100\nsignals received: 95\nsuccess rate: 95%")
resultData.pack()

#
#   Buttons
#

saveLoad = tk.Frame(EditBench)
saveLoad.pack(pady = (20, 10))

save = tk.Button(saveLoad, text = "Save Results", width = 20)
save.grid(row = 0)

load = tk.Button(saveLoad, text = "Return", width = 20)
load.grid(row = 0, column = 2, padx = 10)

load = tk.Button(saveLoad, text = "Run Again", width = 20)
load.grid(row = 0, column = 3)

#
#   WINDOW
#

EditBench.geometry("500x300")
EditBench.mainloop()