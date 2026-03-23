import tkinter as tk
from tkinter import ttk, messagebox

import os

import core.CoreInit as ci
import app.tools.WindowsTools as wt   
import core.tools.Constant as cs

class PasswordWindows():
    
    def __init__(self, CoreInit :ci.CoreInit):

        self.CoreInit = CoreInit
        
    
    def get_windows(self, user_id :str):
        
        color_backgroud :str = cs.GUI_COLOR_BASE_SCREEN_BACK_COLOR
        windows_width :int = 260
        windows_height :int = 140
    
        root = tk.Tk()
        root.iconbitmap(os.path.join(self.CoreInit.common_root_ini_path, "icon", "dprm_main.ico"))
        
        root.title("User Reset Password ...")
        root.resizable(False, False)
        root.geometry(f"{windows_width}x{windows_height}+50+50") 
        root.configure(background=color_backgroud)
        
        root.wm_attributes("-topmost", True) 
        
        wt.WindowsTools.center_window(root)
        
        def is_valid_string(str_value_to_check :str, valid_value_char :str) -> bool:
        
            has_valid_char :bool = False
            
            if len(str_value_to_check) > 0:
            
                for i in range(len(str_value_to_check)):
                    
                    has_valid_char = False
                    for j in range(len(valid_value_char)):
                        
                        if str_value_to_check[i] == valid_value_char[j]:
                            has_valid_char = True
                            break
                            
                    if not has_valid_char:
                        return False
                    
            return True
        
        def exit_windows():
            
            self.CoreInit.admin_pwd_change = False
            root.destroy()
        
        def check_input():
            
            valid_pwd_char = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ?!&%ç*"+-/_-'
            
            new_password = new_password_entry.get()
            check_password = check_new_password_entry.get()
            
            if len(new_password) < 8:
                messagebox.showerror("Reset Password Error", 
                                     "Lenght of New password is less than 8 minumum value digit ...")    
                
                root.wm_attributes("-topmost", True) 
                return 
            
            if not is_valid_string(new_password, valid_pwd_char):
                messagebox.showerror("Reset Password Error", 
                                     'Password is not valid format!\n\n' + 'Character value allowed only: [' 
                                     + valid_pwd_char + '] ...')    
                
                root.wm_attributes("-topmost", True) 
                return 
            
            if new_password != check_password:
                messagebox.showerror("Reset Password Error", 
                                     "New password and check password not match ...")    
                root.wm_attributes("-topmost", True) 
                
                return 
            
            self.CoreInit.data.data_tools.reset_user_password(user_id, new_password)
            messagebox.showinfo("Reset Password",
                                "Paswword for user id: " + str(user_id) + " has been modified!")
            root.destroy()    
            
        root.protocol("WM_DELETE_WINDOW", exit_windows)                
        
        title_label = ttk.Label(root, text="RESET PASSWORD", font=("Font", 12), background=color_backgroud)
        title_label.place(x=45,y=10, width=170)
        
        title_label = ttk.Label(root, text="NEW PASSWORD:", background=color_backgroud)
        title_label.place(x=5,y=40, width=100)
        
        new_password_entry = tk.Entry(root, show="*")
        new_password_entry.place(x=120,y=40, width=130)
        
        title_label = ttk.Label(root, text="CHECK PASSWORD:", background=color_backgroud)
        title_label.place(x=5,y=70, width=115)
        
        check_new_password_entry = tk.Entry(root, show="*")
        check_new_password_entry.place(x=120,y=70, width=130)
        
        change_pwd_button = ttk.Button(root,
                            text='Change',
                            command=check_input)
        change_pwd_button.place(x=windows_width-165, y=windows_height-35)        
        
        exit_button = ttk.Button(root,
                          text='Exit',
                          command=exit_windows)
        exit_button.place(x=windows_width-85, y=windows_height-35)       
        
        root.mainloop()
