import tkinter as tk
from tkinter import ttk, messagebox

import os

import core.CoreInit as ci
import app.tools.WindowsTools as wt   
import core.tools.Constant as cs

import core.tools.DataTools as dt

class EditProxyRedirectWindows():
    
    def __init__(self, CoreInit :ci.CoreInit):
        
        self.CoreInit = CoreInit
        
    def get_windows(self, is_proxy :bool, is_edit: bool, label_value_list :list):
        
        color_backgroud :str = cs.GUI_COLOR_BASE_SCREEN_BACK_COLOR
        windows_width :int = 260
        windows_height :int = 170
        windows_title :str = ""
        button_title :str = ""

        label_value_list_default :list = []

        if str(label_value_list[0][1])[1:-1][0:1] == "'":
            label_value_list_default.append(str(label_value_list[0][1])[2:-2])    
        else:
            label_value_list_default.append(str(label_value_list[0][1])[1:-1])    
            
        if is_proxy:
            label_value_list_default.append(str(label_value_list[1][1])[2:-2])
        else:
            label_value_list_default.append(str(label_value_list[1][1])[1:-1])

        label_value_list_default.append(str(label_value_list[2][1])[2:-2])

        root = tk.Tk()
        root.iconbitmap(os.path.join(self.CoreInit.common_root_ini_path, "icon", "dprm_main.ico"))
        
        if is_edit:
            windows_title = "Edit"
            button_title = "SAVE"
        else:
            windows_title = "New"
            button_title = "NEW"
        
        if is_proxy:
            windows_title += " Proxy Server ..."
        else:
            windows_title += " Redirect Server ..."
        
        root.title(windows_title)
        
        root.resizable(False, False)
        root.geometry(f"{windows_width}x{windows_height}+50+50") 
        root.configure(background=color_backgroud)
        
        root.wm_attributes("-topmost", True) 
        
        wt.WindowsTools.center_window(root)

        def is_valid_data_input_value(is_proxy :bool, is_edit: bool, 
                                      input_list :list[tk.Entry], 
                                      input_list_default :list[list[str]]) -> bool:
    
            ip_port_value :str = ""
            sql_statements :str = ""

            if is_proxy:
                # PROXY SERVER
                for i in range(1,3):

                    ip_port_value = input_list[i].get()

                    if len(ip_port_value) == 0:
                        messagebox.showerror("Error on data validation", "No Ip Port defined ...")
                        return False
                    
                    if not self.CoreInit.is_valid_ip_port_format(ip_port_value):
                        messagebox.showerror("Error on data validation", 
                                             "Ip Port not valid [[0..255].[0..255].[0..255].[0..255]]:[0..65535]]")
                        return False
                    
                if len(input_list[0].get()) > 0:
                   
                    if input_list_default[0] != input_list[0].get():
                        
                        sql_statements = "SELECT COUNT(*) FROM " + dt.TABLE_NAME_SYS_PROXY_REQUEST  
                        sql_statements += " WHERE name = '" + input_list[0].get() + "'"
                
                        if self.CoreInit.data.data_tools.sql_is_count_exist_statements(sql_statements):
                            messagebox.showerror("Error on data validation", "Name definition already exist on database ...")
                            return False
                else:
                    messagebox.showerror("Error on data validation", "No Name defined ...")
                    return False

                if input_list_default[1] != input_list[1].get() or input_list_default[2] != input_list[2].get() : 

                    sql_statements = "SELECT COUNT(*) FROM " + dt.TABLE_NAME_SYS_PROXY_REQUEST 
                    sql_statements += " WHERE HTTP = '" + input_list[1].get() + "' AND HTTPS ='" + input_list[2].get() + "'" 
                    
                    if self.CoreInit.data.data_tools.sql_is_count_exist_statements(sql_statements):
                        messagebox.showerror("Error on data validation", "Ip Port definition combinaison already exist ...")
                        return False
                    
            else:
            
                ip_port_value = input_list[2].get()
                
                if len(ip_port_value) == 0:
                    messagebox.showerror("Error on data validation", "No Ip Port defined ...")
                    return False

                if not self.CoreInit.is_valid_ip_port_format(ip_port_value):
                    messagebox.showerror("Error on data validation", 
                                         "Ip Port not valid [[0..255].[0..255].[0..255].[0..255]]:[0..65535]]")
                    return False

                if not self.CoreInit.is_max_users_allowed(input_list[1].get()):
                    messagebox.showerror("Error on data validation", 
                                         "Max users allowed format not valid [1] -> [1'000'000'000]")
                    return False
                
                if len(input_list[0].get()) > 0:
                    
                    if input_list_default[0] != input_list[0].get():
                        
                        sql_statements = "SELECT COUNT(*) FROM " + dt.TABLE_NAME_SYS_REDIRECTION_SERVER 
                        sql_statements += " WHERE name = '" + input_list[0].get() + "'"
                
                        if self.CoreInit.data.data_tools.sql_is_count_exist_statements(sql_statements):
                            messagebox.showerror("Error on data validation", "Name definition already exist on database ...")
                            return False
                else:
                    messagebox.showerror("Error on data validation", "No Name defined ...")
                    return False
                
                if input_list_default[2] != ip_port_value: 

                    sql_statements = "SELECT COUNT(*) FROM " + dt.TABLE_NAME_SYS_REDIRECTION_SERVER 
                    sql_statements += " WHERE ip_port = '" + ip_port_value + "'"
                
                    if self.CoreInit.data.data_tools.sql_is_count_exist_statements(sql_statements):
                        messagebox.showerror("Error on data validation", "Ip Port definition already exist ...")
                        return False
            
            return True
        
        def exit_windows():
            
            root.destroy()

        def check_input():

            input_list :list[tk.Entry] = []
            sql_statements :str = ""
    
            input_list.append(val1_input_text_value)
            input_list.append(val2_input_text_value)
            input_list.append(val3_input_text_value)
        
            if is_valid_data_input_value(is_proxy, is_edit, input_list, label_value_list_default):
            
                if is_edit:
                    if is_proxy:
                        
                        sql_statements = "UPDATE " + dt.TABLE_NAME_SYS_PROXY_REQUEST 
                        sql_statements += " SET name = '" + input_list[0].get() + "', "
                        sql_statements += "HTTP = '" + input_list[1].get() + "', "
                        sql_statements += "HTTPS = '" + input_list[2].get() + "' "
                        sql_statements += "WHERE name ='" + label_value_list_default[0] + "' "
                        sql_statements += "AND HTTP = '" + label_value_list_default[1] + "' "
                        sql_statements += "AND HTTPS = '" + label_value_list_default[2] + "' "
                   
                    else:
                        
                        sql_statements = "UPDATE " + dt.TABLE_NAME_SYS_REDIRECTION_SERVER 
                        sql_statements += " SET name = '" + input_list[0].get() + "', "
                        sql_statements += "max_users = " + input_list[1].get() + ", "
                        sql_statements += "ip_port = '" + input_list[2].get() + "' "
                        sql_statements += "WHERE name ='" + label_value_list_default[0] + "' "
                        sql_statements += "AND max_users = " + label_value_list_default[1] + " "
                        sql_statements += "AND ip_port = '" + label_value_list_default[2] + "' "
                        
                else:
                    if is_proxy:
                        
                        sql_statements = "INSERT INTO " + dt.TABLE_NAME_SYS_PROXY_REQUEST 
                        sql_statements += "(name, HTTP, HTTPS) VALUES ('" 
                        sql_statements +=  input_list[0].get() + "','"
                        sql_statements +=  input_list[1].get() + "','"
                        sql_statements +=  input_list[2].get() + "')"
                        
                    else:
                        
                        sql_statements = "INSERT INTO " + dt.TABLE_NAME_SYS_REDIRECTION_SERVER 
                        sql_statements += "(name, max_users, ip_port) VALUES ('" 
                        sql_statements +=  input_list[0].get() + "',"
                        sql_statements +=  input_list[1].get() + ",'"
                        sql_statements +=  input_list[2].get() + "')"
                    
                root.destroy()
                
                self.CoreInit.data.data_tools.sql_execute_statement(sql_statements)

            else:

                root.wm_attributes("-topmost", True) 
                
        root.protocol("WM_DELETE_WINDOW", exit_windows)                
        
        title_label0 = ttk.Label(root, text=windows_title.upper(), font=("Font", 11), background=color_backgroud)
        title_label0.place(x=5,y=7, width=220)
        
        title_label1 = ttk.Label(root, text=label_value_list[0][0], background=color_backgroud)
        title_label1.place(x=5,y=40, width=100)
        
        val1_text = tk.StringVar(root)

        if str(label_value_list[0][1])[1:-1][0:1] == "'":
            val1_text.set(str(label_value_list[0][1])[2:-2])
        else:
            val1_text.set(str(label_value_list[0][1])[1:-1])
        
        val1_input_text_value = tk.Entry(root, textvariable=val1_text)
        val1_input_text_value.place(x=80, y=40, width=165, height=20)
        
        if is_proxy:
            title_label2 = ttk.Label(root, text=label_value_list[1][0], background=color_backgroud)
        else:
            title_label2 = ttk.Label(root, text=str(label_value_list[1][0])[2:-2], background=color_backgroud)
        
        title_label2.place(x=5,y=70, width=100)
        
        val2_text = tk.StringVar(root)

        if is_proxy:
            val2_text.set(str(label_value_list[1][1])[2:-2])
        else:
            val2_text.set(str(label_value_list[1][1])[1:-1])

        if  val2_text.get() == "''":
            val2_text.set("")

        val2_input_text_value = tk.Entry(root, textvariable=val2_text)
        val2_input_text_value.place(x=80, y=70, width=165, height=20)
        
        title_label3 = ttk.Label(root, text=label_value_list[2][0], background=color_backgroud)
        title_label3.place(x=5,y=100, width=115)
        
        val3_text = tk.StringVar(root)
        val3_text.set(str(label_value_list[2][1])[2:-2])

        val3_input_text_value = tk.Entry(root, textvariable=val3_text)
        val3_input_text_value.place(x=80, y=100, width=165, height=20)
        
        change_pwd_button = ttk.Button(root,
                            text=button_title,
                            command=check_input)
        change_pwd_button.place(x=windows_width-171, y=windows_height-35)        
        
        exit_button = ttk.Button(root,
                          text='Exit',
                          command=exit_windows)
        exit_button.place(x=windows_width-91, y=windows_height-35)       
        
        root.mainloop()