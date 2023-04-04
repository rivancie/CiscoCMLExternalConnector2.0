# Module
# Description: This module puts the newly built config updates to the end of the existing config
#
import requests
import GlobalVar

GV = GlobalVar

def update_node_config(token, url):
    token = 'Bearer' + ' ' + token
    headers = {
        'accept': 'application/json',
        'Authorization': token
    }
    # This section puts the updated config on the device
    api_call = "/v0/labs/" + GlobalVar.global_labid + "/nodes/" + GlobalVar.global_nodeid + "/config"
    full_url = url + api_call

    response = requests.put(full_url, data=GlobalVar.global_node_config, headers=headers, verify=False)
