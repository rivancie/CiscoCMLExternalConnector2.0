# Module
# Description: This module loops through the number of labs and puts info into a list
#
import requests
import GlobalVar

def get_labsdetail(token, url, labids):
    token = 'Bearer' + ' ' + token
    headers = {
        'accept': 'application/json',
        'Authorization': token
    }

    for labid in labids:
        api_call = "/v0/labs/" + labid
        laburl = url + api_call
        guiurl = url.rstrip('api')
        guiurl = guiurl + "lab/" + labid

        response = requests.get(laburl, headers=headers, verify=False).json()
        title_and_id = str(response['lab_title']) + " ID:" + labid
        # print(str(response['lab_title']))
        GlobalVar.global_lab_list.append(str(title_and_id))
        # print("{0:42}{1:22}{2:18}{3:18}".
        #      format(str(title_and_id), str(response['created']), str(response['state']), str(guiurl)))

