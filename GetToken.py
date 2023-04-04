# Module
# Description: This module just gets the token for the CML server
#
import json
import requests


def get_token(url, user, password):
	api_call = "/v0/authenticate"
	url += api_call

	headers = {
		'Content-Type': 'application/json',
		'accept': 'application/json'
	}

	payload = {
		"username": user,
		"password": password
	}

	response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False).json()

	if response.status_code == 200:
		print("CML Credentials accepted and working")

	else:
		print(f"Error: Unable to connect to CML Server. Status code: {response.status_code}")
		sys.exit("Program Halted")

	return response