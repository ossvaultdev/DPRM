import hashlib
import tkinter as tk
from tkinter import ttk, messagebox

import os

import core.CoreInit as ci
import app.tools.WindowsTools as wt   
import core.tools.Constant as cs

class LoginWindows():
    
    def __init__(self, CoreInit :ci.CoreInit):
        
        self.CoreInit = CoreInit
        self.root :tk.Tk = None
        
    def get_windows(self):
        
        color_backgroud :str = cs.GUI_COLOR_BASE_SCREEN_BACK_COLOR
        windows_width :int = 400
        windows_height :int = 220
        
        self.root = tk.Tk()
        self.root.iconbitmap(os.path.join(self.CoreInit.common_root_ini_path, "icon", "dprm_main.ico"))
        self.root.title("Login ...")
        self.root.resizable(False, False)
        self.root.geometry(f"{windows_width}x{windows_height}+50+50") 
        self.root.attributes('-topmost', 1)
        self.root.configure(background=color_backgroud)
        
        wt.WindowsTools.center_window(self.root)
        
        tk.Label(
            self.root,
            text="ADMIN APPLICATION LOGIN",
            font=("Font", 14),
            background=color_backgroud,
        ).pack(ipady=5, fill="x")
        
        tk.Label(
            self.root,
            text="Data Product Management Refined",
            font=("Font", 18),
            background=color_backgroud,
        ).pack(ipady=5, fill="x")
        
        exit_button = ttk.Button(self.root,
                          text='Exit',
                          command=self.root.destroy)
        
        exit_button.place(x=windows_width-90, y=windows_height-40)

        def check_input():
                        
            password = hashlib.sha256(password_entry.get().encode()).hexdigest()
            
            if len(password) > 0 and password == self.CoreInit.data.admin_server_data["admin_password"]:
                self.CoreInit.admin_login = password 
                self.root.destroy()
            else:
                messagebox.showerror("Login Error", "Invalid password Input ...")

        tk.Label(self.root, text="Admin Password:", background=color_backgroud, font=("Font", 11)).pack(anchor="w", padx=30)

        password_entry = tk.Entry(self.root, show="*", font=("Font", 14))
        password_entry.pack(padx=30, fill="x")
        
        tk.Button(
            self.root,
            text="LOGIN",
            command=check_input,
            width=18,            
        ).pack(pady=10, padx=30, fill="x")
        
        self.root.mainloop()
        