# This module provides a popup for additional user input. 2 new devices will be added to the running lab.
# The external cloud connector object and the management switch.  This also adds the management links to
# all devices in the lab.
import tkinter
import GlobalVar
import requests
import json
from tkinter import *
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


def addManagement():

    def confirmClick():
        print("made it past")
        V.global_mgmt_type = clicked1.get()
        V.global_vlanID = enter2.get()
        V.global_bridge = enter1.get()

        # This section below gets the lab node count from the user input
        token = 'Bearer' + ' ' + V.global_token
        headers = {
            'accept': 'application/json',
            'Authorization': token
        }

        # This section prepares the management portion
        api_call = "/v0/labs/" + GlobalVar.global_labid
        full_url = V.global_CML_URL + api_call
        response = requests.get(full_url, headers=headers, verify=False).json()
        GlobalVar.global_node_count = str(response['node_count'])

        # Add the Management Switch and external Cloud objects
        switch_payload = {
                            "label": "ExtSwitch",
                            "node_definition": "nxosv",
                            "x": 0,
                            "y": 0,
                        }
        switch_payload2 = {
                            "tags": [
                              "MANAGEMENT"
                            ]
                        }
        cloud_payload = {
                      "x": 40,
                      "y": 40,
                      "label": "OutSide-Cloud",
                      "node_definition": "external_connector",
                    }
        cloud_payload2 = {
                      "configuration": V.global_bridge,
                      "tags": [
                        "MANAGEMENT"
                      ]
                    }
        full_url = full_url + "/nodes"
        response1 = requests.post(full_url, headers=headers, data=json.dumps(cloud_payload), verify=False)

        if response1.status_code == 200:
            print(f"Cloud Device added successfully to CML lab '{V.global_labid}.")
            #These statements below get the node id that was just created and updates the node
            V.global_cloud_node = json.loads(response1.content)
            full_url2 = full_url + "/"
            full_url2 = f"{full_url2}{V.global_cloud_node['id']}"
            response12 = requests.patch(full_url2, headers=headers, data=json.dumps(cloud_payload2), verify=False)

        else:
            print(f"Error: Unable to add device to CML. Status code: {response1.status_code}")

        #This section adds the mgmt switch and updates the config
        response2 = requests.post(full_url, headers=headers, data=json.dumps(switch_payload), verify=False)
        if response2.status_code == 200:
            print(f"Mgmt Switch added successfully to CML lab '{V.global_labid}.")
            #These statements update the mgmt switch node
            V.global_mgmtswitch_node = json.loads(response2.content)
            full_url3 = full_url + "/"
            full_url3 = f"{full_url3}{V.global_mgmtswitch_node['id']}"
            response21 = requests.patch(full_url3, headers=headers, data=json.dumps(switch_payload2), verify=False)

            env_dict = {'mgmt_vlan': V.global_vlanID,
                        'mgmt_mode': V.global_mgmt_type
                        }
            with open('nxos_mgmt_template.cfg') as file:
                config = file.read()
                config = remove_end_line(config)
                temp_config = config.format(**env_dict)
                V.global_nodeid = V.global_mgmtswitch_node['id']
                V.global_node_config = temp_config
                UpdateNodeConfig.update_node_config(V.global_token, V.global_CML_URL)
        else:
            print(f"Error: Unable to add device to CML. Status code: {response2.status_code}")

        #Create Interfaces on Mgmt Switch
        V.global_add_int_info['node'] = V.global_mgmtswitch_node['id']
        V.global_add_int_info['slot'] = 31
        addint_url = V.global_CML_URL + api_call + '/interfaces'
        response3 = requests.post(addint_url, headers=headers, data=json.dumps(V.global_add_int_info), verify=False)
        V.global_mgmtswitch_node['interfaces'] = json.loads(response3.content)

        #Create Interface on Cloud
        V.global_add_int_info['node'] = V.global_cloud_node['id']
        V.global_add_int_info['slot'] = 0
        response31 = requests.post(addint_url, headers=headers, data=json.dumps(V.global_add_int_info), verify=False)
        V.global_cloud_node['interfaces'] = json.loads(response31.content)

        #Create the link between the mgmt switch and cloud
        addlink_url = V.global_CML_URL + api_call + '/links'
        V.global_linkem['src_int'] = V.global_cloud_node['interfaces'][0]['id']
        V.global_linkem['dst_int'] = V.global_mgmtswitch_node['interfaces'][31]['id']
        response4 = requests.post(addlink_url, headers=headers, data=json.dumps(V.global_linkem), verify=False)

        #Create links to all devices
        for counter1 in range(int(GlobalVar.global_node_count)):
            #Ensures the 8th port of the device is created
            V.global_add_int_info['node'] = ("n" + str(counter1))
            V.global_add_int_info['slot'] = 8
            response5 = requests.post(addint_url, headers=headers, data=json.dumps(V.global_add_int_info), verify=False)
            V.global_add_int_info['interfaces'] = json.loads(response5.content)

            #Connects the current node to the mgmt switch
            V.global_linkem['src_int'] = V.global_add_int_info['interfaces'][8]['id']
            V.global_linkem['dst_int'] = V.global_mgmtswitch_node['interfaces'][counter1+1]['id']
            response51 = requests.post(addlink_url, headers=headers, data=json.dumps(V.global_linkem), verify=False)
        print(f"{counter1+1} Mgmt connections made successfully")

        root.destroy()

    root = Tk()
    root.title("Adding Management Switch and Connections")
    root.geometry("300x300")

    label1 = Label(root, text="External Bridge Name for the Cloud")
    label1.pack(side=TOP)
    enter1 = Entry(root, width=20)
    enter1.pack(side=TOP)
    enter1.insert(0, V.global_bridge)

    label2 = Label(root, text="VLAN ID if required - default is 1")
    label2.pack(side=TOP)
    enter2 = Entry(root, width=20)
    enter2.pack(side=TOP)
    enter2.insert(0, V.global_vlanID)

    # NED drop-down
    label4 = Label(root, text="Set Bridge out as trunk or access")
    label4.pack(side=TOP)

    clicked1 = StringVar(root)
    clicked1.set("Select external Type")

    # Create Dropdown menu
    drop1 = OptionMenu(root, clicked1, *V.global_list_connection)
    drop1.pack(side=TOP)

    myButton1 = Button(root, text="Confirm", command=confirmClick)
    myButton1.pack(side=TOP)

    root.mainloop()