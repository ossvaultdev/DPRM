from tkinter.filedialog import askopenfilename
import webbrowser
import subprocess
import threading

import os
import sys

import core.CoreInit as ci
import core.tools.Constant as cs

import app.SubWindows.WindowPassword as pw
import app.tools.WindowsTools as wt   
import app.SubWindows.FrameWebServer as wa
import app.SubWindows.FrameUsers as wu
import app.SubWindows.FrameStatistics as ws

class AdminWindows():
    
    def __init__(self, CoreInit :ci.CoreInit):
        
        self.CoreInit = CoreInit
                
    def get_windows(self):
        
        windows_width :int = 940
        windows_height :int = 450
        
        SubWindowsServer = wa.WebServerFrame(self.CoreInit)
        SubUsers = wu.UsersFrame(self.CoreInit)
        SubStatistics = ws.StatisticsFrame(self.CoreInit)
        
        root = wt.WindowsTools.create_window_base(cs.ASCDEV_SYSTEM_COPYRIGHT + "  " + cs.WIN_ADM_TITLE_WINDOWS , windows_width, windows_height)
        root.iconbitmap(os.path.join(self.CoreInit.common_root_ini_path, "icon", "dprm_main.ico"))
        
        # WINDOWS EVENT MAIN SECTION
        def event_select_windows_frame(frame_position :int):
        
            if frame_position == cs.WIN_ADM_SERVER_FRAME_ID:
                server_frame.place(width=windows_width-20, height=windows_height-80)
                users_frame.place(width=0, height=0) 
                statistic_frame.place(width=0, height=0)    
                
            if frame_position == cs.WIN_ADM_USERS_FRAME_ID:
                server_frame.place(width=0, height=0)    
                users_frame.place(width=windows_width-20, height=windows_height-80) 
                statistic_frame.place(width=0, height=0)    
                
            if frame_position == cs.WIN_ADM_STATISTICS_FRAME_ID:
                server_frame.place(width=0, height=0)    
                users_frame.place(width=0, height=0) 
                statistic_frame.place(width=windows_width-20, height=windows_height-80)
                
        def event_change_password():
            
            if not self.CoreInit.admin_pwd_change:
                self.CoreInit.admin_pwd_change = True
                password_windows = pw.PasswordWindows
                password_windows.get_windows(self)
                
        def event_select_server_path():
            filename = askopenfilename(initialdir="\\",                                                             
                                       filetypes=[("PYTHON","DPRM_Web.py")], 
                                       title="Select DPRM_Web.py full path name ...")
            if len(filename) > 0:
                label_display_server_path.config(text=filename)    
                self.CoreInit.data.sql_change_admin_value('web_server_path', filename)                 
                
        def thread_call_start_server():
            full_path_cmd_server :str = self.CoreInit.data.get_full_command_launch_server()
            if len(full_path_cmd_server) > 0:
                if len(self.CoreInit.data.admin_server_data["server_ip_port"]) > 0:
                    url = "http://127.0.0.1:"  
                    url += str(self.CoreInit.data.admin_server_data["server_ip_port"]).split(":")[1]
                    webbrowser.open(url, new=0, autoraise=True)
                subprocess.run(["powershell", full_path_cmd_server], shell=True)
                
        def event_start_server():       
            thread_start_server = threading.Thread(target=thread_call_start_server)
            thread_start_server.start()
                        
        # WINDOWS FRAME MAIN SECTION
        server_frame = wt.WindowsTools.create_frame_base(root, cs.GUI_COLOR_BASE_FRAME_BACK_COLOR, 
                                                         10, 40, windows_width-20, windows_height-80)
        
        users_frame = wt.WindowsTools.create_frame_base(root, cs.GUI_COLOR_BASE_FRAME_BACK_COLOR, 
                                                        10, 40, windows_width-20, windows_height-80)
        
        statistic_frame = wt.WindowsTools.create_frame_base(root, cs.GUI_COLOR_BASE_FRAME_BACK_COLOR, 
                                                            10, 40, windows_width-20, windows_height-80)
        
        users_frame.place(width=0, height=0)    
        statistic_frame.place(width=0, height=0)    

        SubWindowsServer.window_server_frame(server_frame, windows_width-20, windows_height-80)
        SubUsers.windows_users_frame(users_frame, windows_width-20, windows_height-80)
        SubStatistics.windows_statistics_frame(statistic_frame, windows_width-20, windows_height-80)
        
        wt.WindowsTools.create_button_base(root, '  WEB SERVER  ', 
                                           lambda:event_select_windows_frame(cs.WIN_ADM_SERVER_FRAME_ID), 14, 10)
        
        wt.WindowsTools.create_button_base(root, '  USERS  ', 
                                           lambda:event_select_windows_frame(cs.WIN_ADM_USERS_FRAME_ID), 104, 10)
        
        wt.WindowsTools.create_button_base(root, '  STATISTICS  ', 
                                           lambda:event_select_windows_frame(cs.WIN_ADM_STATISTICS_FRAME_ID), 182, 10)
        
        # CHANGE PASSWORD BUTTON
        wt.WindowsTools.create_button_base(root, 'Change Password', event_change_password, windows_width-120, 10)                

        # START SERVERBUTTON 
        wt.WindowsTools.create_button_base(root, ' START WEB SERVER ', event_start_server, 15, windows_height-35)
        # SERVER PATH SELECTION
        wt.WindowsTools.create_button_detailed(root, '...', event_select_server_path, 
                                               windows_width-127, windows_height - 32, 30, 19)                
        
        label_display_server_path = wt.WindowsTools.create_label_base(root, 
                                                                      self.CoreInit.data.admin_server_data["web_server_path"], 
                                                                      'gray58', 138, windows_height - 32, 670, 20)
        # EXIT BUTTON 
        wt.WindowsTools.create_button_base(root, 'Exit', sys.exit, windows_width-90, windows_height-35)                
        
        root.mainloop()    