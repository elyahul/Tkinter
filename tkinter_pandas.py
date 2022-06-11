import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import os.path
import time

var_dict = {}
var_list = []
checkbox_dict = {}

class Enter_Frame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title('Log file path Entry Frame')
        self.path = ''
        self.FilePath_Var = tk.StringVar()
        self.input_window = ttk.Entry(self, textvariable=self.FilePath_Var, width=45)
        self.input_window.grid(row=3, columnspan=2, padx=15,pady=(2,7))
        self.input_window.insert(0, "Input Log File path")
        self.error_label = ttk.Label(self, text='', font=("Courier", 11))
        self.error_label.configure(foreground="red")
        self.clear_button = ttk.Button(self, text='Clear', command=self.clear_entry)
        self.clear_button.grid(row=7, column=1, padx=5, pady=(12,5), sticky='w')
        self.submit_button = ttk.Button(self, text='Submit', command=self.submit)
        self.submit_button.grid(row=7, column=0, padx=5, pady=(12,5), sticky='e')
        self.clicked = self.input_window.bind('<Button-1>', self.click)          ### Bind the Entry widget with Mouse Button to clear the content
        self.grid()
        self.focus_force()
        
        
    def click(self, event):                                                      ### Define a function to clear the content of the text widget
        self.input_window.delete(0, 'end')
        self.input_window.unbind('<Button-1>', self.clicked)
   
    def clear_entry(self):
        self.input_window.delete(0, 'end')
        self.error_label.grid_forget()
        
##    def destroy(self):
##        self.master.()
            
    def submit(self):
        self.path = self.FilePath_Var.get()
        self.file_validation()
                
    
    def file_validation(self):
        if len(self.path) == 0:
            self.error_label.config(text='Empty Input')
            self.error_label.grid(row=4, columnspan=2, pady=(2,7))
        elif os.path.isabs(self.path) == False:
            self.error_label.config(text='Invalid Input')
            self.error_label.grid(row=4, columnspan=2, pady=(2,7))
        elif os.path.isfile(self.path) == False:
            self.error_label.config(text='File Not Found')
            self.error_label.grid(row=4, columnspan=2, pady=(2,7))
        elif os.path.splitext(self.path)[1] != '.xlsx':
            self.error_label.config(text='Excel file format cannot be determined, input correct filepath')
            self.error_label.grid(row=4, columnspan=2, pady=(2,7))
        else:
            self.error_label.config(text='Log File path is Excepted ..')
            self.error_label.grid(row=4, columnspan=2, pady=(2,7))
            return self.path
        
    def input_validation():
        if self.path:
            iframe = Input_Frame(self)
            
        
    
class Input_Frame(tk.Toplevel):
    def __init__(self, parent = Enter_Frame()):
        super().__init__()
        options = {'padx':5, 'pady':5}                                                 ## field options
        self.var = tk.StringVar()
        self.error_var = tk.StringVar()
        self.text='Input Here"
        self.input_widgit = ttk.Entry(self, textvariable=self.var, width=40)
        self.input_widgit.grid(row=2, columnspan=2, padx=5,pady=(2,7))
        self.input_widgit.insert(0, text)
        self.infolabel = ttk.Label(self, text='   ')
        self.infolabel.grid(row=1,columnspan=2, pady=(2,7), sticky=tk.W)
        self.infolabel.configure(foreground="red")
        self.clear_button = ttk.Button(self, text='Clear', command=self.clear_entry)
        self.clear_button.grid(row=5, column=1, padx=5, pady=(12,5), sticky='w')
        self.submit_button = ttk.Button(self, text='Submit', command=self.submit)
        self.submit_button.grid(row=7, column=0, padx=5, pady=(12,5), sticky='e')
        self.error_label = ttk.Label(self, text='', font=("Courier", 13))
        self.error_label.configure(foreground="red")
        self.clicked = self.input_widgit.bind('<Button-1>', self.click)                ## bind the "Entry Widget" with mouse click
        self.grid()       
        
##    def click(self, event):                                                            ## define a function to clear the content of the text widget
##        self.input_widgit.delete(0, 'end')
##        self.input_widgit.unbind('<Button-1>', self.clicked)
##          
##    def clear_entry(self):                                                             ## handle mouse click event
##        self.input_widgit.delete(0, 'end')
##        self.error_label.config(text='')
##                
##    def destroy(self):
##        self.master.destroy()

    def port_checker(self):
        if len(self.var_value) == 0:
             self.error_label.config(text='Empty Input not Allowed')
             self.error_label.grid(row=3, columnspan=2, pady=(2,7))
        else:
            port_list = [i.strip() for i in self.var_value.split(',')]
            for i in port_list:
                if i.isnumeric() == False:
                    self.error_label.config(text=i + ' -- is invalid port value')
                    self.error_label.grid(row=3, columnspan=2, pady=(2,7))
                else:
                    self.error_label.config(text='Input is Excepted')
                    self.error_label.grid(row=3, columnspan=2, pady=(2,7))
        return 

class Frame(tk.Tk):
    def __init__(self, obj):
        super().__init__()
        self.title(obj+'  input frame')
        self.geometry('350x130')
        self.resizable(True,True)
    

class CheckBox_Frame(ttk.Frame):
    def __init__(self, master, checkbars=[]):
        ttk.Frame.__init__(self)
        self.master.title('CheckBox Frame')
        self.vars = []
        self.main_frame = ttk.Frame(self.master, width=1200, height=50, relief=tk.SUNKEN)
        self.main_frame.focus_force()                        ## force focus on this window
        self.main_frame.pack()
        for idx,checkbar in enumerate(checkbars):
            var_dict[idx] = checkbar
            self.var = tk.BooleanVar()
            self.ChkBttn = ttk.Checkbutton(self.main_frame, text=checkbar, width = 25, variable=self.var)
            self.ChkBttn.pack(padx = 5, pady = 5)
            self.vars.append(self.var)
        self.submit_button = ttk.Button(self.main_frame, text='Submit', command=self.submit)
        self.submit_button.pack(padx = 2, pady = 2)

    def submit(self):                                         ### code for "submit button"
        for idx,item in enumerate(self.vars):
            if item.get() == True:
                var_list.append(var_dict[idx])
        self.master.destroy()
        return var_list

    def checked(self, var):                                    ### what happens when "checkbox" is checked
        idx = (self.var_list).index(var)
        self.var_value_list[idx]=var.get()
        return self.var_value_list
    
def main_foo():
    result = tk.messagebox.askyesno(message="Want to add new variables ?")
    root= tk.Tk()
    if result == True:
       cf = CheckBox_Frame(root, ['allowed_hosts', 'denied_hosts', 'tcpdenied_ports', 'udpdenied_ports'])
    else:
       ef = Enter_Frame(root)
    root.mainloop() 

if __name__ == "__main__":
    root = tk.Tk()
    ef = Enter_Frame(root)
    root.mainloop()
##    main_foo()
##    for item in var_list:
##        if 'host' in item:
##            fr = Frame(item) 
##            iframe = Input_Frame(fr, item)
##            def host_checker():
##                if len(var_value) != 0:
##                    host_list = [value.strip() for value in var_value.split(',')]
##                    checkbox_dict[item] = host_list
##                    for host in host_list:
##                        if host.isnumeric() == True:
##                            iframe.error_label.config(text=host + ' -- is invalid host name')
##                            iframe.error_label.grid(row=3, columnspan=2, pady=(2,7))
##                            break
##                    else:
##                        iframe.error_label.config(text='Input is Excepted')
##                        iframe.error_label.grid(row=3, columnspan=2, pady=(2,7))
##                        
##                else:
##                     iframe.error_label.config(text='Empty Input not Allowed')
##                     iframe.error_label.grid(row=3, columnspan=2, pady=(2,7))
##                return checkbox_dict
##            def submit(foo):
##                global var_value
##                var_value = iframe.var.get()
##                foo()
##                fr.mainloop()
##            submit_button = ttk.Button(iframe, text='Submit', command=lambda: submit(host_checker))
##            submit_button.grid(row=5, column=0, padx=5, pady=(12,5), sticky='e')
##            fr.mainloop()
##        else:
##            fr = Frame(item) 
##            iframe = Input_Frame(fr, item)
##            def port_checker():
##                if len(var_value) != 0:
##                    port_list = [value.strip() for value in var_value.split(',')]
##                    checkbox_dict[item] = port_list
##                    for port in port_list:
##                        if port.isnumeric() == False:
##                            iframe.error_label.config(text=port + ' -- is invalid host name')
##                            iframe.error_label.grid(row=3, columnspan=2, pady=(2,7))
##                            break
##                    else:
##                        iframe.error_label.config(text='Input is Excepted')
##                        iframe.error_label.grid(row=3, columnspan=2, pady=(2,7))
##                        
##                else:
##                     iframe.error_label.config(text='Empty Input not Allowed')
##                     iframe.error_label.grid(row=3, columnspan=2, pady=(2,7))
##                return checkbox_dict
##            def submit(foo):
##                global var_value
##                var_value = iframe.var.get()
##                foo()
##                fr.mainloop()
##            submit_button = ttk.Button(iframe, text='Submit', command=lambda: submit(port_checker))
##            submit_button.grid(row=5, column=0, padx=5, pady=(12,5), sticky='e')
##            fr.mainloop()
##
