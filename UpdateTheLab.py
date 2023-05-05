import ipaddress
import GlobalVar
import UpdateNodeConfig
import GetNodeConfig
from tkinter import *

V = GlobalVar

def startLoop():
    # Iterative for each node in the selected lab
    for counter1 in range(int(GlobalVar.global_node_count)):
        #GlobalVar.global_nodeid = ("n" + str(counter1))
        GlobalVar.global_nodeid = V.global_nodeID_list[counter1]
        GlobalVar.global_node_mac = ("0000.0123.0" + str(format(counter1, '03d')))
        GlobalVar.global_node_address = ipaddress.IPv4Address(GlobalVar.global_userstartaddress) + counter1
        GetNodeConfig.get_node_config(V.global_token, V.global_CML_URL)

        if GlobalVar.global_node_type != "SKIP":
            UpdateNodeConfig.update_node_config(V.global_token, V.global_CML_URL)
            #print(GlobalVar.global_node_hostname + "," + str(GlobalVar.global_node_address) + ",Telnet,admin," + GlobalVar.global_title + ",VT100\n")
            GlobalVar.global_secureCRT = GlobalVar.global_secureCRT + (GlobalVar.global_node_hostname + ","
                                                                       + str(GlobalVar.global_node_address)
                                                                       + ",Telnet,admin," + GlobalVar.global_title
                                                                       + ",VT100\n")

    #def display_info():
    top = Tk()
    top.geometry("600x600")
    top.title("SecureCRT Import Data")
    text_box = Text(top, height = 25, width = 80)
    text_box.pack(expand=TRUE)
    text_box.insert(END, GlobalVar.global_secureCRT)
    top.mainloop()