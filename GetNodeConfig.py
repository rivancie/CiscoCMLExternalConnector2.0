# Module
# Description: This module pulls the nodes config and stores it for later use.  Then, identifies the type of device
#               and grabs the corresponding template, updates the template with VARs.
import requests
import GlobalVar
import sys

GV = GlobalVar

# This small function removes the last line of any string sent to it
def remove_end_line(in_string):
    split_it = in_string.split("\n")
    in_string = "\n".join(split_it[:-1])
    return in_string


# This function gets the details of the node in globalvar and merges the configurations
def get_node_config(token, url):
    token = 'Bearer' + ' ' + token
    headers = {
        'accept': 'application/json',
        'Authorization': token
    }
    # This section gets the fetched config of the current node/device and stores in global var
    api_call = "/v0/labs/" + GlobalVar.global_labid + "/nodes/" + GlobalVar.global_nodeid + "/config"
    full_url = url + api_call

    GlobalVar.global_node_config = requests.get(full_url, headers=headers, verify=False)

    # This section gets the device type of the current node/device and stores in global var
    api_call = "/v0/labs/" + GlobalVar.global_labid + "/nodes/" + GlobalVar.global_nodeid
    full_url = url + api_call
    response = requests.get(full_url, headers=headers, verify=False)

    if response.status_code == 200:
        node_info = requests.get(full_url, headers=headers, verify=False).json()
        if "data" in node_info:
            node_info = node_info['data']
        node_type = node_info['node_definition']
        GlobalVar.global_node_hostname = node_info['label']
    else:
        node_type = "SKIP"

    # This section looks for the management tag and skips configuring this device
    api_call = "/v0/labs/" + GlobalVar.global_labid + "/nodes/" + GlobalVar.global_nodeid + "/tags"
    full_url = url + api_call
    node_tag = requests.get(full_url, headers=headers, verify=False).json()
    node_tag = str(node_tag)
    if "MANAGEMENT" in node_tag:
        GlobalVar.global_node_type = "SKIP"
        node_type = "SKIP"
    node_type = str(node_type)

    # The following if statements look for various device types and starts to build the updated config
    env_dict = {'ip_addr': GlobalVar.global_node_address,
                'def_gtwy': GV.global_usergtwyaddress,
                'subnet_mask': GV.global_usersm,
                'mgmt_vrf': GV.global_uservrfname,
                'host_name': GV.global_node_hostname,
                'mac_var': GV.global_node_mac
                }
    if "iosxrv9" in node_type:
        GlobalVar.global_node_type = "XR"
        with open('asr9ktemp.cfg') as file:
            config = file.read()
            node_info['configuration'] = remove_end_line(str(node_info['configuration']))
            temp_config = config.format(**env_dict)
            GV.global_node_config = node_info['configuration'] + temp_config
    elif "iosxrv" in node_type:
        GlobalVar.global_node_type = "XR"
        with open('xrtemp.cfg') as file:
            config = file.read()
            temp_config = config.format(**env_dict)
            GV.global_node_config = node_info['configuration'] + temp_config
    elif "iosxrv9" in node_type:
        GlobalVar.global_node_type = "XR"
        with open('asr9ktemp.cfg') as file:
            config = file.read()
            node_info['configuration'] = remove_end_line(str(node_info['configuration']))
            temp_config = config.format(**env_dict)
            GV.global_node_config = node_info['configuration'] + temp_config
    elif "iosvl2" in node_type:
        GlobalVar.global_node_type = "XE"
        with open('xel2temp.cfg') as file:
            config = file.read()
            temp_config = config.format(**env_dict)
            GV.global_node_config = node_info['configuration'] + temp_config
    elif "iosv" in node_type:
        GlobalVar.global_node_type = "XE"
        with open('xetemp.cfg') as file:
            config = file.read()
            temp_config = config.format(**env_dict)
            GV.global_node_config = node_info['configuration'] + temp_config
    elif "csr" in node_type:
        GlobalVar.global_node_type = "XE"
        with open('csrtemp.cfg') as file:
            config = file.read()
            node_info['configuration'] = remove_end_line(str(node_info['configuration']))
            temp_config = config.format(**env_dict)
            GV.global_node_config = node_info['configuration'] + temp_config
    elif "nxosv9" in node_type:
        GlobalVar.global_node_type = "NXOS"
        with open('nx9500temp.cfg') as file:
            config = file.read()
            temp_config = config.format(**env_dict)
            GV.global_node_config = node_info['configuration'] + temp_config
    elif "nxosv" in node_type:
        GlobalVar.global_node_type = "NXOS"
        with open('nxtemp.cfg') as file:
            config = file.read()
            temp_config = config.format(**env_dict)
            GV.global_node_config = node_info['configuration'] + temp_config
    else:
        GlobalVar.global_node_type = "SKIP"
