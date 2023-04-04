# Module
# Description: This module does a lot of lifting.  Provides a basic user GUI for input
#               then checks the the selected lab to see if its actively running.

import time
import tkinter
from idlelib import window
from tkinter import Checkbutton
import AddExternalNetwork
import requests
import GlobalVar
import sys
from tkinter import *
import tkinter.font as font

import UpdateTheLab

g = GlobalVar


# Beginning of tKinter user pop up box
def input_box():
    def myClick():
        # This function gets the user input items and stores them in the global vars and prints results to the user
        g.global_userstartaddress = enter1.get()
        g.global_usersm = enter2.get()
        temp_it = clicked.get()
        g.global_labid = temp_it[-6:]
        g.global_usergtwyaddress = enter3.get()
        g.global_uservrfname = enter4.get()
        myLabel = Label(root, text="This is the starting point: " + g.global_userstartaddress)
        myLabel.pack()
        myLabel = Label(root, text="This is the SM: " + g.global_usersm)
        myLabel.pack()
        myLabel = Label(root, text="This is the GTWY: " + g.global_usergtwyaddress)
        myLabel.pack()
        myLabel = Label(root, text="This is the VRF name: " + g.global_uservrfname)
        myLabel.pack()
        myLabel = Label(root, text="This is the labID: " + g.global_labid)
        myLabel.pack()

    def doneClick():
        # This saves and closes the pop up box
        g.global_userstartaddress = enter1.get()
        g.global_usersm = enter2.get()
        temp_it = clicked.get()
        g.global_labid = temp_it[-6:]
        g.global_usergtwyaddress = enter3.get()
        g.global_uservrfname = enter4.get()
        root.destroy()

    def checkedBox():
        temp_it = clicked.get()
        g.global_labid = temp_it[-6:]
        AddExternalNetwork.addManagement()

    def quitButton():
        sys.exit("Program Stopped")

    # This creates the gui object
    root = Tk()
    root.title("User Input")
    root.geometry("1000x700")
    message = '''
    HowTo Info  *** HEED AND READ ***
            Pre-Requisites
                1. You have already built bridge interfaces on CML mapping to correct external networks
                    - note NAT/PAT cannot be used, bridged mode only
                2. You have updated the CML lab with the correct topology and names on devices
                3. You have added the tag "MANAGEMENT" to any/all devices you do not want this script to touch
                4. Make sure you save your configs inside CML e.g. "fetch from device" or configs will be removed
                5. Devices Supported: IOSv, IOSl2, CSR, ASR9k, XRv, NXOS & NXOS9000; nothing else at this time
                6. You have already built your external network/Vlan to assign the addressing pool
            What it Does
                1. User pop-up box for input of key variables -- NOTE this must be accurate
                2. Select the correct lab -- the lab will be shutdown and wiped in order to update
                3. The program will stop the lab if running, wipe all nodes, append the management configs per the templates
                    and display the SecureCRT import statements
                4. Each device type has a separate config template which implements in slot 9 of all devices - CAREFUL
                5. Once complete the lab will remain off
                6. Remote access to devices will be telnet at this point as RSA key pairs are not created in this program
                7. (optional) Check the box if you want this script to automatically add the external management switch
                8. (optional) Add the bridge name you want the script to assign to the cloud connector
                9. (optional) Add the VLAN ID you want the external switch to use - default will not use any VLAN tagging

            Summary - this program basically adds relative management configs to all intended devices for external access
                      outside of CML virtual environment.  This will be useful for adding external services to your labs
                      e.g. DNS, NSO, ISE/TACACs, etc.  This program can automatically add the management switch and 
                      connections if selected.

            Have FUN!!! '''
    text_box = Text(root, width=900)
    text_box.pack(expand=TRUE)
    text_box.insert(END, message)

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

    # initial menu text for drop down
    clicked = StringVar()
    clicked.set("Select Lab Here")

    # Create Dropdown menu
    drop = OptionMenu(root, clicked, *g.global_lab_list)
    drop.pack()

    checkvar1 = tkinter.IntVar
    checkBox1 = tkinter.Checkbutton(root, text="Add Mgmt switch and Connections * Please select the correct lab above", variable=checkvar1, onvalue=1, offvalue=0, command=checkedBox)
    checkBox1.pack()

    button_font = font.Font(size=10, weight="bold")
    myButton1 = Button(root, text="Confirm Changes", command=myClick)
    myButton1.pack()

    myButton2 = Button(root, text="Execute", width=10, height= 5, command=doneClick)
    myButton2['font'] = button_font
    myButton2.pack(side="left")

    #myButton3 = Button(root, text="QUIT", width=10, height= 5, command=root.destroy)
    myButton3 = Button(root, text="QUIT", width=10, height= 5, command=quitButton)

    myButton3['font'] = button_font
    myButton3.pack(side="right")

    tkinter.mainloop()

# Beginning of tKinter pop up box for YES NO stopping the lab
def stop_box():

    def stop_lab():
        g.global_on_off = "Y"
        root.destroy()

    def nostop_lab():
        g.global_on_off = "N"
        root.destroy()

    root = Tk()
    root.title("Running lab detected!")
    root.geometry("300x100")
    message = "Running lab has been detected, do you want me to shut this lab down?"
    text_box = Text(root, height=2, width=70)
    text_box.pack(expand=TRUE)
    text_box.insert(END, message)

    button_font = font.Font(size=10, weight="bold")
    myButton1 = Button(root, text="YES", command=stop_lab)
    myButton1['font'] = button_font
    myButton1.pack()

    myButton2 = Button(root, text="NO", command=nostop_lab)
    myButton2['font'] = button_font
    myButton2.pack()

    tkinter.mainloop()

def get_user_input(token, url, CML_USER, CML_PASS):
    input_box()

    # This section below gets the lab name from the user input
    token = 'Bearer' + ' ' + token
    headers = {
        'accept': 'application/json',
        'Authorization': token
    }
    api_call = "/v0/labs/" + GlobalVar.global_labid
    laburl = url + api_call
    guiurl = url.rstrip('api')
    guiurl = guiurl + "lab/" + GlobalVar.global_labid

    response = requests.get(laburl, headers=headers, verify=False).json()
    GlobalVar.global_title = str(response['lab_title'])

    # This section gets the number of nodes and saves as global var
    api_call = "/v0/labs/" + GlobalVar.global_labid
    full_url = url + api_call
    response = requests.get(full_url, headers=headers, verify=False).json()
    GlobalVar.global_node_count = str(response['node_count'])

    # This section checks if the lab status is on, then asks the user if they want this program to stop it
    api_call = "/v0/labs/" + GlobalVar.global_labid + "/state"
    full_url = url + api_call
    response = requests.get(full_url, headers=headers, verify=False).json()
    if response == "STARTED":
        stop_box()

        if (g.global_on_off == "Y") or (g.global_on_off == "y"):
            api_call = "/v0/labs/" + GlobalVar.global_labid + "/stop"
            full_url = url + api_call
            response = requests.put(full_url, headers=headers, verify=False)
            time.sleep(3)
        else:
            sys.exit("Program Stopped")

    api_call = "/v0/labs/" + GlobalVar.global_labid + "/wipe"
    wipe_url = url + api_call
    response_wipe = requests.put(wipe_url, headers=headers, verify=False)
    UpdateTheLab.startLoop()
