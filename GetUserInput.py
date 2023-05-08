# Module
# Description: This module does a lot of lifting.  Provides a basic user GUI for input
#               then checks the selected lab to see if it's actively running.

import tkinter
import AddExternalNetwork
import requests
import GlobalVar
import sys
from tkinter import *
import tkinter.font as font
import StopBox
import UpdateTheLab
import re
import ipaddress
import AddExternalConfigs
g = GlobalVar


# Make a regular expression
# for validating an Ip-address
regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''

# Define a function for
# validate an Ip address


def check(Ip):
    # pass the regular expression
    # and the string in search() method
    if(re.search(regex, Ip)):
        g.global_valid = True
    else:
        g.global_valid = False


def input_box():
    # Beginning of tKinter user pop up box

    def doneClick():
        # This saves and closes the pop-up box
        temp_it = clicked.get()
        temper = temp_it.split("ID:", 1)
        g.global_labid = temper[1]
        root.destroy()

    def checkedBox1():
        temp_it = clicked.get()
        temper = temp_it.split("ID:", 1)
        g.global_labid = temper[1]
        g.global_addExternal = not g.global_addExternal

    def checkedBox2():
        temp_it = clicked.get()
        temper = temp_it.split("ID:", 1)
        g.global_labid = temper[1]
        g.global_addConfig = True

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
                1. User pop-up box for CML Credentials
                2. Main dashboard will prompt user for lab selection
                3. Optional Check boxes for user; layer in management devices and interfaces and/or add management 
                   configurations -- both can be completed
                4. Each device type has a separate config template which implements in slot 8 of all devices - CAREFUL
                5. If the selected lab is running, user prompt for shutting down the lab to make the changes requested
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

    # initial menu text for drop down
    clicked = StringVar()
    clicked.set("Select Lab Here")

    # Create Dropdown menu
    drop = OptionMenu(root, clicked, *g.global_lab_list)
    drop.pack()

    checkvar1 = tkinter.IntVar
    checkBox1 = tkinter.Checkbutton(root, text="Optional - Add Mgmt switch and Connections to the lab selected above", variable=checkvar1, onvalue=1, offvalue=0, command=checkedBox1)
    checkBox1.pack()

    checkvar2 = tkinter.IntVar
    checkBox2 = tkinter.Checkbutton(root, text="Optional - Add Mgmt Configurations to the lab selected above", variable=checkvar2, onvalue=1, offvalue=0, command=checkedBox2)
    checkBox2.pack()

    button_font = font.Font(size=10, weight="bold")

    myButton2 = Button(root, text="Execute", width=10, height= 5, command=doneClick)
    myButton2['font'] = button_font
    myButton2.pack(side="left")

    myButton3 = Button(root, text="QUIT", width=10, height= 5, command=quitButton)
    myButton3['font'] = button_font
    myButton3.pack(side="right")

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

    #This section gets the NodeIDs and stores them as a list
    node_url = url + api_call + "/nodes"
    response2 = requests.get(node_url, headers=headers, verify=False).json()
    GlobalVar.global_nodeID_list = response2

    #This checks the CML version running and sets the var for old or new
    version_url = url + "/v0/system_information"
    response3 = requests.get(version_url, headers=headers, verify=False).json()
    GlobalVar.global_version = response3['version']
    if "2.2" in GlobalVar.global_version or "2.3" in GlobalVar.global_version:
        GlobalVar.global_old = True
        GlobalVar.global_mgmtswitch_node['node_definition'] = "nxosv"
        GlobalVar.global_mgmt_node_num = "2"
        print("OLD version")
    elif "2.4" in GlobalVar.global_version or "2.5" in GlobalVar.global_version:
        GlobalVar.global_old = False
        GlobalVar.global_mgmtswitch_node['node_definition'] = "nxosv9000"
        GlobalVar.global_mgmt_node_num = "1"
        print("NEW version")

    #This checks to see if the lab is running and asks the user if they want to stop the lab
    StopBox.check_started()

    #This section runs the functions if the check boxes were checked by the user
    if g.global_addExternal:
        AddExternalNetwork.addManagement()
    if g.global_addConfig:
        AddExternalConfigs.addConfigs()
        UpdateTheLab.startLoop()
