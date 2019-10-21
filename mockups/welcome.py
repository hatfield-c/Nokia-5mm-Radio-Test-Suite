import tkinter as tk
from PIL import ImageTk, Image

Welcome = tk.Tk()
Welcome.title("Nokia Test Suite Editor")
Welcome.iconbitmap("icon.ico")

img = ImageTk.PhotoImage(Image.open("logo.png"))
logo = tk.Label(Welcome, image = img)
logo.pack()

msg = tk.Label(Welcome, text = "WELCOME!", font = ("Arial", 16))
msg.pack()

newSuite = tk.Button(Welcome, text = "New Test Suite", width=25)
newSuite.pack(pady = 10)

loadSuite = tk.Button(Welcome, text = "Load Test Suite", width=25)
loadSuite.pack()

Welcome.geometry("500x300")
Welcome.mainloop()