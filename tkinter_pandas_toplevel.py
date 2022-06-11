import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import os.path
import sys
import time
import pandas as pd


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

    @property
    def filepath(self):
        global dframe
        try:
            if ef._filepath:
                dframe = pd.read_excel(ef._filepath)
                return dframe
        except exception as e:
            print(e)

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
            assert type(self._filepath) == str
            return  self._filepath
        
    @property
    def filepath(self):
        global dframe
        try:
            if self._filepath:
                dframe = pd.read_excel(self._filepath)
                return dframe
        except exception as e:
            print(e)
                  
    def chain_foo(self):
        if self._filepath:
            result = tk.messagebox.askyesno(message="Want to add new variables ?")
            if result == True:
                print(self.filepath)
                self.checkbox_strater()
            elif result == False:
                print(self.filepath)
                self.destroy()
                self.master.destroy()
               
    def checkbox_strater(self):
        ch = CheckBox_Frame(self, ['allowed_hosts', 'denied_hosts', 'tcpdenied_ports', 'udpdenied_ports'])
            
class Input_Frame(tk.Tk):
    def __init__(self, text):
        super().__init__()
        global checkbox_dict
        checkbox_dict = {}
        self.title('New Variables Entry Widget')
        self._input = tk.StringVar()
        self._input_value = None
        self.var = text
        self.text= "Input new " + text
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
            self.port_checker(self.var, )
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

    def submit(self):                                         ### code for "submit button"
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
        
   
    

if __name__ == "__main__":
    root = tk.Tk()
    fr = Frame(root)
    root.mainloop()
    print('exit')
    print(checkbox_dict)
    l = [1,2,3]
    print(l)
