import pandas as pd
import ipaddress
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
import re
import sys
import inspect
from tkinter_pandas_toplevel import Enter_Frame, CheckBox_Frame, Frame, Input_Frame

allowed_hosts = ['ndlg']
denied_hosts = ['lync', 'skp']
ignored_hosts = ['rar7app']
tcpdenied_ports = ['5061', '3389']
udpdenied_ports = ['5100']
most_used_ports = ['80', '443', '389', '139', '445' , '137', '135']
denied_subnets = ["192.168.0.0/24"]

def duplicate_hosts_list(lst, dct):                   ### function for sorting duplicate hostnames
    global key_list
    global new_list
    global dup_dict
    new_list = []
    key_list = []
    for idx,hostname in enumerate(lst):
        if hostname != lst[0]:
            break
        if (idx == len(lst)-1):
            idx = idx + 1
    new_list = lst[(idx):]
    for (key,val) in dct.items():
        if dct[key] == lst[0]:
            key_list.append(key)
    dup_dict[lst[0]] = key_list
    for key in key_list:
        host_dict.pop(key)
    return (new_list, dup_dict)

class Getter():
    def __init__(self, index):
        self.idx = index
        self.row = dframe.iloc[self.idx,:]
        self.dst_ip = self.row.Destination
        self.dst_port = self.row.Port
        self.dst_proto = self.row.Protocol
        self.dst_hostname = self.row.Destination_HostName
        self.hit_nmbr = self.row.Hits
        
class Setter():
    @staticmethod
    def action_column_setter(df, index, action):
        df.at[index, 'Action'] = action
    @staticmethod
    def comments_column_setter(df, index, comment):
        df.at[index, 'Comments'] = comment
     
class Validator():
    def check_ports(self, port, port_list):
        var = port in port_list
        return var
    def check_ip(self, ip, subnet):
        host  = ipaddress.ip_address(ip)
        net = ipaddress.ip_network(subnet)
        var = host in net
        return var
    def check_broadcast(self, ip):
        iface = ipaddress.ip_interface(ip+'/24')
        broadcast = iface.network.broadcast_address
        var = ip in broadcast.exploded
        return var
    def check_hits(self, hits, hit_nmbr):
        var = (hits <= hit_nmbr)
        return var
    def check_hostname(self, hostname, host_list):
        for pattern in host_list:
            var = bool(re.search(pattern, hostname))
            if var == True:
                break
        return var


if __name__ == "__main__":
    root = tk.Tk()
    fr = Frame(root)
    root.mainloop()
    
    pd.set_option('display.max_columns', None)
    pd.set_option('max_colwidth', None)
    pd.set_option('display.max_rows', None)
    pd.set_option("expand_frame_repr", False)
    print(dframe)
    host_list = dframe.Destination_HostName.sort_values(ascending=True, inplace=False).to_list()
    host_dict = dframe.Destination_HostName.sort_values(ascending=True, inplace=False).to_dict()
    
    duplicate_hosts_list(host_list, host_dict)                      ### Sort Duplicate Hostnames
    while len(new_list)>0:
        duplicate_hosts_list(new_list, host_dict)                   ### Create final dict with duplicate hostnemes
        
    for hostname,idx_list in dup_dict.items():
        s = Setter()
        vl = Validator()
        if (vl.check_hostname(hostname, denied_hosts) == True):
            for idx in idx_list:
                g = Getter(idx)
                s.action_column_setter(dframe, idx, 'Block')
                s.comments_column_setter(dframe, idx, 'Traffic to/from this server will be blocked')
        elif (vl.check_hostname(hostname, allowed_hosts) == True):
            for idx in idx_list:
                g = Getter(idx)
                s.action_column_setter(dframe, idx, 'Allow')
                s.comments_column_setter(dframe, idx, 'Allowed but investigate ..')
        elif (vl.check_hostname(hostname, ignored_hosts) == True):
            for idx in idx_list:
                g = Getter(idx)
                s.action_column_setter(dframe, idx, 'Ignore')
                s.comments_column_setter(dframe, idx, 'Traffic to/from this server will be ignored')
        else:
            for idx in idx_list:
                g = Getter(idx)
                if (vl.check_ports(g.dst_port, tcpdenied_ports) == True):
                    s.action_column_setter(dframe, idx, 'Block')
                    s.comments_column_setter(dframe, idx, 'Denied Destination Port')
                elif (vl.check_ports(g.dst_port, udpdenied_ports) == True):
                    s.action_column_setter(dframe, idx, 'Block')
                    s.comments_column_setter(dframe, idx, 'Denied Destination Port')
                elif (vl.check_hits(g.hit_nmbr, 5) == True):
                    s.action_column_setter(dframe, idx, 'Ignore')
                    s.comments_column_setter(dframe, idx, 'Less then 5 hits')
                elif (vl.check_broadcast(g.dst_ip) == True):
                    s.action_column_setter(dframe, idx, 'Ignore')
                    s.comments_column_setter(dframe, idx, 'Broadcast IP Address')
                else:
                    for subnet in denied_subnets:
                        if vl.check_ip(g.dst_ip, subnet) == True:
                            s.action_column_setter(dframe, idx, 'Block')
                            s.comments_column_setter(dframe, idx, 'Bad subnet')
                        else:
                            s.comments_column_setter(dframe, idx, 'UNDEFINED')

    print(dframe.sort_values(by=['Action'], ascending=True))
##    final_logfile = input('Please Insert Final Excel Log File  Desired Location ...')
##    dframe.to_excel(final_logfile)



    

