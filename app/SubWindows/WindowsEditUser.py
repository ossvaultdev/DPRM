from tkinter import ttk, messagebox

import tkinter as tk
import hashlib
import os

import core.CoreInit as ci
import core.tools.Constant as cs
import core.user.User as cu

import app.tools.WindowsTools as wt   

class EditUsertWindows():
    
    def __init__(self, CoreInit :ci.CoreInit):
        
        self.CoreInit = CoreInit
        
    def get_windows(self, user_id :str, is_edit :bool):
        
        color_backgroud :str = cs.GUI_COLOR_BASE_SCREEN_BACK_COLOR
        
        update_user :cu.User = cu.User()
        
        windows_width :int = 370
        windows_height :int = 360
        windows_title :str = ""
        button_title :str = ""

        root = tk.Tk()
        root.iconbitmap(os.path.join(self.CoreInit.common_root_ini_path, "icon", "dprm_main.ico"))
        
        if is_edit:
            windows_title = "Edit User"
            button_title = "SAVE"
            
            update_user.user_id = user_id
            self.CoreInit.data.data_tools.get_user_data_by_id(update_user)
            
        else:
            windows_title = "New User"
            button_title = "NEW"
        
        root.title(windows_title)
        
        root.resizable(False, False)
        root.geometry(f"{windows_width}x{windows_height}+50+50") 
        root.configure(background=color_backgroud)
        
        root.wm_attributes("-topmost", True) 
        
        wt.WindowsTools.center_window(root)
        
        def is_valid_data_input() -> str:
            
            if not is_edit:
                if len(name_text.get()) == 0:
                    return "User name not valid, missing value"
            
                if not self.CoreInit.data.data_tools.is_valid_new_user_by_name(name_text.get()):
                    return "User name already exist on data system"
            
                if len(pwd_text.get()) == 0:
                    return "User password not valid, missing value"
            
                if (pwd_text.get() != pwd2_text.get()):
                    return "User password are not the same with check password"
            
            if len(frst_name_text.get()) == 0:
                return "User first name not valid, missing value"
                
            if len(lst_name_text.get()) == 0:
                return "User last name not valid, missing value"
            
            if len(address_text.get()) == 0:
                return "User address not valid, missing value"
            
            if not is_valid_address(address_text.get()):
                valid_address_char :str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 :.-,()'    
                return "Address not Valid. Character value allowed only: ['" + valid_address_char + "']'"

            if len(selected_country.get()) == 0:
                return "User country not valid, missing value"
            
            if not is_valid_email(email_text.get()):
                return "EMail not Valid [xxxxx@xxx.xx] -> [xxx.xxxx.x.xx@xxx.xx] No special aplha value admited"
                        
            if len(phone_text.get()) == 0:
                return "User phone not valid, missing value"
                
            if not is_valid_phone(phone_text.get()):
                valid_phone_number_char :str = '0123456789+.-()'
                return "Phone not Valid. Character value allowed only: ['" + valid_phone_number_char + "']'"
            
            return ""
        
        def is_valid_email(check_email :str) -> bool:
        
            valid_email_char :str = '.0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            user_email_split = check_email.split('@')
        
            if len(user_email_split) == 2:
            
                if ((is_valid_string(user_email_split[0], valid_email_char)) 
                    and (is_valid_string(user_email_split[1], valid_email_char))):
                    return True
            
            return False
    
        def is_valid_phone(check_phone :str) -> bool:
            
            valid_phone_number_char :str = '0123456789+.-()'
            
            if is_valid_string(check_phone, valid_phone_number_char):
                return True
            
            return False                
        
        def is_valid_address(check_address :str) -> bool:
            
            valid_address_char :str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 :.-,()'
            
            if is_valid_string(check_address, valid_address_char):
                return True
            
            return False                
            
        def is_valid_string(value_to_check :str, valid_value :str) -> bool:
            
            has_Value :bool = False
            
            for i in range(len(value_to_check)):
                has_Value = False
                for j in range(len(valid_value)):
                    if(value_to_check[i] == valid_value[j]):
                        has_Value = True
                        
                if not has_Value:
                    return False 
            
            return True

        def exit_windows():
            
            root.destroy()

        def check_input():
            
            check_data_input :str = is_valid_data_input()
            
            if len(check_data_input) > 0:
                messagebox.showerror("Error","Error on data input: " + check_data_input)
                root.wm_attributes("-topmost", True) 
            else:
                
                user :cu.User = cu.User()
                
                user.user_name = name_text.get()
                user.user_pwd = hashlib.sha256(pwd_text.get().encode()).hexdigest() 
                user.user_first_name = frst_name_text.get()
                user.user_last_name = lst_name_text.get()
                user.user_address = address_text.get()
                user.user_country = self.CoreInit.data.data_tools.get_code_country_by_definition(selected_country.get())
                user.user_email = email_text.get()
                user.user_phone = phone_text.get()
                
                if not is_edit:
                    self.CoreInit.data.data_tools.add_new_user(user)
                else:
                    user.user_id = user_id
                    self.CoreInit.data.data_tools.update_user(user)
                    
                user = None
                root.destroy()
                
        root.protocol("WM_DELETE_WINDOW", exit_windows)                
        
        title_label0 = ttk.Label(root, text=windows_title.upper(), font=("Font", 11), background=color_backgroud)
        title_label0.place(x=128,y=10, width=220)
        
        left_label :int = 13
        with_label :int = 140
        left_input :int = 128
        with_input :int = 220
        
        name_label = ttk.Label(root, text="NAME", background=color_backgroud)
        name_label.place(x=left_label,y=40, width=with_label)
        name_text = tk.StringVar(root)
        name_text.set(update_user.user_name)
        name_input_text_value = tk.Entry(root, textvariable=name_text)
        name_input_text_value.place(x=left_input, y=40, width=with_input, height=20)
        if is_edit:
            name_input_text_value.config(state="disabled")
        
        pwd_label = ttk.Label(root, text="PASSWORD", background=color_backgroud)
        pwd_label.place(x=left_label,y=70, width=with_label)
        pwd_text = tk.StringVar(root)
        pwd_text.set("")
        pwd_input_text_value = tk.Entry(root, show="*",textvariable=pwd_text)
        pwd_input_text_value.place(x=left_input, y=70, width=with_input, height=20)
        if is_edit:
            pwd_input_text_value.config(state="disabled")
        
        pwd2_label = ttk.Label(root, text="CHECK PASSWORD", background=color_backgroud)
        pwd2_label.place(x=left_label,y=100, width=with_label)
        pwd2_text = tk.StringVar(root)
        pwd2_text.set("")
        pwd2_input_text_value = tk.Entry(root, show="*",textvariable=pwd2_text)
        pwd2_input_text_value.place(x=left_input, y=100, width=with_input, height=20)
        if is_edit:
            pwd2_input_text_value.config(state="disabled")
        
        frst_name_label = ttk.Label(root, text="FIRST NAME", background=color_backgroud)
        frst_name_label.place(x=left_label,y=130, width=with_label)
        frst_name_text = tk.StringVar(root)
        frst_name_text.set(update_user.user_first_name)
        frst_name_input_text_value = tk.Entry(root,textvariable=frst_name_text)
        frst_name_input_text_value.place(x=left_input, y=130, width=with_input, height=20)
        
        lst_name_label = ttk.Label(root, text="LAST NAME", background=color_backgroud)
        lst_name_label.place(x=left_label,y=160, width=with_label)
        lst_name_text = tk.StringVar(root)
        lst_name_text.set(update_user.user_last_name)
        lst_name_input_text_value = tk.Entry(root,textvariable=lst_name_text)
        lst_name_input_text_value.place(x=left_input, y=160, width=with_input, height=20)
        
        address_label = ttk.Label(root, text="ADDRESS", background=color_backgroud)
        address_label.place(x=left_label,y=190, width=with_label)
        address_text = tk.StringVar(root)
        address_text.set(update_user.user_address)
        address_input_text_value = tk.Entry(root,textvariable=address_text)
        address_input_text_value.place(x=left_input, y=190, width=with_input, height=20)
        
        country_label = ttk.Label(root, text="COUNTRY", background=color_backgroud)
        country_label.place(x=left_label,y=220, width=with_label)
        selected_country = tk.StringVar(root)
        if is_edit:
            selected_country.set(self.CoreInit.data.data_tools.get_definition_country_by_code(update_user.user_country))    
        else:
            selected_country.set("")    
        
        country_selection = ttk.Combobox(root, textvariable=selected_country)

        country_selection['values'] = tuple(self.CoreInit.data.data_tools.get_default_values_country_definition())
        country_selection['state'] = 'readonly'
        country_selection.place(x=left_input, y=220, height=23, width=220)
        
        email_label = ttk.Label(root, text="EMAIL", background=color_backgroud)
        email_label.place(x=left_label,y=250, width=with_label)
        email_text = tk.StringVar(root)
        email_text.set(update_user.user_email)
        email_input_text_value = tk.Entry(root, textvariable=email_text)
        email_input_text_value.place(x=left_input, y=250, width=with_input, height=20)
        
        phone_label = ttk.Label(root, text="PHONE", background=color_backgroud)
        phone_label.place(x=left_label,y=280, width=with_label)
        phone_text = tk.StringVar(root)
        phone_text.set(update_user.user_phone)
        phone_input_text_value = tk.Entry(root, textvariable=phone_text)
        phone_input_text_value.place(x=left_input, y=280, width=with_input, height=20)

        change_pwd_button = ttk.Button(root,
                            text=button_title,
                            command=check_input)
        change_pwd_button.place(x=windows_width-171-8, y=windows_height-40)        
        
        exit_button = ttk.Button(root,
                          text='Exit',
                          command=exit_windows)
        exit_button.place(x=windows_width-91-8, y=windows_height-40)       
        
        root.mainloop()