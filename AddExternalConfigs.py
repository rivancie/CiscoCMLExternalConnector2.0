# This module provides a popup for additional user input. This will prompt the user for the seed address,
# default gtwy, and management vrf to be added to the devices.
import tkinter
import GlobalVar
import requests
import json
from tkinter import *
import sys
import tkinter.font as font
import ast
import UpdateNodeConfig
import StopBox
import time

V = GlobalVar

def remove_end_line(in_string):
    split_it = in_string.split("\n")
    in_string = "\n".join(split_it[:-1])
    return in_string

def addConfigs():

    def quitClick():
        sys.exit("Program Stopped")

    def confirmClick():
        # This saves and closes the pop up box
        V.global_userstartaddress = enter1.get()
        V.global_usersm = enter2.get()
        V.global_usergtwyaddress = enter3.get()
        V.global_uservrfname = enter4.get()
        root.destroy()

    root = Tk()
    root.title("Network Management Address Info")
    root.geometry("300x300")

    # These are the user input boxes
    enter1 = Entry(root, width=50)
    enter1.pack()
    enter1.insert(0, "Starting IP Address goes here")

    enter2 = Entry(root, width=50)
    enter2.pack()
    enter2.insert(0, "Enter Subnet Mask here")

    enter3 = Entry(root, width=50)
    enter3.pack()
    enter3.insert(0, "Enter in the GTWY IP Address")

    enter4 = Entry(root, width=50)
    enter4.pack()
    enter4.insert(0, "Enter management VRF name")


    myButton1 = Button(root, text="Confirm", command=confirmClick)
    myButton1.pack(side=TOP)

    label6 = Label(root, text="Adds the Configs")
    label6.pack(side=TOP)

    myButton2 = Button(root, text="Quit", command=quitClick)
    myButton2.pack(side=TOP)

    root.mainloop()