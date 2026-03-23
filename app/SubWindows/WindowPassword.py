import hashlib
import tkinter as tk
from tkinter import ttk, messagebox

import os

import core.CoreInit as ci
import app.tools.WindowsTools as wt   
import core.tools.Constant as cs

class PasswordWindows():
    
    def __init__(self, CoreInit :ci.CoreInit):

        self.CoreInit = CoreInit
    
    def get_windows(self):
        
        color_backgroud :str = cs.GUI_COLOR_BASE_SCREEN_BACK_COLOR
        windows_width :int = 260
        windows_height :int = 170
    
        root = tk.Tk()
        root.iconbitmap(os.path.join(self.CoreInit.common_root_ini_path, "icon", "dprm_main.ico"))
        
        root.title("Password Change ...")
        root.resizable(False, False)
        root.geometry(f"{windows_width}x{windows_height}+50+50") 
        root.configure(background=color_backgroud)
        
        root.wm_attributes("-topmost", True) 
        
        wt.WindowsTools.center_window(root)
        
        def exit_windows():
            
            self.CoreInit.admin_pwd_change = False
            root.destroy()
        
        def check_input():
            
            password = hashlib.sha256(old_password_entry.get().encode()).hexdigest()
            
            if len(password) > 0 and password == self.CoreInit.data.admin_server_data["admin_password"]:
                new_password = new_password_entry.get()
                check_password = check_new_password_entry.get()
                if new_password == check_password:
                    self.CoreInit.data.change_admin_password(new_password)
                    self.CoreInit.admin_pwd_change = False
                    root.destroy()    
                else:
                    messagebox.showerror("New Password Error", "New password no match ...")    
                    root.wm_attributes("-topmost", True) 
            else:
                messagebox.showerror("New Password Error", "Invalid password Input ...")
                root.wm_attributes("-topmost", True) 
                
        root.protocol("WM_DELETE_WINDOW", exit_windows)                
        
        title_label = ttk.Label(root, text="CHANGE PASSWORD", font=("Font", 12), background=color_backgroud)
        title_label.place(x=45,y=10, width=170)
        
        title_label = ttk.Label(root, text="OLD PASSWORD:", background=color_backgroud)
        title_label.place(x=5,y=40, width=100)
        
        old_password_entry = tk.Entry(root, show="*")
        old_password_entry.place(x=120,y=40, width=130)
        
        title_label = ttk.Label(root, text="NEW PASSWORD:", background=color_backgroud)
        title_label.place(x=5,y=70, width=100)
        
        new_password_entry = tk.Entry(root, show="*")
        new_password_entry.place(x=120,y=70, width=130)
        
        title_label = ttk.Label(root, text="CHECK PASSWORD:", background=color_backgroud)
        title_label.place(x=5,y=100, width=115)
        
        check_new_password_entry = tk.Entry(root, show="*")
        check_new_password_entry.place(x=120,y=100, width=130)
        
        change_pwd_button = ttk.Button(root,
                            text='Change',
                            command=check_input)
        change_pwd_button.place(x=windows_width-165, y=windows_height-35)        
        
        exit_button = ttk.Button(root,
                          text='Exit',
                          command=exit_windows)
        exit_button.place(x=windows_width-85, y=windows_height-35)       
        
        root.mainloop()
