import datetime
import threading

import tkinter as tk
from tkinter import ttk, messagebox, DISABLED, ACTIVE, CENTER
from tkinter.filedialog import askopenfilename, askdirectory

import core.CoreInit as ci
import app.tools.WindowsTools as wt   
import core.tools.DataTools as dt
import app.SubWindows.WindowEditProxyRedirect as we

class WebServerFrame():
    
    def __init__(self, CoreInit :ci.CoreInit):
        
        self.CoreInit = CoreInit
        
        self.selection_backup_cycle :str = ""    
        self.selection_redirect_server :str = ""       
        self.selection_use_proxy_balancing :str = ""       
        self.selection_backup_server :str = ""   
        
        self.edit_proxy_windows = None
        self.new_proxy_windows = None
        
        self.edit_redirect_windows = None
        self.new_redirect_windows = None
        
    def create_control_input_value(self, frame_root :tk.Frame, control_list_dict :dict, control_key :str, label_value :str, left :int, top :int):
            control_list_dict[control_key] = wt.WindowsTools.create_input_with_label_complex(
                                                             frame_root, label_value, self.CoreInit.data.admin_server_data, control_key, 
                                                             'gray58', left, top)   
                
    def make_control_input_value(self, frame_root :tk.Frame, control_list_dict :dict,):
            self.create_control_input_value(frame_root, control_list_dict, "server_ip_port","Server Ip Port:",10,10)
            self.create_control_input_value(frame_root, control_list_dict, "max_users_allowed","Max Users Allowed:",10,35)
            self.create_control_input_value(frame_root, control_list_dict, "admin_email","Admin E-Mail:",10,60)
            self.create_control_input_value(frame_root, control_list_dict, "company_name","Company Name:",10,85)
            self.create_control_input_value(frame_root, control_list_dict, "company_address","Company Address:",10,110)
            self.create_control_input_value(frame_root, control_list_dict, "company_contact","Company Contact:",10,135)
            self.create_control_input_value(frame_root, control_list_dict, "smtp_server_ip_port","SMPT Server Ip Port:",10,160)
            self.create_control_input_value(frame_root, control_list_dict, "smtp_user","SMPT User:",10,185)
            self.create_control_input_value(frame_root, control_list_dict, "smtp_password","SMPT Password:",10,210)
            self.create_control_input_value(frame_root, control_list_dict, "smtp_from_email","SMPT From E-Mail:",10,235)
            
    def check_some_input_value(self, web_server_ip_port :str, admin_email :str, smpt_server_ip_port :str, max_user_allowed :str, smpt_email_from :str) -> bool:
        
        if len(web_server_ip_port) == 0:
            messagebox.showerror("Error on update admin data values", "Server Ip Port could be none value ...")
            return False
        
        if not self.CoreInit.is_valid_ip_port_format(web_server_ip_port):
            print(web_server_ip_port)
            messagebox.showerror("Error on update admin data values", "WEB Server Ip Port not valid format [[0..255].[0..255].[0..255].[0..255]]:[0..65535]]")
            return False
            
        if len(smpt_server_ip_port) > 0:
            if not self.CoreInit.is_valid_ip_port_format(smpt_server_ip_port):
                messagebox.showerror("Error on update admin data values", "SMPT Server Ip Port not valid format [[0..255].[0..255].[0..255].[0..255]]:[0..65535]]")
                return False
            
        if len(admin_email) > 0:
             if not self.CoreInit.is_valid_email_format(admin_email):
                messagebox.showerror("Error on update admin data values", "Admin E-Mail format not valid [xxxxx@xxx.xx] -> [xxx.xxxx.x.xx@xxx.xx] No special aplha value admited")
                return False
                
        if not self.CoreInit.is_max_users_allowed(max_user_allowed):
            messagebox.showerror("Error on update admin data values", "Max users allowed format not valid [1] -> [1'000'000'000]")
            return False
        
        if len(smpt_email_from) > 0:
             if not self.CoreInit.is_valid_email_format(smpt_email_from):
                messagebox.showerror("Error on update admin data values", "SMPT From E-Mail format not valid [xxxxx@xxx.xx] -> [xxx.xxxx.x.xx@xxx.xx] No special aplha value admited")
                return False        
        
        return True
        
    def fill_view_list(self, view_list :ttk.Treeview, table_name :str):
        
        data_values_view_list :list = self.CoreInit.data.data_tools.sql_get_execute_statement("SELECT * FROM " + table_name)
        
        for i in range(len(data_values_view_list)):
            view_list.insert('', 'end', text=str(i+1), values=(data_values_view_list[i][1], data_values_view_list[i][2], data_values_view_list[i][3]))   
    
    def proxy_view_list(self, frame_root :tk.Frame, def_button_height :int) -> ttk.Treeview:

        def event_delete_list_multi_hosting():
            
            row_dict :dict = {}
            curItem = view_list.focus()
            
            row_dict = view_list.item(curItem)
            
            if len(list(row_dict["values"])) > 0:
                
                result=messagebox.askyesno(f'Delete Proxy ...','Confirmation to delete ' + str(row_dict["values"][0]) + '?')
            
                if result==True:

                    selected_items = view_list.selection()
                    view_list.delete(*selected_items)

                    value_list :list = list(row_dict["values"])
                    
                    sql_statements :str = ""
                    sql_statements = "DELETE FROM " + dt.TABLE_NAME_SYS_PROXY_REQUEST 
                    sql_statements += " WHERE name ='" + str(value_list[0]) + "'"
                    sql_statements += " AND HTTP ='" + str(value_list[1]) + "'" 
                    sql_statements += " AND HTTPS ='" + str(value_list[2]) + "'"
                    
                    self.CoreInit.data.data_tools.sql_execute_statement(sql_statements)

        def event_insert_list_multi_hosting():            
            
            label_value_list :list[list[str]] = [['NAME:'],['']],[['HTTP:'],['']],[['HTTPS:'],['']]
            
            def detach_process():
                
                if self.new_proxy_windows == None:
                    
                    self.new_proxy_windows = we.EditProxyRedirectWindows
                    self.new_proxy_windows.get_windows(self, True, False, label_value_list)    
                
                    try:
                        wt.WindowsTools.list_view_remove_all_row(view_list)
                        self.fill_view_list(view_list, dt.TABLE_NAME_SYS_PROXY_REQUEST)
                    except:
                        pass
            
            if self.new_proxy_windows == None:
                t = threading.Thread(target=detach_process)
                t.start()
       
        def event_edit_list_multi_hosting():
            
            row_dict :dict = {}
            curItem = view_list.focus()
            
            row_dict = view_list.item(curItem)
            
            if len(row_dict["values"]) > 0:
                         
                label_value_list :list[list[str]] = [['NAME:'],[row_dict["values"][0]]],[['HTTP:'],[row_dict["values"][1]]],[['HTTPS:'],[row_dict["values"][2]]]
                
                def detach_process():
                    
                    if self.edit_proxy_windows == None:
                    
                        self.edit_proxy_windows = we.EditProxyRedirectWindows
                        self.edit_proxy_windows.get_windows(self, True, True, label_value_list)    
                    
                        try:
                            wt.WindowsTools.list_view_remove_all_row(view_list)
                            self.fill_view_list(view_list, dt.TABLE_NAME_SYS_PROXY_REQUEST)
                        except:
                            pass
                        
                        self.edit_proxy_windows = None
                
                if self.edit_proxy_windows == None:
                    t = threading.Thread(target=detach_process)
                    t.start()
                
        tree_left :int  = 450
        tree_top :int = 31 
        tree_height :int = 100
        tree_width :int = 434    
         
        wt.WindowsTools.create_label_base(frame_root, 'PROXY MULTI REQUEST:', 'gray48', tree_left, tree_top-21, 133, 20)
    
        view_list = ttk.Treeview(frame_root, column=("c1", "c2", "c3"), show='headings', height=5, style='Custom.Treeview', selectmode ='browse')
        
        view_list["columns"] = ("1", "2", "3", "4")
        view_list['show'] = 'headings'
        
        view_list.column("# 1", anchor=CENTER, width=134)
        view_list.heading("# 1", text="NAME")
        view_list.column("# 2", anchor=CENTER, width=150)
        view_list.heading("# 2", text="HTTP")
        view_list.column("# 3", anchor=CENTER, width=150)
        view_list.heading("# 3", text="HTTPS")
        
        self.fill_view_list(view_list, dt.TABLE_NAME_SYS_PROXY_REQUEST)
        
        view_list.delete()

        view_list.place(x=tree_left, y=tree_top, height=tree_height, width= tree_width)
        
        verscrlbar = ttk.Scrollbar(frame_root, 
                           orient ="vertical", 
                           command =view_list.yview)
   
        verscrlbar.place(x=tree_left+tree_width, y=tree_top, height=tree_height, width=20)
        
        # DELETE BUTTON LIST MULTI PROXY      
        wt.WindowsTools.create_button_detailed(frame_root, 'DELETE', event_delete_list_multi_hosting, 
                                                                tree_left + tree_width - 66 + 20 , tree_top + tree_height, 66, def_button_height)
        # INSERT BUTTON LIST MULTI PROXY      
        wt.WindowsTools.create_button_detailed(frame_root, 'NEW', event_insert_list_multi_hosting, 
                                                                tree_left + tree_width - 66 - 66 + 20 , tree_top + tree_height, 66, def_button_height)
        # EDIT BUTTON LIST MULTI PROXY      
        wt.WindowsTools.create_button_detailed(frame_root, 'EDIT', event_edit_list_multi_hosting, 
                                                                tree_left + tree_width - 66 - 66 - 66 + 20 , tree_top + tree_height, 66, def_button_height)
        
        return view_list
    
    def redirect_view_list(self, frame_root :tk.Frame, def_button_height :int) -> ttk.Treeview:
        
         # MAKING LIST VIEW FOR REDIRECTING TO OTHER SERVER         
        def event_delete_list_redirect_server():
            
            row_dict :dict = {}
            curItem = view_list.focus()
            
            row_dict = view_list.item(curItem)

            if len(list(row_dict["values"])) > 0:
                
                result=messagebox.askyesno(f'Delete Redirect ...','Confirmation to delete ' + str(row_dict["values"][0]) + '?')
            
                if result==True:
            
                    selected_items = view_list.selection()
                    view_list.delete(*selected_items)

                    value_list :list = list(row_dict["values"])
                    
                    sql_statements :str = ""
                    sql_statements = "DELETE FROM " + dt.TABLE_NAME_SYS_REDIRECTION_SERVER 
                    sql_statements += " WHERE name ='" + str(value_list[0]) + "'"
                    sql_statements += " AND max_users =" + str(value_list[1]) 
                    sql_statements += " AND ip_port ='" + str(value_list[2]) + "'"
                    
                    self.CoreInit.data.data_tools.sql_execute_statement(sql_statements)
            
        def event_insert_list_redirect_server():
            
            label_value_list :list[list[str]] = [['NAME:'],['']],[['MAX USERS:'],['']],[['IP:PORT:'],['']]
            
            def detach_process():
                
                if self.new_redirect_windows == None:
                    
                    self.new_redirect_windows = we.EditProxyRedirectWindows
                    self.new_redirect_windows.get_windows(self, False, False, label_value_list)    
                
                    try:
                        wt.WindowsTools.list_view_remove_all_row(view_list)
                        self.fill_view_list(view_list, dt.TABLE_NAME_SYS_REDIRECTION_SERVER)
                    except:
                        pass
                    
                    self.new_redirect_windows = None
            
            if self.new_redirect_windows == None:
                t = threading.Thread(target=detach_process)
                t.start()

        def event_edit_list_redirect_server():
            
            row_dict :dict = {}
            curItem = view_list.focus()
            
            row_dict = view_list.item(curItem)
            
            if len(row_dict["values"]) > 0:
                         
                label_value_list :list[list[str]] = [['NAME:'],[row_dict["values"][0]]],[['MAX USERS:'],[row_dict["values"][1]]],[['IP:PORT:'],[row_dict["values"][2]]]
                
                def detach_process():
                    
                    if self.edit_redirect_windows == None:
                    
                        self.edit_redirect_windows = we.EditProxyRedirectWindows
                        self.edit_redirect_windows.get_windows(self, False, True, label_value_list)    
                    
                        try:
                            wt.WindowsTools.list_view_remove_all_row(view_list)
                            self.fill_view_list(view_list, dt.TABLE_NAME_SYS_REDIRECTION_SERVER)
                        except:
                            pass
                        
                        self.edit_redirect_windows = None
                
                if self.edit_redirect_windows == None:
                    t = threading.Thread(target=detach_process)
                    t.start()
                
        tree_left :int  = 450
        tree_top :int = 160
        tree_height :int = 100
        tree_width :int = 434 
            
        wt.WindowsTools.create_label_base(frame_root, 'SERVER REDIRECTION IP:', 'gray48', tree_left, tree_top-21, 133, 20)
        
        view_list = ttk.Treeview(frame_root, column=("c1", "c2", "c3"), show='headings', height=5, style='Custom.Treeview', selectmode ='browse')
        
        view_list["columns"] = ("1", "2", "3", "4")
        view_list['show'] = 'headings'
        
        view_list.column("# 1", anchor=CENTER, width=134)
        view_list.heading("# 1", text="NAME")
        view_list.column("# 2", anchor=CENTER, width=150)
        view_list.heading("# 2", text="MAX USERS")
        view_list.column("# 3", anchor=CENTER, width=150)
        view_list.heading("# 3", text="IP:PORT")
        
        self.fill_view_list(view_list, dt.TABLE_NAME_SYS_REDIRECTION_SERVER)
        
        view_list.delete()
      
        view_list.place(x=tree_left, y=tree_top, height=tree_height, width= tree_width)
        
        verscrlbar = ttk.Scrollbar(frame_root, 
                           orient ="vertical", 
                           command =view_list.yview)
   
        verscrlbar.place(x=tree_left+tree_width, y=tree_top, height=tree_height, width=20)
        
        # DELETE BUTTON LIST REDIRECT SERVER     
        wt.WindowsTools.create_button_detailed(frame_root, 'DELETE', event_delete_list_redirect_server, 
                                                                tree_left + tree_width - 66 + 20 , tree_top + tree_height, 66, def_button_height)
        # INSERT BUTTON LIST REDIRECT SERVER      
        wt.WindowsTools.create_button_detailed(frame_root, 'NEW', event_insert_list_redirect_server, 
                                                                tree_left + tree_width - 66 - 66 + 20 , tree_top + tree_height, 66, def_button_height)
        # EDIT BUTTON LIST REDIRECT SERVER      
        wt.WindowsTools.create_button_detailed(frame_root, 'EDIT', event_edit_list_redirect_server, 
                                                                tree_left + tree_width - 66 - 66 - 66 + 20 , tree_top + tree_height, 66, def_button_height)
        return view_list

    def window_server_frame(self, frame_root :tk.Frame, frame_width :int, frame_height :int):
        
        def_button_height :int = 23
        control_list_dict :dict = {}
        file_folder_list_dict :dict = {}
        
        file_folder_list_dict["google_public_storage_path"] = ""
        file_folder_list_dict["backup_path_directory"] = ""
        file_folder_list_dict["python_path"] = ""
        
        # SET BUTTON SAVE AND REFRESH BY MODIFIACTION OR RESET(REFRESH)
        def active_save_refresh(is_activate :bool):
            
            if is_activate:
                button_save["state"] = ACTIVE 
                button_restore["state"] = ACTIVE 
                
                style = ttk.Style()
                style.configure(style='Arrow.TButton', background='red', foreground='red',
                                highlightcolor='red', borderwidth=0,
                
                                focuscolor='red')
                button_save["style"] = 'Arrow.TButton'   
            else:
                button_save["state"] = DISABLED                
                button_restore["state"] = DISABLED
                
                style1 = ttk.Style()
                style1.configure(style='Arrow.TButton', background='gray', foreground='gray',
                        highlightcolor='gray', borderwidth=0,
                        focuscolor='gray')
                
        # SET SELECTED CONTROL FORECOLOR TO RED TO SIGNAL A USER MODIFICATION
        def event_key_release(control_key :str):
            
            if not(control_key == "SERVER_TYPE_SELECTION" or control_key == "BACKUP_TYPE_SELECTION" or control_key == "USE_PROXY_BALANCING"):
                control_list_dict[control_key]["control"].configure(fg='red')
            
            active_save_refresh(True)
                        
        # RESTORE INITIAL DEFAULT VALUE 
        def event_refresh():
            
            self.selection_backup_cycle = ""            
            self.selection_redirect_server  = ""   
            self.selection_use_proxy_balancing = ""           
            self.selection_backup_server = ""   
            
            style1 = ttk.Style()
            style1.configure(style='Arrow.TButton', background='gray', foreground='gray',
                        highlightcolor='gray', borderwidth=0,
                        focuscolor='gray')
            
            for control_key in control_list_dict:    
                control_list_dict[control_key]["control"].configure(fg='black')
                control_list_dict[control_key]["value"].set(self.CoreInit.data.admin_server_data[control_key])

            label_display_google_path.config(text=self.CoreInit.data.admin_server_data["google_public_storage_path"], foreground='black')                
            label_display_backup_path.config(text=self.CoreInit.data.admin_server_data["backup_path_directory"], foreground='black')                
            label_display_python_path.config(text=self.CoreInit.data.admin_server_data["python_path"], foreground='black')                
            
            file_folder_list_dict["google_public_storage_path"] = ""
            file_folder_list_dict["backup_path_directory"] = ""
            file_folder_list_dict["python_path"] = ""
            
            selected_backup_cycle.set(self.CoreInit.data.get_current_backup_definition())
            
            if self.CoreInit.data.admin_server_data["is_redirect_server"] == "TRUE":
                is_redirect_server.set(1)
            else:
                is_redirect_server.set(0)
            select_web_server_type.configure(fg='gray51')
            
            if self.CoreInit.data.admin_server_data["use_proxy_balancing"] == "TRUE":
                use_proxy_balancing.set(1)
            else:
                use_proxy_balancing.set(0)
            select_use_proxy_balancing.configure(fg='gray51')
            
            if self.CoreInit.data.admin_server_data["is_backup_activate"] == "TRUE":
                is_backup_server.set(1)
            else:
                is_backup_server.set(0)
            select_backup_enable.configure(fg='gray51')
            
            wt.WindowsTools.list_view_remove_all_row(proxy_view_list)
            wt.WindowsTools.list_view_remove_all_row(redirect_view_list)
            
            self.fill_view_list(proxy_view_list, dt.TABLE_NAME_SYS_PROXY_REQUEST)
            self.fill_view_list(redirect_view_list, dt.TABLE_NAME_SYS_REDIRECTION_SERVER)
            
            active_save_refresh(False)
        
        # SAVE MODIFICATION BY USER ADMIN    
        def event_save():
            
             if self.check_some_input_value(str(control_list_dict["server_ip_port"]["value"].get()),
                                               str(control_list_dict["admin_email"]["value"].get()),
                                               str(control_list_dict["smtp_server_ip_port"]["value"].get()),
                                               str(control_list_dict["max_users_allowed"]["value"].get()),
                                               str(control_list_dict["smtp_from_email"]["value"].get())):
                             
                result=messagebox.askyesno('Save Modification ...','Confirmation to save all Modification ?')
            
                if result==True:                                
                    
                    for control_key in control_list_dict:
                        self.CoreInit.data.admin_server_data[control_key] = str(control_list_dict[control_key]["value"].get())
                    
                    if len(self.selection_backup_cycle) > 0:
                        self.CoreInit.data.admin_server_data["backup_time_cycle"] = self.CoreInit.data.get_backup_id_by_definition(self.selection_backup_cycle)
                    
                    if len(self.selection_redirect_server) > 0:
                        self.CoreInit.data.admin_server_data["is_redirect_server"] = self.selection_redirect_server
                        
                    if len(self.selection_use_proxy_balancing) > 0:
                        self.CoreInit.data.admin_server_data["use_proxy_balancing"] = self.selection_use_proxy_balancing
                        
                    if len(self.selection_backup_server) > 0:
                        self.CoreInit.data.admin_server_data["is_backup_activate"] = self.selection_backup_server
                    
                    self.CoreInit.data.data_tools.sql_update_all_system_admin_values(self.CoreInit.data.admin_server_data)
                    
                    if len(file_folder_list_dict["google_public_storage_path"]) > 0:
                        self.CoreInit.data.sql_change_admin_value('google_public_storage_path', file_folder_list_dict["google_public_storage_path"])                         
                        
                    if len(file_folder_list_dict["backup_path_directory"]) > 0:
                        self.CoreInit.data.sql_change_admin_value('backup_path_directory', file_folder_list_dict["backup_path_directory"])                         
                        
                    if len(file_folder_list_dict["python_path"]) > 0:
                        self.CoreInit.data.sql_change_admin_value('python_path', file_folder_list_dict["python_path"])                         
                    
                    event_refresh()
         
        # GOOGLE PATH DISPLAY AND SELECTION
        def event_select_google_path():
            
            directory_name  = askdirectory(initialdir='\\', title="Select GOOGLE directory full path ...")
            
            if len(directory_name) > 0:
                
                label_display_google_path.config(text=directory_name, foreground='red')
                active_save_refresh(True)
                file_folder_list_dict["google_public_storage_path"] = directory_name            
                
        wt.WindowsTools.create_button_detailed(frame_root, '...', event_select_google_path, frame_width - 185, frame_height - 81, 30, 19)
        wt.WindowsTools.create_label_base(frame_root, 'GOOGLE PATH:', 'gray48', 10, frame_height - 82, 112, 20)
        label_display_google_path = wt.WindowsTools.create_label_base(frame_root, self.CoreInit.data.admin_server_data["google_public_storage_path"], 
                                                                      'gray58', 127, frame_height - 82, 603, 20)
        # BACKUP PATH DISPLAY AND SELECTION
        def event_select_backup_path():
            
            directory_name = askdirectory(initialdir='\\', title="Select BackUp directory full path ...")
            
            if len(directory_name) > 0:
                
                label_display_backup_path.config(text=directory_name, foreground='red')
                active_save_refresh(True)
                file_folder_list_dict["backup_path_directory"] = directory_name            
                
        wt.WindowsTools.create_button_detailed(frame_root, '...', event_select_backup_path, frame_width - 185, frame_height - 57, 30, 19)
        wt.WindowsTools.create_label_base(frame_root, 'BACKUP PATH:', 'gray48', 10, frame_height - 58, 112, 20)
        label_display_backup_path = wt.WindowsTools.create_label_base(frame_root, self.CoreInit.data.admin_server_data["backup_path_directory"], 
                                                                      'gray58', 127, frame_height - 58, 603, 20)
        # PYTHON PATH DISPLAY AND SELECTION
        def event_select_python_path():
            
            file_name = askopenfilename(initialdir='\\', filetypes=[("PYTHON","python.exe")], title="Select Python.exe full path name ...")
            
            if len(file_name) > 0:
            
                label_display_python_path.config(text=file_name, foreground='red')
                active_save_refresh(True)
                file_folder_list_dict["python_path"] = file_name                
                
        wt.WindowsTools.create_button_detailed(frame_root, '...', event_select_python_path, frame_width - 185, frame_height - 33, 30, 19)
        wt.WindowsTools.create_label_base(frame_root, 'PYTHON PATH:', 'gray48', 10, frame_height - 34, 112, 20)
        label_display_python_path = wt.WindowsTools.create_label_base(frame_root, self.CoreInit.data.admin_server_data["python_path"], 
                                                                      'gray58', 127, frame_height - 34, 603, 20)
        # MAKING INPUT DATA VALUE WITH LABEL
        self.make_control_input_value(frame_root, control_list_dict)
        control_list_dict["smtp_password"]["control"].config(show="*")
            
        def add_event_key_release(control_key :str):
            control_list_dict[control_key]["control"].bind('<KeyRelease>',lambda a: event_key_release(control_key))
        
        for control_key in control_list_dict.keys():
            add_event_key_release(control_key)
            
        # REFRESH BUTTON        
        button_restore = wt.WindowsTools.create_button_detailed(frame_root, 'RESTORE', event_refresh, 
                                                                frame_width - 82 - 66 - 3, frame_height - 36, 66, def_button_height)
        button_restore["state"] = DISABLED
        
        # SAVE BUTTON        
        button_save = wt.WindowsTools.create_button_detailed(frame_root, 'SAVE', event_save, frame_width - 82, 
                                                             frame_height - 36, 66, def_button_height)
        button_save["state"] = DISABLED
    
        # LIST VIEW FOR PROXY AND REDIRECT LIST SERVER IP AND PORT AND DESCRIPTION 
        proxy_view_list = self.proxy_view_list(frame_root, def_button_height)
        redirect_view_list = self.redirect_view_list(frame_root, def_button_height)
        
        # CHECKBOX TO SELECT IF IS A REDIRECT SERVER                
        def active_redirect_server():
            active_save_refresh(True)
            select_web_server_type.configure(fg='red')            
            event_key_release("SERVER_TYPE_SELECTION")            
            if (is_redirect_server.get() == 1):
                self.selection_redirect_server = "TRUE"
            else:
                self.selection_redirect_server = "FALSE"
                
        is_redirect_server = tk.IntVar()
        if self.CoreInit.data.admin_server_data["is_redirect_server"] == "TRUE":
            is_redirect_server.set(1)
        else:
            is_redirect_server.set(0)
            
        select_web_server_type = tk.Checkbutton(frame_root, text='IS A REDIRECT WEB SERVER', 
                                                variable=is_redirect_server, command=active_redirect_server, 
                                                background='gray23', foreground='gray51', onvalue=1, offvalue=0)
        select_web_server_type.place(x=737, y=5)
        
        # CHECKBOX TO SELECT TO USE PROXY BALANCING
        def active_use_proxy_balancing():
            active_save_refresh(True)
            select_use_proxy_balancing.configure(fg='red')            
            event_key_release("USE_PROXY_BALANCING")            
            if (use_proxy_balancing.get() == 1):
                self.selection_use_proxy_balancing = "TRUE"
            else:
                self.selection_use_proxy_balancing = "FALSE"
                
        use_proxy_balancing = tk.IntVar()
        if self.CoreInit.data.admin_server_data["use_proxy_balancing"] == "TRUE":
            use_proxy_balancing.set(1)
        else:
            use_proxy_balancing.set(0)
            
        select_use_proxy_balancing = tk.Checkbutton(frame_root, text='USE PROXY BALANCING', 
                                                    variable=use_proxy_balancing, command=active_use_proxy_balancing, 
                                                    background='gray23', foreground='gray51', onvalue=1, offvalue=0)
        select_use_proxy_balancing.place(x=585, y=5)
        
        # CHECKBOX TO SELECT IF AUTO BACKUP IS ENABLE
        def active_backup_server():
            active_save_refresh(True)
            select_backup_enable.configure(fg='red')            
            event_key_release("BACKUP_TYPE_SELECTION")
            if (is_backup_server.get() == 1):
                self.selection_backup_server = "TRUE"
            else:
                self.selection_backup_server = "FALSE"
                
        is_backup_server = tk.IntVar()        
        if self.CoreInit.data.admin_server_data["is_backup_activate"] == "TRUE":
            is_backup_server.set(1)
        else:
            is_backup_server.set(0)
        
        select_backup_enable = tk.Checkbutton(frame_root, text='ACTIVATE BACKUP', variable=is_backup_server, command=active_backup_server, 
                                              background='gray23', foreground='gray51', onvalue=1, offvalue=0)
        select_backup_enable.place(x=445, y=frame_height - 109)
        
        # DISPLAY LAST AND FIRST LOG WEB SERVER
        if len(self.CoreInit.data.admin_server_data["first_server_start_date"]) > 0:
            wt.WindowsTools.create_label_base(frame_root, 'FIRST:' + self.CoreInit.data.admin_server_data["first_server_start_date"], 
                                              'gray48', 768, frame_height - 80, 136, 20)    
        else:
            wt.WindowsTools.create_label_base(frame_root, 'FIRST ' + str(datetime.datetime.now()).split(".")[0].replace("-","."), 
                                              'gray48', 768, frame_height - 80, 136, 20)
                
        if len(self.CoreInit.data.admin_server_data["last_server_start_date"]) > 0:
            wt.WindowsTools.create_label_base(frame_root, 'LAST: ' + self.CoreInit.data.admin_server_data["last_server_start_date"], 
                                              'gray48', 768, frame_height - 58, 136, 20)    
        else:
            wt.WindowsTools.create_label_base(frame_root, 'LAST  ' + str(datetime.datetime.now()).split(".")[0].replace("-","."), 
                                              'gray48', 768, frame_height - 58, 136, 20)    
            
        # COMBOBOX TO SELECT BACKUP CYCLE
        selected_backup_cycle = tk.StringVar(frame_root)
        backup_cycle_selection = ttk.Combobox(frame_root, textvariable=selected_backup_cycle)

        backup_cycle_selection['values'] = tuple(self.CoreInit.data.data_tools.get_default_values_backup_definition())
        backup_cycle_selection['state'] = 'readonly'
        backup_cycle_selection.place(x=210+10, y=260, height=23, width=220)
        
        def backup_cycle_changed(event):
            active_save_refresh(True)
            self.selection_backup_cycle = selected_backup_cycle.get()

        backup_cycle_selection.bind('<<ComboboxSelected>>', backup_cycle_changed)
        selected_backup_cycle.set(self.CoreInit.data.get_current_backup_definition())
        
        wt.WindowsTools.create_label_base(frame_root, 'Back Up Cycle:', 'gray58', 10, 260, 200, 20)
        