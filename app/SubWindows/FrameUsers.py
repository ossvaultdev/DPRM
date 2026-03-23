from tkinter import ttk, messagebox, CENTER 
import tkinter as tk
import threading

import core.CoreInit as ci
import core.tools.DataDefault as df

import app.tools.WindowsTools as wt   
import app.SubWindows.WindowsEditUser as we

import app.SubWindows.WindowsUserPwd as up

class UsersFrame():
    
    def __init__(self, CoreInit :ci.CoreInit):
        
        self.CoreInit = CoreInit
        
        self.add_new_user_windows = None
        self.edit_user_windows = None
        
        self.is_on_show_active_user :bool = True
        
    def redirect_view_list(self, frame_root :tk.Frame, def_button_height :int) -> ttk.Treeview:
    
        def event_delete_user():
            
            row_dict :dict = {}
            curItem = view_list.focus()
            
            row_dict = view_list.item(curItem)

            if len(list(row_dict["values"])) > 0:

                if str(row_dict["values"][1]) == "FALSE":
                
                    messagebox.showerror("Delete User","User can not be deleted, already deleted")
                    
                else:

                    result=messagebox.askyesno(f'Delete User ...', 
                                                'Confirmation to delete User: ' + str(row_dict["values"][2]) + '?')
                
                    if result==True:

                        all_root_items = view_list.get_children()
                        view_list.delete(*all_root_items)

                        self.CoreInit.data.data_tools.desactive_user(str(row_dict["values"][0]))

                        user_list :list = self.CoreInit.data.data_tools.get_user_list_values()

                        for i in range(len(user_list)):
                            view_list.insert('', 'end', text=str(i+1), 
                                                        values=(user_list[i][0], ["TRUE" if user_list[i][10] == 1 else "FALSE"], 
                                                                user_list[i][1], user_list[i][8], user_list[i][9], 
                                                                user_list[i][4], user_list[i][5], 
                                                                user_list[i][6], user_list[i][7]))
                        view_list.delete()

        def event_add_new_user():
            
            def detach_process():
                
                if self.add_new_user_windows == None:
                    
                    self.add_new_user_windows = we.EditUsertWindows
                    self.add_new_user_windows.get_windows(self,"1", False)
                
                    user_list :list = self.CoreInit.data.data_tools.get_user_list_values()
                    
                    all_root_items = view_list.get_children()
                    view_list.delete(*all_root_items)
                    
                    for i in range(len(user_list)):
                        view_list.insert('', 'end', text=str(i+1), 
                                                    values=(user_list[i][0], ["TRUE" if user_list[i][10] == 1 else "FALSE"], 
                                                            user_list[i][1], user_list[i][8], user_list[i][9], 
                                                            user_list[i][4], user_list[i][5], 
                                                            user_list[i][6], user_list[i][7]))
                        
                    label_first_name.config(text = "...")
                    label_last_name.config(text = "...")
                    label_address.config(text = "...")
                    label_country.config(text = "...")        
                        
                    view_list.delete()                        
                    self.add_new_user_windows = None
            
            if self.add_new_user_windows == None:
                t = threading.Thread(target=detach_process)
                t.start()
            
        def event_edit_user():
            
            def detach_process():
                
                if self.edit_user_windows == None:
                    
                    row_dict :dict = {}
                    curItem = view_list.focus()
            
                    row_dict = view_list.item(curItem)

                    if len(list(row_dict["values"])) > 0:

                        if str(row_dict["values"][1]) == "FALSE":
                            
                            messagebox.showerror("Update User","User Deleted can not be changed")

                        else:
                            
                            self.edit_user_windows = we.EditUsertWindows
                            self.edit_user_windows.get_windows(self,str(row_dict["values"][0]), True)
                            
                            all_root_items = view_list.get_children()
                            view_list.delete(*all_root_items)
                        
                            user_list :list = self.CoreInit.data.data_tools.get_user_list_values()
                            
                            for i in range(len(user_list)):
                                view_list.insert('', 'end', text=str(i+1), 
                                                            values=(user_list[i][0], ["TRUE" if user_list[i][10] == 1 else "FALSE"], 
                                                                    user_list[i][1], user_list[i][8], user_list[i][9], 
                                                                    user_list[i][4], user_list[i][5], 
                                                                    user_list[i][6], user_list[i][7]))
                            view_list.delete()                                
                            
                            label_first_name.config(text = "...")
                            label_last_name.config(text = "...")
                            label_address.config(text = "...")
                            label_country.config(text = "...")        
                            
                            self.edit_user_windows = None

            if self.edit_user_windows == None:
                t = threading.Thread(target=detach_process)
                t.start()
        
        def event_reset_pwd_user():
            
            row_dict :dict = {}
            curItem = view_list.focus()

            row_dict = view_list.item(curItem)

            if len(list(row_dict["values"])) > 0:
                
                user_reset_password = up.PasswordWindows
                user_reset_password.get_windows(self, str(row_dict["values"][0]))
            
        def event_show_delete_user():
            
            all_root_items = view_list.get_children()
            view_list.delete(*all_root_items)
            
            self.is_on_show_active_user = not self.is_on_show_active_user
            
            user_list :list = self.CoreInit.data.data_tools.get_user_list_values(self.is_on_show_active_user)
            
            if self.is_on_show_active_user:
                bt_show_delete_user.configure(text="SHOW DELETE USER")
            else:
                bt_show_delete_user.configure(text="SHOW ACTIVE USER")

            for i in range(len(user_list)):
                view_list.insert('', 'end', text=str(i+1), 
                                            values=(user_list[i][0], ["TRUE" if user_list[i][10] == 1 else "FALSE"], 
                                                    user_list[i][1], user_list[i][8], user_list[i][9], 
                                                    user_list[i][4], user_list[i][5], 
                                                    user_list[i][6], user_list[i][7]))
            view_list.delete()
            
        tree_left :int  = 10
        tree_top :int = 35
        tree_height :int = 240 
        tree_width :int = 875  
            
        wt.WindowsTools.create_label_base(frame_root, 'USER DEFINITIONS:', 'gray48', tree_left, tree_top-21, 108, 20)

        view_list = ttk.Treeview(frame_root, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "C9"), 
                                 show='headings', height=5, style='Custom.Treeview', selectmode ='browse')
        
        view_list["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
        view_list['show'] = 'headings'
        
        view_list.column("# 1", anchor=CENTER, width=110)
        view_list.heading("# 1", text="USER ID")
        view_list.column("# 2", anchor=CENTER, width=150)
        view_list.heading("# 2", text="ACTIVE")
        view_list.column("# 3", anchor=CENTER, width=250)
        view_list.heading("# 3", text="NAME")
        view_list.column("# 4", anchor=CENTER, width=200)
        view_list.heading("# 4", text="EMAIL")
        view_list.column("# 5", anchor=CENTER, width=200)
        view_list.heading("# 5", text="PHONE")

        view_list.column("# 6", anchor=CENTER, width=150)
        view_list.heading("# 6", text="FIRST NAME")
        view_list.column("# 7", anchor=CENTER, width=300)
        view_list.heading("# 7", text="LAST NAME")
        view_list.column("# 8", anchor=CENTER, width=150)
        view_list.heading("# 8", text="ADDRESS")
        view_list.column("# 9", anchor=CENTER, width=150)
        view_list.heading("# 9", text="COUNTRY")

        user_list :list = self.CoreInit.data.data_tools.get_user_list_values()

        for i in range(len(user_list)):
            view_list.insert('', 'end', text=str(i+1), 
                                        values=(user_list[i][0], ["TRUE" if user_list[i][10] == 1 else "FALSE"], 
                                                user_list[i][1], user_list[i][8], user_list[i][9], 
                                                user_list[i][4], user_list[i][5], 
                                                user_list[i][6], user_list[i][7]))

        view_list.delete()
    
        view_list.place(x=tree_left, y=tree_top, height=tree_height, width= tree_width)
        
        verscrlbar = ttk.Scrollbar(frame_root, 
                        orient ="vertical", 
                        command =view_list.yview)

        verscrlbar.place(x=tree_left+tree_width, y=tree_top, height=tree_height, width=20)
        
        # DELETE USER BUTTON 
        wt.WindowsTools.create_button_detailed(frame_root, 'DELETE', event_delete_user, 
                                               tree_left + tree_width - 66 + 20 , 
                                               tree_top + tree_height, 66, def_button_height)
        # INSERT NEW USER BUTTON 
        wt.WindowsTools.create_button_detailed(frame_root, 'NEW', event_add_new_user, 
                                               tree_left + tree_width - 66 - 66 + 20 , 
                                               tree_top + tree_height, 66, def_button_height)
        # EDIT USER BUTTON 
        wt.WindowsTools.create_button_detailed(frame_root, 'EDIT', event_edit_user, 
                                               tree_left + tree_width - 66 - 66 - 66 + 20 , 
                                               tree_top + tree_height, 66, def_button_height)
        
        # RESET PASSWORD USER BUTTON 
        wt.WindowsTools.create_button_detailed(frame_root, 'RESET PASSWORD', event_reset_pwd_user, 
                                               tree_left + tree_width - 66 - 66 - 66 + 20 - 120, 
                                               tree_top + tree_height, 120, def_button_height)
        
        # SHOW DELETED USER
        bt_show_delete_user = wt.WindowsTools.create_button_detailed(frame_root, 'SHOW DELETE USER', event_show_delete_user, 
                                               tree_left + tree_width - 66 - 66 - 66 + 20 - 120 - 120, 
                                               tree_top + tree_height, 120, def_button_height)
        
    
        top_label :int = tree_top + tree_height + 10
        left_label :int = 10
        width_value_label :int = 250
        
        wt.WindowsTools.create_label_base(frame_root, 'FIRST NAME:', 'gray48', left_label, top_label, 112, 20)
        label_first_name = wt.WindowsTools.create_label_base(frame_root, "...", 'white', left_label + 115, 
                                                             top_label, width_value_label, 20)
 
        wt.WindowsTools.create_label_base(frame_root, 'LAST NAME:', 'gray48', left_label, top_label + 24, 112, 20)
        label_last_name = wt.WindowsTools.create_label_base(frame_root, "...", 'white', left_label + 115, 
                                                            top_label + 24, width_value_label, 20)

        wt.WindowsTools.create_label_base(frame_root, 'ADDRESS:', 'gray48', left_label, top_label + 48, 112, 20)
        label_address = wt.WindowsTools.create_label_base(frame_root, "...", 'white', left_label + 115, 
                                                          top_label + 48, width_value_label, 20)
        
        wt.WindowsTools.create_label_base(frame_root, 'COUNTRY:', 'gray48', left_label + 120 + width_value_label, top_label + 48, 112, 20)
        label_country = wt.WindowsTools.create_label_base(frame_root, "...", 'white', left_label + 115 + 120 + width_value_label, 
                                                          top_label + 48, width_value_label - 38, 20)

        def displaySelectedItem(a):

            try:

                selectedItem = view_list.selection()[0]

                label_first_name.config(text = view_list.item(selectedItem)['values'][5])
                label_last_name.config(text = view_list.item(selectedItem)['values'][6])
                label_address.config(text = view_list.item(selectedItem)['values'][7])
                
                for i in range(len(df.DEFAULT_DATA_USER_COUNTRY_DEF)):
                    if list(df.DEFAULT_DATA_USER_COUNTRY_DEF[i])[0] == view_list.item(selectedItem)['values'][8]:
                        label_country.config(text = list(df.DEFAULT_DATA_USER_COUNTRY_DEF[i])[1])        
                        break
            except:
                pass

        view_list.bind("<<TreeviewSelect>>", displaySelectedItem)

        return view_list
        
    def windows_users_frame(self, frame_root :tk.Frame, frame_width :int, frame_height :int):
        
        def_button_height :int = 23
        
        proxy_view_list = self.redirect_view_list(frame_root, def_button_height)
        