
#############################################################################
# This code was created to sort Tufin Log File which is generated
# by Tufin application based on Firewall traffic monitoring.
#
# Two columns were added to the original Tufin's log file.
# Column names are: "Comment" and "Action". The result of "Action" column
# is set after code execution and depends on global variables
# which are defined manually (all variables are stored separetly using JSON) 
# or alternatevly could be created and added during code execution.
# Three possible results of "Action" column calculation are:
# "Allow", "Block" or "Ignore".
#
# "Comments" column is optional and can be easily ommited or
# modified due to code modular structure and free access to
# code source itself.
#
# Due to code modularity the creation of new columns within original log file
# does not impact script execution. New column's data is easily accessed
# and any manipulations are possible via adding corresponding function to
# the appropriate Project Class.
#
# This script is packed into Python package. It can be executed on Windows
# or Linux OS.
# Jaml variables dictionaries are created and saved automatically (optional) .. #
# The graphycal interface is created by Tkinter module and has full             #
# interaction with the rest of the script.                                      #
# All rights reserved to ELIL                                                   #
#################################################################################

import pandas as pd
import ipaddress
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
import re
import os.path
import platform
import sys
import pdb
import yaml
from config.definitions import ROOT_DIR, yaml_file, result_file


allowed_hosts = ['ndlg', 'dpfwslba', 'emp', 'limsx', 'fs', 'web-ie11']
denied_hosts = ['lync', 'skp', 'epo', 'lexc', 'skp', 'evg', 'nowev']
ignored_hosts = ['rar7', 'rap7', 'nlm', 'dc']
tcpdenied_ports = ['5061', '3389',]
udpdenied_ports = ['5100']
denied_subnets = ['192.168.0.0/24']


class Frame(ttk.Frame):                                                                                   ## Main Frame Class Definition   
    def __init__(self, master):
        super().__init__(master)
        self.master.title('GUI Application')
        self.master.geometry('300x100')
        self.master.resizable(True,True)
        self.label = ttk.Label(self, text='Press Submit Button To Start Application', font=("Courier", 13))
        self.label.grid(row =2, columnspan=2, padx=10, pady=(20,5) )
        self.exit_button = ttk.Button(self, text='Exit', command=self.master.destroy)
        self.exit_button.grid(row=5, column=1, padx=1, pady=(12,5), sticky='e')
        self.submit_button = ttk.Button(self, text='Submit', command=self.submit)
        self.submit_button.grid(row=5, column=0, padx=15, pady=(12,5), sticky='w')
        self.master.bind('<Return>', self.submit)
        self.master.bind('<Escape>', self.close)
        self.focus_force()
        self.grid()
   
    def center_window(self, width, height):
        # get screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.master.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def submit(self, event=None):
        self.master.withdraw()
        ef = Enter_Frame(self)
        ef.protocol("WM_DELETE_WINDOW", self.master.destroy)

    def close(self, event):
        self.master.destroy()
        sys.exit()

class Enter_Frame(tk.Toplevel):
    def __init__(self, master):
        super().__init__()
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        self.geometry("+%d+%d" % (x + 100, y + 200))
        self.title('Log file path Entry Frame')
        self._path = None
        self._filepath = None 
        self.filepath_var = tk.StringVar()
        self.input_entry = ttk.Entry(self, textvariable=self.filepath_var, width=45)
        self.input_entry.grid(row=3, columnspan=2, padx=15,pady=(2,7))
        self.input_entry.insert(0, "Input Log File path")
        self.error_label = ttk.Label(self, text=None, font=("Courier", 13))
        self.error_label.configure(foreground="red")
        self.clear_button = ttk.Button(self, text='Clear', command=self.clear_entry)
        self.clear_button.grid(row=7, column=1, padx=5, pady=(12,5), sticky='w')
        self.submit_button = ttk.Button(self, text='Submit', command=self.submit)
        self.submit_button.grid(row=7, column=0, padx=5, pady=(12,5), sticky='e')
        self.clicked = self.input_entry.bind('<Button-1>', self.click)                                                 ## Bind the Entry widget with Mouse Button to clear the content
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.bind('<Return>', self.submit)
        self.bind('<Escape>', self.close)
        self.bind('c', self.clear_entry)
        self.focus_force()
        
    def click(self, event):                                                                                            ## Define a function to clear the content of the text widget
        self.input_entry.delete(0, 'end')
        self.input_entry.unbind('<Button-1>', self.clicked)
           
    def clear_entry(self, event):
        self.input_entry.delete(0, 'end')
        self.error_label.grid_forget()
        self.input_entry.insert(0, "Input Log File path")
        self.clicked = self.input_entry.bind('<Button-1>', self.click)     
           
    def submit(self, event=None):
        self.read_input()
        self.filepath_validation()
        self.dframe_create                                                                              
        self.after(1000, self.chain_foo)

    def read_input(self):
        self._path = self.filepath_var.get()
        return self._path
    
    def filepath_validation(self):
        if  not self._path:
            self.error_label.config(text='Empty Input')
            self.error_label.grid(row=4, columnspan=2, pady=(2,7))
        elif os.path.isabs(self._path) == False:
            self.error_label.config(text='Invalid Input')
            self.error_label.grid(row=4, columnspan=2, pady=(2,7))
        elif os.path.isfile(self._path) == False:
            self.error_label.config(text='File Not Found')
            self.error_label.grid(row=4, columnspan=2, pady=(2,7))
##        elif os.path.splitext(self._path)[1] == '.csv':
##            self.error_label.config(text='Csv file format cannot be determined, input correct filepath')
##            self.error_label.grid(row=4, columnspan=2, pady=(2,7))
##            print(self._path)
        elif os.path.splitext(self._path)[1] != '.xlsx':
            self.error_label.config(text='Excel file format cannot be determined, input correct filepath')
            self.error_label.grid(row=4, columnspan=2, pady=(2,7))
        else:
             self.error_label.config(text='Input Excepted')
             self.error_label.grid(row=4, columnspan=2, pady=(2,7))
             self.error_label.configure(foreground="green")
             self.after(800, self.withdraw)
             self._filepath = self._path
             return  self._filepath
        
    @property
    def dframe_create(self):
        global dframe
        global source_file
        source_file = None
        try:
            if self._filepath:
                source_file = self._filepath 
                dframe = pd.read_excel(source_file)
                return dframe, source_file
        except ValueError as error:
            messagebox.showerror(message=error)
            self.close()
                      
    def chain_foo(self):
        if source_file :
            result = messagebox.askyesno(message="Add new variables ?")
            if result == True:
                self.checkbox_strater()
            elif result == False:
                self.master.destroy()
                       
    def checkbox_strater(self):
        ch = CheckBox_Frame(self, ['allowed_hosts', 'denied_hosts', 'ignored_hosts', 'tcpdenied_ports', 'udpdenied_ports'])

    def close(self, event=None):
        self.master.deiconify()
        self.destroy()
        sys.exit()
        
                   
class Input_Frame(tk.Tk):
    def __init__(self, text_var):
        super().__init__()
##        self._checkbox_dict = None
##        self.yaml_file = os.path.join(ROOT_DIR, 'data', 'variables.yaml')
        self.text_var = text_var
        self.title('Variables Entry Widget')
        self._input = tk.StringVar()
        self._input_value = None
        self.text= "Input new " + self.text_var
        self.input_entry = ttk.Entry(self, textvariable=self._input, width=50)
        self.input_entry.grid(row=2, columnspan=2, padx=5,pady=(2,7))
        self.input_entry.insert(0, self.text)
        self.clear_button = ttk.Button(self, text='Clear', command=self.clear_entry)
        self.clear_button.grid(row=5, column=1, padx=5, pady=(12,5), sticky='w')
        self.submit_button = ttk.Button(self, text='Submit', command=self.submit)
        self.submit_button.grid(row=5, column=0, padx=5, pady=(12,5), sticky='e')
        self.error_label = ttk.Label(self, text=None, font=("Courier", 13))
        self.error_label.configure(foreground="red")
        self.error_label.grid(row=3, columnspan=2, pady=(2,7))
        self.clicked = self.input_entry.bind('<Button-1>', self.click)          ##bind the "Entry Widget" with mouse click
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.bind('<Return>', self.submit)
        self.bind('<Escape>', self.close)
        self.focus_force()
        
    def click(self, event):                                      ##define a function to clear the content of the text widget
        self.input_entry.delete(0, 'end')
        self.input_entry.unbind('<Button-1>', self.clicked)
          
    def clear_entry(self):                                                                        ##handle mouse click event
        self.input_entry.delete(0, 'end') 
        self.error_label.grid_forget()
        self.input_entry.insert(0, self.text)
        self.clicked = self.input_entry.bind('<Button-1>', self.click)     

    def submit(self, event=None):
        global yaml_dict
##        self._input_value = self._input.get()
        self.read_input()
        yp = Yaml_Parser(yaml_file)
        yp.loader(yaml_file)
        yaml_dict = yp.data
        if 'host' in  self.text_var:
            self.host_checker(self._input_value)
        elif 'port' in  self.text_var:
            self.port_checker(self._input_value)
        yp.dumper(yaml_file, yaml_dict)

        
    def read_input(self):
        self._input_value = self._input.get()
        if not self._input_value:
            self.error_label.config(text='Empty Input')
            self.error_label.grid(row=3, columnspan=2, pady=(2,7))
        
        
    
    def port_checker(self, input_data):
        _port_list = list(dict.fromkeys([value.strip() for value in input_data.split(',') if not value.isspace()]))
        for port in _port_list:
            if port.isnumeric() == False:
                self.error_label.config(text=port+ ' - Is Invalid Port Value')
                self.error_label.grid(row=3, columnspan=2, pady=(2,7))
                break
        else:
            self.error_label.config(text='Input Excepted')
            self.error_label.configure(foreground='green')
            self.error_label.grid(row=3, columnspan=2, pady=(2,7))
            return _port_list
##        
##            if string in yaml_dict.keys():
##                yaml_dict[string].extend(_port_list)
##            else:
##                yaml_dict[string] = _port_list
##            self.destroy()
##            return yaml_dict
            
    def host_checker(self, input_data):
        _host_list = list(dict.fromkeys([value.strip() for value in input_data.split(',') if not value.isspace()]))
        for host in _host_list:
            if host.isnumeric() == True:
                self.error_label.config(text=host+' - Is Invalid Host Name')
                self.error_label.grid(row=3, columnspan=2, pady=(2,7))
                break
        else:
            self.error_label.config(text='Input Excepted')
            self.error_label.configure(foreground='green')
            self.error_label.grid(row=3, columnspan=2, pady=(2,7))
            return _host_list
##        
##            if string in yaml_dict.keys():
##                yaml_dict[string].extend(_host_list)
##            else:
##                yaml_dict[string] = _host_list
##            self.destroy()
##            return yaml_dict
                
    def close(self, event=None):
        self.destroy()
        
class Yaml_Parser():
    def __init__(self, file_path):
        self.file_path = file_path
        self.allowed_hosts = None
        self.denied_hosts = None
        self.ignored_hosts = None
        self.tcpdenied_ports = None
        self.udpdenied_ports = None
        self.denied_subnets = None
        self.data = None
        self.loader(self.file_path)
        
    def loader(self, file_path):
        with open(file_path, 'a+') as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)
        print(self.data)
        if not self.data:
            self.data = {}
        return self.data
    
    def data_reader(self):
        try:
            self.allowed_hosts = self.data.get('allowed_hosts')
        except KeyError as error:
            self.allowed_hosts = None
    
        try:
            self.denied_hosts = self.data.get('denied_hosts')
        except KeyError as error:
            self.denied_hosts = None
    
        try:
            self.ignored_hosts = self.data.get('ignored_hosts')
        except KeyError as error:
            self.ignored_hosts = None
    
        try:
            self.tcpdenied_ports = self.data.get('tcpdenied_ports')
        except KeyError as error:
            self.tcpdenied_ports = None

        try:
            self.udpdenied_ports = self.data.get('udpdenied_ports')
        except KeyError as error:
            self.udpdenied_ports = None
        return (self.udpdenied_ports, self.udpdenied_ports, self.allowed_hosts, self.denied_hosts, self.ignored_hosts)

        
    
      
        
    def dumper(self, file_path, data):
        with open(file_path, 'w') as file:
            yaml.dump(data, file)
                  
class CheckBox_Frame(tk.Toplevel):
    def __init__(self, master, checkbars=[]):
##        global checkbox_dict
##        checkbox_dict = {}
        super().__init__()
        self.checkbars_dict = {}
        self.title('CheckBox Window')
        self.vars = []
        for idx,checkbar in enumerate(checkbars):
            self.checkbars_dict[idx] = checkbar
            self.var = tk.BooleanVar()
            self.ChkBttn = ttk.Checkbutton(self, text=checkbar, width = 40, variable=self.var)
            self.ChkBttn.pack(padx = 5, pady = 5)
            self.vars.append(self.var)
        
        self.submit_button = ttk.Button(self, text='Submit', command=self.submit)
        self.submit_button.pack(padx = 2, pady = 2)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.bind('<Return>', self.submit)
        self.bind('<Escape>', self.close)
        self.focus_force()

    def submit(self, event=None):                                           ## code for "submit button"
        check_list = []
        for idx,item in enumerate(self.vars):
            if item.get() == True:
                check_list.append(self.checkbars_dict[idx])
        self.master.destroy()
        print(check_list)
        for item in check_list:
            self.inputframe_starter(item)
         
    def checked(self, var):                                                 ## what happens when "checkbox" is checked (Optional)
        idx = (check_list).index(var)
        self.var_value_list[idx]=var.get()
        return self.var_value_list
    
    def inputframe_starter(self, string):
        iframe = Input_Frame(string)
        iframe.mainloop()

    def close(self, event=None):
        self.master.destroy()

class Child_Input_Frame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        self.master.geometry("+%d+%d" % (x + 100, y + 200))
        self.master.title('FilePath Input Window')
        self._path = None
##        self._filepath = None 
        self.filepath_var = tk.StringVar()
##        self.result_file = os.path.join(ROOT_DIR, 'Log Files', 'result.xlsx')
        self.input_entry = ttk.Entry(master, textvariable=self.filepath_var, width=55)
        self.input_entry.insert(0, "Input Excel Log File Path ")
        self.input_entry.grid(row=2, columnspan=2, padx=5,pady=(2,7))
        self.clear_button = ttk.Button(master, text='Clear', command=self.clear_entry)
        self.clear_button.grid(row=5, column=1, padx=5, pady=(12,5), sticky='w')
        self.submit_button = ttk.Button(master, text='Submit', command=self.submit)
        self.submit_button.grid(row=5, column=0, padx=5, pady=(12,5), sticky='e')
        self.error_label = ttk.Label(master, text=None, font=("Courier", 13))
        self.error_label.configure(foreground="red")
        self.clicked = self.input_entry.bind('<Button-1>', self.click)                                                 ## bind the "Entry Widget" with mouse click
        self.master.bind('<Return>', self.submit)
        self.master.bind('<Escape>', self.close)
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        self.master.focus_force()
        
    def click(self, event):                                                                                            ## Define a function to clear the content of the text widget
        self.input_entry.delete(0, 'end')
        self.input_entry.unbind('<Button-1>', self.clicked)
           
    def clear_entry(self):
        self.input_entry.delete(0, 'end')
        self.error_label.grid_forget()
        self.input_entry.insert(0, "Input Log File path")
        self.clicked = self.input_entry.bind('<Button-1>', self.click)     
           
    def submit(self, event=None):
        self.read_input()
        self.filepath_validation()

    def read_input(self):
        self._path = self.filepath_var.get()
        return self._path
       
    def save_to_default_dst(self, dst_path):
        self.master.destroy()
        messagebox.showinfo(title='Notification',
                    message='Due to input error, log file is written to preconfigured destination')
        dframe.to_excel(dst_path)
        messagebox.showinfo(title='Notification', message='File location is: '+ dst_path)
        
    def filepath_validation(self):
        if not self._path:
            self.error_label.config(text='Empty Input')
            self.error_label.grid(row=4, columnspan=2, pady=(2,7))
        elif os.path.isabs(self._path) == False:
            self.error_label.config(text='Invalid Input')
            self.error_label.grid(row=4, columnspan=2, pady=(2,7))
        elif os.path.splitext(self._path)[1] != '.xlsx':
            self.error_label.config(text='Excel file format cannot be determined, input correct filepath')
            self.error_label.grid(row=4, columnspan=2, pady=(2,7))
        else:
            self.error_label.config(text='Validating Input')
            self.error_label.configure(foreground='green')
            self.error_label.grid(row=4, columnspan=2, pady=(2,7))
##            self._filepath = self._path
            if self._path != source_file:
                self.save_result_file(self._path)
            else:
                self.save_to_default_dst(result_file)
       
    def save_result_file(self, file):
        dframe.to_excel(file)
        self.after(500, self.error_label.config(text='File was written to the destination path'))
        self.after(1500, self.master.destroy)
                        
    def close(self, event=None):
        self.master.destroy()
        sys.exit()


## Pandas DataFrame Calculation Code         
class Getter():
    def __init__(self, index):
        self.idx = index
        self.row = dframe.iloc[self.idx,:]
        self.dst_ip = self.row.Destination_Ip
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
    def ip_validator(self, ip_addr):
        try:
            ipaddress.ip_address(ip_addr)
        except:
            try:
                global _nakedip
                iface = ipaddress.ip_interface(ip_addr)
                _nakedip = iface.ip.exploded
                return _nakedip
            except ValueError as error:
                messagebox.showerror(title='Invalid IP Address Value', message=error)
                
    def check_ports(self, port, port_list):
        var = port in port_list
        return var
    
    def check_ip(self, ip, subnet):
        self.ip_validator(ip)
        if _nakedip:
            ip = _nakedip
        host  = ipaddress.ip_address(ip)
        net = ipaddress.ip_network(subnet)
        var = host in net
        return var
    
    def check_broadcast(self, ip):
        self.ip_validator(ip)
        if _nakedip:
            ip = _nakedip
        iface = ipaddress.ip_interface(ip+'/24')
        broadcast = iface.network.broadcast_address
        var = ip in broadcast.exploded
        return var
    
    @staticmethod
    def check_hits(hits:int, hit_nmbr=5) -> bool:
        var = (hits <= hit_nmbr)
        return var

    @staticmethod
    def check_hostname(host:str, hosts:list) -> bool:
        for host_pattern in hosts:
            var = bool(re.search(host_pattern, host.lower()))
            if var == True:
                break
        return var
    
def duplicate_hosts_list(dct):          ##this function sorts duplicate hostnames
    global dup_dict
    dup_dict = {}
    seen = []
    for key,value in dct.items():
        if value not in seen:
            seen.append(value)
            key_list = []
            key_list.append(key)
            dup_dict[value] = key_list
        else:
            key_list.append(key)
            dup_dict[value] = key_list
    return dup_dict


if __name__ == "__main__":
    ##Start GUI Application 
    root = tk.Tk()
    fr = Frame(root)
    fr.center_window(440, 200)
    root.mainloop()
    ##Start Pandas DataFrame Sorting
    if not dframe.empty:
        pd.set_option('display.max_columns', None)
        pd.set_option('max_colwidth', None)
        pd.set_option('display.max_rows', None)
        pd.set_option("expand_frame_repr", False)
        host_dict = dframe.Destination_HostName.sort_values(ascending=True, inplace=False).to_dict()
        duplicate_hosts_list(host_dict)                           ##Sort Duplicate Destination Hosts
        print(dup_dict)
        
        for hostname,idx_list in dup_dict.items():
            sttr = Setter()
            vl = Validator()
            if (vl.check_hostname(hostname, denied_hosts) == True):
                for idx in idx_list:
                    gttr = Getter(idx)
                    sttr.action_column_setter(dframe, idx, 'Block')
                    sttr.comments_column_setter(dframe, idx, 'Traffic to host will be blocked')
            elif (vl.check_hostname(hostname, allowed_hosts) == True):
                for idx in idx_list:
                    gttr = Getter(idx)
                    sttr.action_column_setter(dframe, idx, 'Allow')
                    sttr.comments_column_setter(dframe, idx, 'Conformation needed')
            elif (vl.check_hostname(hostname, ignored_hosts) == True):
                for idx in idx_list:
                    gttr = Getter(idx)
                    sttr.action_column_setter(dframe, idx, 'Ignore')
                    sttr.comments_column_setter(dframe, idx, 'Traffic to host will be ignored')
            else:
                for idx in idx_list:
                    gttr = Getter(idx)
                    if (vl.check_ports(gttr.dst_port, tcpdenied_ports) == True):
                        sttr.action_column_setter(dframe, idx, 'Block')
                        sttr.comments_column_setter(dframe, idx, 'Forbidden Destination Port')
                    elif (vl.check_ports(gttr.dst_port, udpdenied_ports) == True):
                        sttr.action_column_setter(dframe, idx, 'Block')
                        sttr.comments_column_setter(dframe, idx, 'Forbidden Destination Port')
                    elif (vl.check_hits(gttr.hit_nmbr, 5) == True):
                        sttr.action_column_setter(dframe, idx, 'Ignore')
                        sttr.comments_column_setter(dframe, idx, 'Less then 5 hits')
                    elif (vl.check_broadcast(gttr.dst_ip) == True):
                        sttr.action_column_setter(dframe, idx, 'Ignore')
                        sttr.comments_column_setter(dframe, idx, 'Broadcast IP Address')
                    else:
                        for subnet in denied_subnets:
                            if vl.check_ip(gttr.dst_ip, subnet) == True:
                                sttr.action_column_setter(dframe, idx, 'Block')
                                sttr.comments_column_setter(dframe, idx, 'Forbiden subnet')
                            else:
                                sttr.action_column_setter(dframe, idx, 'Verification required')
                                sttr.comments_column_setter(dframe, idx, 'Undefined')
        ## Input Window for defining location of the result Excel log file. 
        ##  print(dframe.sort_values(by=['Action'], ascending=True))
        root = tk.Tk()
        child_iframe = Child_Input_Frame(root)
        root.mainloop()

