
##########################################################################
# This code was created to sort Tufin Log File which is created
# by Tufin application based on Firewall traffic monitoring.
#
# Two columns were added to the original Tufin's log file.
# Column names are: "Comment" and "Action". The result of "Action" column
# is set after code execution and depends on global variables
# which defined manually (all variables are stored separetly using JSON)
# or alternatevly could be created and added during code execution.
# Three possible results of "Action" column calculation are:
# "Allow", "Block" or "Ignore".
#
# "Comments" column is optional and can be easily ommited or
# modified due to code modular structure and free access to
# code source itself.
#
# Due to code modularity the creation of new columns on original log file
# does not impact script execution. New column's data is easily accessed
# and any manipulations are possible via adding corresponding function to
# the appropriate Class.
#
# This script is packed into Python package. It can be executed on Windows
# or Linux OS. Json dictionaries are created and saved automatically
# without User ....
# The graphycal interface is created by Tkinter module and has full
# interaction with the rest of the script.
# All rights reserved to ELIL
############################################################################

import pandas as pd
import ipaddress
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
import re
import os.path
import sys
import time
import pdb
from config.definitions import ROOT_DIR


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
        self.bind('<Return>', self.submit)
        self.bind('<Escape>', self.close)
        self.focus_force()
        
    def click(self, event):                                                                                            ## Define a function to clear the content of the text widget
        self.input_entry.delete(0, 'end')
        self.input_entry.unbind('<Button-1>', self.clicked)
           
    def clear_entry(self):
        self.input_entry.delete(0, 'end')
        self.error_label.grid_forget()
        self.input_entry.insert(0, "Input Log File path")
        self.clicked = self.input_entry.bind('<Button-1>', self.click)     
           
    def submit(self, event=None):
        self._path = self.filepath_var.get()
        self.filepath_validation()
        self.dframe_create                                                                              
        self.after(1000, self.chain_foo)
    
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
            print(self._path, os.path.splitext(self._path)[1])
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
        
        try:
            if self._filepath:
                source_file = self._filepath 
                dframe = pd.read_excel(self._filepath)
                return dframe, source_file
        except ValueError as error:
            messagebox.showerror(message=error)
            self.master.destroy()
            sys.exit()
                      
    def chain_foo(self):
        if self._filepath:
            result = messagebox.askyesno(message="Add new variables ?")
            if result == True:
                self.checkbox_strater()
            elif result == False:
                self.master.destroy()
                       
    def checkbox_strater(self):
        ch = CheckBox_Frame(self, ['allowed_hosts', 'denied_hosts', 'tcpdenied_ports', 'udpdenied_ports'])

    def close(self, event=None):
        self.master.deiconify()
        self.destroy()
            
class Input_Frame(tk.Tk):
    def __init__(self, text_var):
        super().__init__()
        self._checkbox_dict = None
        self.var = text_var
        self.title('New Variables Entry Widget')
        self._input = tk.StringVar()
        self._input_value = None
        self.text= "Input new " + text_var
        self.input_entry = ttk.Entry(self, textvariable=self._input, width=50)
        self.input_entry.grid(row=2, columnspan=2, padx=5,pady=(2,7))
        self.input_entry.insert(0, self.text)
        self.clear_button = ttk.Button(self, text='Clear', command=self.clear_entry)
        self.clear_button.grid(row=5, column=1, padx=5, pady=(12,5), sticky='w')
        self.submit_button = ttk.Button(self, text='Submit', command=self.submit)
        self.submit_button.grid(row=5, column=0, padx=5, pady=(12,5), sticky='e')
        self.error_label = ttk.Label(self, text=None, font=("Courier", 13))
        self.error_label.configure(foreground="red")
        self.clicked = self.input_entry.bind('<Button-1>', self.click)          ##bind the "Ent ry Widget" with mouse click
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
        self._input_value = self._input.get()
        if 'host' in self.var:
            self.host_checker(self.var)
        elif 'port' in self.var:
            self.port_checker(self.var)
    
    def port_checker(self, var:int):
        if not self._input_value:
            self.error_label.config(text='Empty Input')
            self.error_label.grid(row=3, columnspan=2, pady=(2,7))
        else:
            port_list = [value.strip() for value in self._input_value.split(',')]
            for port in port_list:
                if not port:
                    port_list.remove(port)
                elif  port.isnumeric() == False:
                    self.error_label.config(text=port+' - Invalid Port Value')
                    self.error_label.grid(row=3, columnspan=2, pady=(2,7))
                    break
            else:
                self.error_label.config(text='Input Excepted')
                self.error_label.configure(foreground='green')
                self.error_label.grid(row=3, columnspan=2, pady=(2,7))
                checkbox_dict[var] = port_list
                self.destroy()
                return checkbox_dict
            
    def host_checker(self, var):
        if not self._input_value:
            self.error_label.config(text='Empty Input')
            self.error_label.grid(row=3, columnspan=2, pady=(2,7))
        else:
            host_list = [value.strip() for value in self._input_value.split(',')]
            for host in host_list:
                if not host:
                    host_list.remove(host)
                elif host.isnumeric() == True:
                    self.error_label.config(text=host+' - Invalid Host Name')
                    self.error_label.grid(row=3, columnspan=2, pady=(2,7))
                    break
            else:
                self.error_label.config(text='Input Excepted')
                self.error_label.configure(foreground='green')
                self.error_label.grid(row=3, columnspan=2, pady=(2,7))
                checkbox_dict[var] = host_list
                self.destroy()
                self.checkbox_dict_add(checkbox_dict)
                return checkbox_dict
                
    def checkbox_dict(self):
        self._checkbox_dict = checkbox_dict
        return self._checkbox_dict
    
    @staticmethod
    def checkbox_dict_add(dct):
        for key,value in dct.items():
            if key == 'allowed_hosts':
                for var in value:
                    allowed_hosts.append(var)
            elif key == 'denied_hosts':
                for var in value:
                    denied_hosts.append(var)
            elif key == 'tcpdenied_ports':
                for var in value:
                    tcpdenied_ports.append(var)
            elif key == 'udpdenied_port':
                for var in value:
                    udpdenied_ports.append(var)
        return (allowed_hosts, denied_hosts, tcpdenied_ports, udpdenied_ports)
        
    def close(self, event=None):
        self.destroy()
       
class Child_Input_Frame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        self.master.geometry("+%d+%d" % (x + 100, y + 200))
        self.master.title('FilePath Input Window')
        self._path = None
        self._filepath = None 
        self.filepath_var = tk.StringVar()
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
        self._path = self.filepath_var.get()
        self.filepath_validation()

    
    def default_filepath(self, sourcefile):
        self.master.destroy()
        messagebox.showinfo(title='Notification',
                    message='Due to input error, log file is written to preconfigured location')
        result = r''.join([os.path.splitext(sourcefile)[0]+'_final', os.path.splitext(sourcefile)[1]])
        with open(result, 'w') as r:
            dframe.to_excel(result)
        messagebox.showinfo(title='Notification',
                    message='File location is: '+result)
        
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
            self._filepath = self._path
            if not self._filepath == source_file:
                self.file_create(self._filepath)
            else:
                self.default_filepath(source_file)
       
    def file_create(self, file):
        with open(file, 'w') as f:
            dframe.to_excel(file)
            self.after(500, self.error_label.config(text='File was written to the destination path'))
            self.after(1500, self.master.destroy)
                        
    def close(self, event=None):
        self.master.destroy()
        sys.exit()
             
class CheckBox_Frame(tk.Toplevel):
    def __init__(self, master, checkbars=[]):
        global checkbox_dict
        checkbox_dict = {}
        super().__init__()
        self.var_dict = {}
        self.title('CheckBox Frame')
        self.vars = []
        for idx,checkbar in enumerate(checkbars):
            self.var_dict[idx] = checkbar
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
                check_list.append(self.var_dict[idx])
        self.master.destroy()
        for item in check_list:
            self.inputframe_starter(item)
         
    def checked(self, var):                                                 ## what happens when "checkbox" is checked
        idx = (check_list).index(var)
        self.var_value_list[idx]=var.get()
        return self.var_value_list
    
    def inputframe_starter(self, var):
        iframe = Input_Frame(var)
        iframe.mainloop()

    def close(self, event=None):
        self.master.destroy()

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
                sys.exit()
                
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
    
    def check_hits(self, hits, hit_nmbr):
        var = (hits <= hit_nmbr)
        return var
    
    def check_hostname(self, hostname, host_list):
        for pattern in host_list:
            var = bool(re.search(pattern, hostname.lower()))
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
print(os.path.join(ROOT_DIR, 'data', 'variables.json'))
    
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
        ##Gui Input Window for target result Excel log file 
       
    ##        print(dframe.sort_values(by=['Action'], ascending=True))
        root = tk.Tk()
        child_iframe = Child_Input_Frame(root)
        root.mainloop()

