from tkinter import *

root = Tk()

root.title("User Input")
enter1 = Entry(root, width=50)
enter1.pack()
enter1.insert(0, "Starting IP Address goes here")

enter2 = Entry(root, width=50)
enter2.pack()
enter2.insert(0, "Enter Subnet Mask here")

enter3 = Entry(root, width=50)
enter3.pack()
enter3.insert(0, "Enter in the GTWY IP Address")

options = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]
clicked = StringVar()

# initial menu text
clicked.set("Select Lab Here")

# Create Dropdown menu
drop = OptionMenu(root, clicked, *options)
drop.pack()

def myClick():
    address = enter1.get()
    subnetmask = enter2.get()
    lab_id = clicked.get()
    gtwy_address = enter3.get()
    myLabel = Label(root, text="This is the starting point: " + address)
    myLabel.pack()
    myLabel = Label(root, text="This is the SM: " + subnetmask)
    myLabel.pack()
    myLabel = Label(root, text="This is the GTWY: " + gtwy_address)
    myLabel.pack()
    myLabel = Label(root, text="This is the lab: " + lab_id)
    myLabel.pack()

def doneClick():
    myLabel2 = Label(root, text="DONE and SAVED")
    myLabel2.pack()

myButton1 = Button(root, text="Confirm Changes", command =myClick)
myButton1.pack()

myButton2 = Button(root, text="Close", command =doneClick)
myButton2.pack(side="left")

myButton3 = Button(root, text="QUIT", command =doneClick)
myButton3.pack(side="right")

root.mainloop()