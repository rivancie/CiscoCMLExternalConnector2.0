# Module
# Description: This module gets the number of labs running
#
import requests

def get_labs(token, url, labname):
	api_call = "/v0/labs"
	url += api_call
	token = 'Bearer' + ' ' + token

	headers = {
		'accept': 'application/json',
		'Authorization': token
	}

	response = requests.get(url, headers=headers, verify=False).json()
	# print("#" + " " + "Simulated labs on CML" + ": " + str(len(response)) + " at " + labname)
	return response
