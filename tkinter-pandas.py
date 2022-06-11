import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import os.path

class Enter_Frame(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self)
        self.main_window = ttk.Frame(self.master, width=50, height=40, relief=tk.SUNKEN)
        self.FilePath_Var = tk.StringVar()
        self.input_window = ttk.Entry(self.main_window, textvariable=self.FilePath_Var, width=45)
        self.input_window.grid(row=3, columnspan=2, padx=15,pady=(2,7))
        self.input_window.insert(0, "Input Log File path")
        self.label = ttk.Label(self.main_window, text='Log file path entry window')
        self.label.grid(row=1,columnspan=2, pady=(2,7))
        self.clear_button = ttk.Button(self.main_window, text='Clear', command=self.clear_entry)
        self.clear_button.grid(row=7, column=1, padx=5, pady=(12,5), sticky='w')
        self.submit_button = ttk.Button(self.main_window, text='Submit', command=self.submit)
        self.submit_button.grid(row=7, column=0, padx=5, pady=(12,5), sticky='e')
        ###Bind the Entry widget with Mouse Button to clear the content
        self.clicked = self.input_window.bind('<Button-1>', self.click)
        self.main_window.pack()
        self.main_window.focus_force()
        self.main_window.mainloop()
        
   
    ###Define a function to clear the content of the text widget
    def click(self, event):
        self.input_window.delete(0, 'end')
        self.input_window.unbind('<Button-1>', self.clicked)
   
    def clear_entry(self):
            self.input_window.delete(0, 'end')
            
    def submit(self):
        try:
            self.path = self.FilePath_Var.get()
            if len(self.path) == 0:
                tk.messagebox.showerror(title='Input Error', message='Empty value is not allowed')
                self.main_window.focus_force()
            dframe = pd.read_excel(self.path)
            self.master.destroy()
        except ValueError as e:
            result = tk.messagebox.askyesno(title='Invalid file path or buffer object type', message='Return to previous window ?')
            if result == True:
                self.clear_entry()
                self.main_window.focus_force()
            else:
                self.master.destroy()
        except FileNotFoundError as e:
            result = tk.messagebox.askyesno(title='FileNotFound', message='Return to previous window ?')
            if result == True:
                self.clear_entry()
                self.main_window.focus_force()
            else:
                self.master.destroy()
        return self.path
    
class Check_Frame(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self)
        self.main_frame = ttk.Frame(self.master, width=60, height=50, relief=tk.SUNKEN)
        self.Var0 = tk.BooleanVar()
        self.Var0.set(False)   
        self.Var1 = tk.BooleanVar()
        self.Var1.set(False)   
        self.Var2 = tk.BooleanVar()
        self.Var2.set(False)                      
        self.Var3 = tk.BooleanVar()
        self.Var3.set(False)   
        self.text_list = ["Denied Hosts", "Allowed Hosts", "TCP-Denied Ports", "UDP-Denied Ports"]
        self.var_dict = {}
        self.var_list = [self.Var0, self.Var1, self.Var2, self.Var3]
        self.var_value_list = [self.Var0.get(), self.Var1.get(), self.Var2.get(), self.Var3.get()]
        self.ChkBttn0 = ttk.Checkbutton(self.main_frame, text = self.text_list[0], width = 25, variable = self.Var0, onvalue = True, offvalue = False, command=lambda: self.checked(self.Var0))
        self.ChkBttn0.pack(padx = 5, pady = 5)
        self.ChkBttn1 = ttk.Checkbutton(self.main_frame, text = self.text_list[1], width = 25, variable = self.Var1, onvalue = True, offvalue = False, command=lambda: self.checked(self.Var1))
        self.ChkBttn1.pack(padx = 5, pady = 5)
        self.ChkBttn2 = ttk.Checkbutton(self.main_frame, text = self.text_list[2], width = 25, variable = self.Var2, onvalue = True, offvalue = False, command=lambda: self.checked(self.Var2))
        self.ChkBttn2.pack(padx = 5, pady = 5)
        self.ChkBttn3 = ttk.Checkbutton(self.main_frame, text = self.text_list[3], width = 25, variable = self.Var3, onvalue = True, offvalue = False, command=lambda: self.checked(self.Var3))
        self.ChkBttn3.pack(padx = 5, pady = 5)
        self.submit_button = ttk.Button(self.main_frame, text='Submit', command=self.submit)
        self.submit_button.pack(padx = 2, pady = 2)
        self.main_frame.focus_force() ## force focus on this window
        self.main_frame.pack()
        self.main_frame.mainloop()
    
    def submit(self):       ### code for "submit button" 
        for idx,i in enumerate(self.text_list):
            self.var_dict[i] = (self.var_list[idx]).get()
        self.master.destroy()
        ##print(self.var_dict)
        return self.var_dict
    
    def checked(self, var): ### what happenes when "checkbox" is checked
        idx = (self.var_list).index(var)
        self.var_value_list[idx]=var.get()
        return self.var_value_list
    
def main_foo():
    result = tk.messagebox.askyesno(message="Want to add new variables ?")
    root= tk.Tk()
    if result == True:
       cf = Check_Frame(root)
    else:
       ef = Enter_Frame(root)

if __name__ == "__main__":
    main_foo()
