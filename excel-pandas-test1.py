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
dup_dict = {}
hostnames = []
new_idx_list = []

def duplicate_hosts_list(lst, dct):
    global key_list
    global new_list
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
    def __init__(self, index):
        self.index = index
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
   

def starter():
    root = tk.Tk()
    fr = Frame(root)
    if fr.file:
        dframe1 =  fr.file
        print(dframe1)
    root.mainloop()

if __name__=='__main__':
    
    dframe = pd.read_excel (r'C:\Users\user\Documents\MAIPU - RFC.xlsx')
##    print(dframe)
##    starter()
    pd.set_option('display.max_columns', None)
    pd.set_option('max_colwidth', None)
    pd.set_option('display.max_rows', None)
    pd.set_option("expand_frame_repr", False)
##    print(dframe)
##    sys.exit()
    host_list = dframe.Destination_HostName.sort_values(ascending=True, inplace=False).to_list()
    host_dict = dframe.Destination_HostName.sort_values(ascending=True, inplace=False).to_dict()
    duplicate_hosts_list(host_list, host_dict)                       ## Sort Duplicate Hostnames
    
    while len(new_list)>0:
        duplicate_hosts_list(new_list, host_dict)

    for hostname,idx_list in dup_dict.items():
        print(hostname,idx_list)
        s = Setter()
        for idx in idx_list:
            g = Getter(idx)
            vl = Validator(idx)
            if hostname == 'Cannot resolve hostname':
                if (vl.check_ports(g.dst_port, tcpdenied_ports) == True):
                    s.action_column_setter(dframe, idx, 'Block')
                    new_idx_list.append(idx)
                elif (vl.check_ports(g.dst_port, udpdenied_ports) == True):
                    s.action_column_setter(dframe, idx, 'Block')
                    new_idx_list.append(idx)
                elif (vl.check_hits(g.hit_nmbr, 5) == True):
                    s.action_column_setter(dframe, idx, 'Ignore')
                    new_idx_list.append(idx)
                elif (vl.check_broadcast(g.dst_ip) == True):
                    s.action_column_setter(dframe, idx, 'Ignore')
                    new_idx_list.append(idx)
                else:
                    for subnet in denied_subnets:
                        if vl.check_ip(g.dst_ip, subnet) == True:
                            s.action_column_setter(dframe, idx, 'Block')
                            new_idx_list.append(idx)
                            break
                        else:
                            s.comments_column_setter(dframe, idx, 'UNDEFINED')
            elif (vl.check_hostname(hostname, denied_hosts) == True):
                s.action_column_setter(dframe, idx, 'Block')
                s.comments_column_setter(dframe, idx, 'Traffic to/from this server will be blocked')
                hostnames.append(hostname)
            elif (vl.check_hostname(hostname, allowed_hosts) == True):
                s.action_column_setter(dframe, idx, 'Allow')
                s.comments_column_setter(dframe, idx, 'Allowed but investigate ..')
                hostnames.append(hostname)
            elif (vl.check_hostname(hostname, ignored_hosts) == True):
                s.action_column_setter(dframe, idx, 'Ignore')
                s.comments_column_setter(dframe, idx, 'Traffic to/from this server will be ignored')
                hostnames.append(hostname)
            else:
                if (vl.check_ports(g.dst_port, udpdenied_ports) == True) or (vl.check_ports(g.dst_port, tcpdenied_ports) == True):
                    s.action_column_setter(dframe, idx, 'Block')
                    s.comments_column_setter(dframe, idx, 'Traffic to/from this Port will be blocked')
                    new_idx_list.append(idx)
                elif (vl.check_hits(g.hit_nmbr, 5) == True):
                    s.action_column_setter(dframe, idx, 'Ignore')
                    s.comments_column_setter(dframe, idx, 'Less then 5 hits')
                    new_idx_list.append(idx)
                else:
                    s.action_column_setter(dframe, idx, 'NN')
                    s.comments_column_setter(dframe, idx, '')
                    

print(dframe.sort_values(by=['Action'], ascending=True))
##    final_logfile = input('Please Insert Final Excel Log File  Desired Location ...')
##    dframe.to_excel(final_logfile)


##            if len(idx_list) > len(new_idx_list):
##                idx_set = set(idx_list).difference(set(new_idx_list))
##                idx_list = list(idx_set)
##                dup_dict[hostname] = idx_list
##            else:
##                hostnames.append(hostname)
##    for hostname in hostnames:
##        dup_dict.pop(hostname)
        
   
    

