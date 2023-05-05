import tkinter
import GlobalVar
import requests
import json
import time
from tkinter import *
import tkinter.font as font
import sys

V = GlobalVar

# Beginning of tKinter pop up box for YES NO stopping the lab
def stop_box():

    def yesstop_lab():
        V.global_on_off = "Y"
        root2.destroy()


    def nostop_lab():
        V.global_on_off = "N"
        root2.destroy()

    root2 = Tk()
    root2.title("Running lab detected!")
    root2.geometry("300x100")
    message = "Running lab has been detected, do you want me to shut this lab down?"
    text_box = Text(root2, height=2, width=70)
    text_box.pack(expand=TRUE)
    text_box.insert(END, message)

    button_font = font.Font(size=10, weight="bold")
    myButton1 = Button(root2, text="YES", command=yesstop_lab)
    myButton1['font'] = button_font
    myButton1.pack()

    myButton2 = Button(root2, text="NO", command=nostop_lab)
    myButton2['font'] = button_font
    myButton2.pack()

    tkinter.mainloop()

def stop_lab():
    api_call = "/v0/labs/" + V.global_labid + "/stop"
    full_url = V.global_CML_URL + api_call
    token = 'Bearer' + ' ' + V.global_token
    headers = {
        'accept': 'application/json',
        'Authorization': token
    }
    response = requests.put(full_url, headers=headers, verify=False)
    time.sleep(3)

def wipe_lab():
    api_call = "/v0/labs/" + GlobalVar.global_labid + "/wipe"
    wipe_url = V.global_CML_URL + api_call
    token = 'Bearer' + ' ' + V.global_token
    headers = {
        'accept': 'application/json',
        'Authorization': token
    }
    response_wipe = requests.put(wipe_url, headers=headers, verify=False)

def check_started():

    # This section checks if the lab status is on, then asks the user if they want this program to stop it
    token = 'Bearer' + ' ' + V.global_token
    headers = {
        'accept': 'application/json',
        'Authorization': token
    }
    url = GlobalVar.global_CML_URL
    api_call = "/v0/labs/" + GlobalVar.global_labid + "/state"
    full_url = url + api_call
    response = requests.get(full_url, headers=headers, verify=False).json()
    if response == "STARTED":
        stop_box()
        print("here 2")
        if (V.global_on_off == "Y") or (V.global_on_off == "y"):
            stop_lab()
        else:
            sys.exit("Program Stopped")

    wipe_lab()