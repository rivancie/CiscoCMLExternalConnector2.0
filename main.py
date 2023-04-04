# Program: CML External Management Installer
# Date: 5/3/2022
# By: Rob Ivancie
# RPC Method: HTTP Requests
# Description: This program implements external mgmt addresses on all device nodes
#              running in a specified CML lab using pre-determined interfaces
#              connecting to an external switch via a bridge cloud in CML.
#              This ultimately allows the CML nodes to access external services.
# Updated: 11/7/2022 - added new xel2 template and code to differentiate between IOSv and IOSvl2 platforms
# Updated: 4/3/2023 - added a new feature to automatically add the management switch and cloud
#                       this update still requires the user to pre-configure their external mgmt network and
#                       any/all CML VM NIC additions with CentOS bridge updates.
#
import urllib3
import CMLinfo
import GetInfo
import GetLabs
import GetLabsDetail
import GetToken
import GetUserInput
import GlobalVar

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



labname = "CML Lab " + CMLinfo.CML["host"]

if __name__ == "__main__":
    GetInfo.info()
    CML_URL = "https://" + CMLinfo.CML["host"] + "/api"
    GlobalVar.global_CML_URL = CML_URL
    CML_USER = CMLinfo.CML["username"]
    CML_PASS = CMLinfo.CML["password"]
    auth_token = GetToken.get_token(CML_URL, CML_USER, CML_PASS)
    GlobalVar.global_token = auth_token
    print("#" * 113)
    labids = GetLabs.get_labs(auth_token, CML_URL, labname)
    print("#" * 113)
    GetLabsDetail.get_labsdetail(auth_token, CML_URL, labids)
    print("#" * 113)
    GetUserInput.get_user_input(auth_token, CML_URL, CML_USER, CML_PASS)
    print("#" * 113)

