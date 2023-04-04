# This module creates an initial popup box asking for CML credentials
import tkinter
from tkinter import *
import tkinter.font as font
import CMLinfo

V = CMLinfo

def info():

    def confirmClick():
        V.CML['host'] = enter1.get()
        V.CML['username'] = enter2.get()
        V.CML['password'] = enter3.get()
        root.destroy()

    root = Tk()
    root.title("CML Input")
    root.geometry("300x250")
    message = "Confirm when done"
    text_box = Text(root, height=1, width=70)
    text_box.pack(expand=TRUE)
    text_box.insert(END, message)

    label1 = Label(root, text="CML IP Address")
    label1.pack(side=TOP)
    enter1 = Entry(root, width=20)
    enter1.pack(side=TOP)
    enter1.insert(0, V.CML['host'])

    label2 = Label(root, text="CML Username")
    label2.pack(side=TOP)
    enter2 = Entry(root, width=20)
    enter2.pack(side=TOP)
    enter2.insert(0, V.CML['username'])

    label3 = Label(root, text="CML Password")
    label3.pack(side=TOP)
    enter3 = Entry(root, width=20)
    enter3.pack(side=TOP)
    enter3.insert(0, V.CML['password'])

    button_font = font.Font(size=10, weight="bold")
    myButton1 = Button(root, text="Confirm CML Settings", command=confirmClick)
    myButton1['font'] = button_font
    myButton1.pack()

    tkinter.mainloop()