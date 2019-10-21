import tkinter as tk
from PIL import ImageTk, Image

EditSuite = tk.Tk()
EditSuite.title("Edit Test Suite: obue_suite")
EditSuite.iconbitmap("icon.ico")

msg = tk.Label(EditSuite, text = "Test Suite Checklist", font = ("Arial", 16))
msg.pack(pady = 10)

#
#   STEP 1
#

step1 = tk.Frame(EditSuite)
step1.pack()

step1Text = tk.Label(step1, text = "1: Test Benches", font = ("Arial", 12))
step1Text.pack(padx = (0, 350))

step1NewBench = tk.Button(step1, text = "New Bench", width = 40)
step1NewBench.pack()

step1Bench1 = tk.Frame(step1)
step1Bench1.pack(pady = 5)

bench1Name = tk.Label(step1Bench1, text = "-   Room Temperature, Straight Beam", font = ("Arial", 10))
bench1Name.grid(row = 0)

bench1Edit = tk.Button(step1Bench1, text = "Edit", font = ("Arial", 10))
bench1Edit.grid(row = 0, column = 1, padx = 5)

bench1Delete = tk.Button(step1Bench1, text = "Delete", font = ("Arial", 10))
bench1Delete.grid(row = 0, column = 2)

step1Bench2 = tk.Frame(step1)
step1Bench2.pack(padx = (0, 3))

bench2Name = tk.Label(step1Bench2, text = "-   Room Temperature, West Beam   ", font = ("Arial", 10))
bench2Name.grid(row = 0)

bench2Edit = tk.Button(step1Bench2, text = "Edit", font = ("Arial", 10))
bench2Edit.grid(row = 0, column = 1, padx = 5)

bench2Delete = tk.Button(step1Bench2, text = "Delete", font = ("Arial", 10))
bench2Delete.grid(row = 0, column = 2)

#
#   STEP 2
#

step2 = tk.Frame(EditSuite)
step2.pack(pady = (15, 0))

step2Text = tk.Label(step2, text = "2: Test Runs     ", font = ("Arial", 12))
step2Text.pack(padx = (0, 350))

step2NewTest = tk.Button(step2, text = " New Test ", width = 40)
step2NewTest.pack()

step2Test1 = tk.Frame(step2)
step2Test1.pack(pady = 5, padx = (0, 6))

test1Name = tk.Label(step2Test1, text = "-   10,000 MHz, obue        ", font = ("Arial", 10))
test1Name.grid(row = 0)

test1Edit = tk.Button(step2Test1, text = "Edit", font = ("Arial", 10))
test1Edit.grid(row = 0, column = 1, padx = 5)

test1Delete = tk.Button(step2Test1, text = "Delete", font = ("Arial", 10))
test1Delete.grid(row = 0, column = 2)

step2Test2 = tk.Frame(step2)
step2Test2.pack()

test2Name = tk.Label(step2Test2, text = "-   20,000 MHz, obue_plus", font = ("Arial", 10))
test2Name.grid(row = 0)

test2Edit = tk.Button(step2Test2, text = "Edit", font = ("Arial", 10))
test2Edit.grid(row = 0, column = 1, padx = 5)

test2Delete = tk.Button(step2Test2, text = "Delete", font = ("Arial", 10))
test2Delete.grid(row = 0, column = 2)

#
#   STEP 3
#

step3 = tk.Frame(EditSuite)
step3.pack(pady = (15, 0))

step3Text = tk.Label(step3, text = "3: Test Sequences", font = ("Arial", 12))
step3Text.pack(padx = (0, 330))

step3NewTest = tk.Button(step3, text = " New Bench/Test Pair ", width = 40)
step3NewTest.pack()

pair1 = tk.Frame(step3)
pair1.pack(pady = 5, padx = (0, 6))

pair1Bench = tk.Entry(pair1, width = 25, font = ("Arial", 10))
pair1Bench.insert(0, "Room Temperature, Straight Beam")
pair1Bench.grid(row = 0)

pair1Run = tk.Entry(pair1, width = 25, font = ("Arial", 10))
pair1Run.insert(0, "10,000 MHz, obue")
pair1Run.grid(row = 0, column = 1, padx = 5)

pair1Save = tk.Button(pair1, text = "Run", font = ("Arial", 10))
pair1Save.grid(row = 0, column = 2)

pair1Delete = tk.Button(pair1, text = "Delete", font = ("Arial", 10))
pair1Delete.grid(row = 0, column = 3, padx = 5)

pair2 = tk.Frame(step3)
pair2.pack(pady = 5, padx = (0, 6))

pair2Bench = tk.Entry(pair2, width = 25, font = ("Arial", 10))
pair2Bench.insert(0, "Room Temperature, West Beam")
pair2Bench.grid(row = 0)

pair2Run = tk.Entry(pair2, width = 25, font = ("Arial", 10))
pair2Run.insert(0, "10,000 MHz, obue")
pair2Run.grid(row = 0, column = 1, padx = 5)

pair2Save = tk.Button(pair2, text = "Run", font = ("Arial", 10))
pair2Save.grid(row = 0, column = 2)

pair2Delete = tk.Button(pair2, text = "Delete", font = ("Arial", 10))
pair2Delete.grid(row = 0, column = 3, padx = 5)

step3RunSequence = tk.Button(step3, text = " Run Sequence ", width = 40)
step3RunSequence.pack(pady = (10, 10))

step3RunAll = tk.Button(step3, text = " Run All Existing Combinations ", width = 40)
step3RunAll.pack()

#
#   WINDOW
#

saveSuite = tk.Button(EditSuite, text = " Save Test Suite ", width = 20)
saveSuite.pack(pady = (50, 0))

EditSuite.geometry("500x600")
EditSuite.mainloop()