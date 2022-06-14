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


class Frame(ttk.Frame):                                                                 ### Master Frame Class Definition   
    def __init__(self, master):
        super().__init__(master)
        self.master.title('GUI Application')
        self.master.geometry('300x100')
        self.master.resizable(True,True)
        self.submit_button = ttk.Button(self, text='Submit', command=self.starter)
        self.submit_button.grid(padx=5, pady=(12,5), sticky='e')
        self.grid()

    def starter(self):
        self.master.withdraw()
        ef = Enter_Frame(self)
        ef.protocol("WM_DELETE_WINDOW",lambda: self.quit())

    def quit(self):
        self.master.destroy()
        sys.exit()

class Enter_Frame(tk.Toplevel):
    def __init__(self, master):
        super().__init__()
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
        self.clicked = self.input_entry.bind('<Button-1>', self.click)                ### Bind the Entry widget with Mouse Button to clear the content
        self.focus_force()
        
    def click(self, event):                                                           ### Define a function to clear the content of the text widget
        self.input_entry.delete(0, 'end')
        self.input_entry.unbind('<Button-1>', self.clicked)
           
    def clear_entry(self):
        self.input_entry.delete(0, 'end')
        self.error_label.grid_forget()
        self.input_entry.insert(0, "Input Log File path")
        self.clicked = self.input_entry.bind('<Button-1>', self.click)     
           
    def submit(self):
        self._path = self.filepath_var.get()
        self.filepath_validation()
        self.filepath                                                                              ### property "getter" attribute
        self.after(700, self.chain_foo)
    
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
        elif os.path.splitext(self._path)[1] != '.xlsx':
            self.error_label.config(text='Excel file format cannot be determined, input correct filepath')
            self.error_label.grid(row=4, columnspan=2, pady=(2,7))
        else:
            self.error_label.config(text='Log File path is Excepted ..')
            self.error_label.grid(row=4, columnspan=2, pady=(2,7))
            self.after(500, self.withdraw)
            self._filepath = self._path
            return  self._filepath
        
    @property
    def filepath(self):
        global dframe
        try:
            if self._filepath:
                dframe = pd.read_excel(self._filepath)
                return dframe
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
            
class Input_Frame(tk.Tk):
    def __init__(self, text_var):
        super().__init__()
        self.var = text_var
        self._checkbox_dict = self.checkbox_dict
        global checkbox_dict
        checkbox_dict = {}
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
        self.clicked = self.input_entry.bind('<Button-1>', self.click)                 ## bind the "Entry Widget" with mouse click
        self.focus_force()
        
    def click(self, event):                                                            ## define a function to clear the content of the text widget
        self.input_entry.delete(0, 'end')
        self.input_entry.unbind('<Button-1>', self.clicked)
          
    def clear_entry(self):                                                             ## handle mouse click event
        self.input_entry.delete(0, 'end')
        self.error_label.grid_forget()
        self.input_entry.insert(0, self.text)
        self.clicked = self.input_entry.bind('<Button-1>', self.click)     

    def submit(self):
        self._input_value = self._input.get()
        if 'port' in self.var:
            self.port_checker(self.var)
        elif 'host' in self.var:
            self.host_checker(self.var)
    
    def port_checker(self, var):
        if not self._input_value:
            self.error_label.config(text='Empty Input')
            self.error_label.grid(row=3, columnspan=2, pady=(2,7))
        else:
            port_list = [value.strip() for value in self._input_value.split(',')]
            for port in port_list:
                if port.isnumeric() == False:
                    self.error_label.config(text=port+' - Invalid Port Value')
                    self.error_label.grid(row=3, columnspan=2, pady=(2,7))
                    break
            else:
                self.error_label.config(text='Input Excepted')
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
                if host.isnumeric() == True:
                    self.error_label.config(text=host+' - Invalid Host Name')
                    self.error_label.grid(row=3, columnspan=2, pady=(2,7))
                    break
            else:
                self.error_label.config(text='Input Excepted')
                self.error_label.grid(row=3, columnspan=2, pady=(2,7))
                checkbox_dict[var] = host_list
                self.destroy()
                return checkbox_dict
    @property
    def checkbox_dict(self):
        return self._checkbox_dict
            
    @checkbox_dict.setter
    def checkbox_dict(self):
        self._checkbox_dict = checkbox_dict
        return self._checkbox_dict
    
        

class CheckBox_Frame(tk.Toplevel):
    def __init__(self, master, checkbars=[]):
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
        self.focus_force()

    def submit(self):                                          ### code for "submit button"
        check_list = []
        for idx,item in enumerate(self.vars):
            if item.get() == True:
                check_list.append(self.var_dict[idx])
        self.master.destroy()
        for item in check_list:
            self.inputframe_starter(item)
         
    def checked(self, var):                                    ### what happens when "checkbox" is checked
        idx = (check_list).index(var)
        self.var_value_list[idx]=var.get()
        return self.var_value_list
    
    def inputframe_starter(self, var):
        iframe = Input_Frame(var)
        iframe.mainloop()
        
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
    def comments_column_setter(self, df, index, comment):
        df.at[index, 'Comments'] = comment
        
        
class Checker():
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

   
