import tkinter as tk
from PIL import ImageTk, Image

LoadSuite = tk.Tk()
LoadSuite.title("Load Test Suite")
LoadSuite.iconbitmap("icon.ico")

img = ImageTk.PhotoImage(Image.open("logo.png"))
logo = tk.Label(LoadSuite, image = img)
logo.pack()

msg = tk.Label(LoadSuite, text = "Please choose test suite to load:", font = ("Arial", 16))
msg.pack(pady = 10)

chooseSuite = tk.Frame(LoadSuite)
chooseSuite.pack()

suiteField = tk.Entry(chooseSuite, width=50)
suiteField.insert(0, "C:\Program Files\Test Suites\\obue_suite.csv ")
suiteField.grid(row = 0)

browse = tk.Button(chooseSuite, text = "Browse")
browse.grid(row = 0, column = 1)

options = tk.Frame(LoadSuite)
options.pack(pady = 10)

run = tk.Button(options, text = "Run")
run.grid(row = 0 ,padx = (0, 10))

edit = tk.Button(options, text = "Edit")
edit.grid(row = 0, column = 1, padx = (10, 0))

LoadSuite.geometry("500x300")
LoadSuite.mainloop()