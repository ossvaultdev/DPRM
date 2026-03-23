from tkinter import ttk, CENTER 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg
        )

import tkinter as tk
import matplotlib 
import numpy as np
import matplotlib.ticker as ticker

matplotlib.use('TkAgg')

import core.CoreInit as ci
import app.tools.WindowsTools as wt   

class StatisticsFrame():
    
    def __init__(self, CoreInit :ci.CoreInit):
        
        self.CoreInit = CoreInit
        
    def server_view_list(self, frame_root :tk.Frame) -> ttk.Treeview:
    
        tree_left :int  = 10
        tree_top :int = 30
        tree_height :int = 150
        tree_width :int = 434  
            
        wt.WindowsTools.create_label_base(frame_root, 'SERVER WEB LOG:', 'gray48', tree_left, tree_top-21, 105, 20)
        
        view_list_server = ttk.Treeview(frame_root, column=("c1", "c2", "c3", "c4"), show='headings', 
                                        height=5, style='Custom.Treeview', selectmode ='browse')
        
        view_list_server["columns"] = ("1", "2", "3")
        view_list_server['show'] = 'headings'
        
        view_list_server.column("# 1", anchor=CENTER, width=60)
        view_list_server.heading("# 1", text="TYPE")
        view_list_server.column("# 2", width=200)
        view_list_server.heading("# 2", text="DESCRIPTION")
        view_list_server.column("# 3", anchor=CENTER, width=150)
        view_list_server.heading("# 3", text="DATE")
        
        server_log_list :list = self.CoreInit.data.data_tools.get_server_log_values()
        
        for i in range(len(server_log_list)):
            view_list_server.insert('', 'end', text=str(i+1), 
                                    values=(server_log_list[i][1], 
                                            str(server_log_list[i][2]).upper(), 
                                            server_log_list[i][3], 
                                            str(server_log_list[i][3]).split(".")[0]))

        view_list_server.delete()
    
        view_list_server.place(x=tree_left, y=tree_top, height=tree_height, width= tree_width)
        
        verscrlbar = ttk.Scrollbar(frame_root, 
                        orient ="vertical", 
                        command =view_list_server.yview)

        verscrlbar.place(x=tree_left+tree_width, y=tree_top, height=tree_height, width=20)
    
        return view_list_server
    
    def user_view_list(self, frame_root :tk.Frame) -> ttk.Treeview:
    
        tree_left :int  = 10
        tree_top :int = 205
        tree_height :int = 150
        tree_width :int = 434  
            
        wt.WindowsTools.create_label_base(frame_root, 'USERS LOG:', 'gray48', tree_left, tree_top-21, 105, 20)
        
        view_list_users = ttk.Treeview(frame_root, column=("c1", "c2", "c3", "c4"), 
                                       show='headings', height=5, style='Custom.Treeview', selectmode ='browse')
        
        view_list_users["columns"] = ("1", "2", "3", "4")
        view_list_users['show'] = 'headings'
        
        view_list_users.column("# 1", anchor=CENTER, width=60)
        view_list_users.heading("# 1", text="USER ID")
        view_list_users.column("# 2", anchor=CENTER, width=150)
        view_list_users.heading("# 2", text="USER IP")
        view_list_users.column("# 3", width=60)
        view_list_users.heading("# 3", text="TYPE")
        view_list_users.column("# 4", anchor=CENTER, width=150)
        view_list_users.heading("# 4", text="DATE")
        
        user_log_list :list = self.CoreInit.data.data_tools.get_user_log_values()
        
        for i in range(len(user_log_list)):
            view_list_users.insert('', 'end', text=str(i+1), 
                                    values=(user_log_list[i][1], 
                                            user_log_list[i][2], 
                                            user_log_list[i][3], 
                                            str(user_log_list[i][5]).split(".")[0]))

        view_list_users.delete()
    
        view_list_users.place(x=tree_left, y=tree_top, height=tree_height, width= tree_width)
        
        verscrlbar = ttk.Scrollbar(frame_root, 
                        orient ="vertical", 
                        command =view_list_users.yview)

        verscrlbar.place(x=tree_left+tree_width, y=tree_top, height=tree_height, width=20)
    
        return view_list_users
        
    def windows_statistics_frame(self, frame_root :tk.Frame, frame_width :int, frame_height :int):

        self.server_view_list(frame_root)
        self.user_view_list(frame_root)
        
        tree_left :int  = 485
        tree_top :int = 30
        tree_height :int = 305
        
        wt.WindowsTools.create_label_base(frame_root, 'USERS STATISTICS:', 'gray48', tree_left, tree_top-21, 106, 20)

        self.display_user_by_country_graph_pie(frame_root)
        
        def event_show_graph_a():
            self.display_user_by_country_graph_pie(frame_root)
            
        def event_show_graph_b():
            self.display_new_user_by_date_graph_bar(frame_root)
            
        def event_show_graph_c():
            self.display_new_user_accumulation_by_date_graph_line(frame_root)
            
        def event_show_graph_d():
            self.display_user_login_by_date_graph_bar(frame_root)
        
        wt.WindowsTools.create_button_detailed(frame_root, 'COUNTRY', event_show_graph_a, 
                                                                tree_left , tree_top + tree_height, 102- 2, 23)
        
        wt.WindowsTools.create_button_detailed(frame_root, 'NEW USER', event_show_graph_b, 
                                                                tree_left + 102 , tree_top + tree_height, 102 - 2, 23)
        
        wt.WindowsTools.create_button_detailed(frame_root, 'ACCUMULATE', event_show_graph_c, 
                                                                tree_left + 102 + 102, tree_top + tree_height, 102 - 2, 23)
        
        wt.WindowsTools.create_button_detailed(frame_root, 'LOGIN', event_show_graph_d, 
                                                                tree_left + 102 + 102 + 102, tree_top + tree_height, 102, 23)
        
                
    def display_user_by_country_graph_pie(self, frame_root :tk.Frame):
        
        figure = Figure(figsize=(8, 8), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, frame_root)
        axes = figure.add_subplot()
        
        user_country :list = self.CoreInit.data.data_tools.get_user_grouped_by_country()
        user_country_value :list = []
        user_country_name :list = []

        for i in range(len(user_country)):
            user_country_value.append(int(list(user_country[i])[0]))
            user_country_name.append(str(list(user_country[i])[1]))
        
        y = np.array(user_country_value)
        mylabels = user_country_name
        
        axes.pie(y, labels = mylabels, startangle = 90, autopct='%1.1f%%')
        axes.set_title('USER BY COUNTRY', weight='bold', size=14)

        figure_canvas.get_tk_widget().place(x=485, y=31, height=300, width=410)
        
    def display_new_user_by_date_graph_bar(self, frame_root :tk.Frame):
        
        figure = Figure(figsize=(8, 8), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, frame_root)
        axes = figure.add_subplot()
        
        new_user_date :list = self.CoreInit.data.data_tools.get_new_user_grouped_by_date()
        new_user_date_value :list = []
        new_user_date_name :list = []

        for i in range(len(new_user_date)):
            new_user_date_value.append(int(list(new_user_date[i])[0]))
            new_user_date_name.append(str(list(new_user_date[i])[1]))
        
        Users = np.array(new_user_date_value)
        Dates = new_user_date_name
        
        axes.bar(Dates, Users)
        axes.set_title('NEW USER BY DATE', weight='bold', size=14)
        axes.set_ylabel('USERS')
        
        figure.autofmt_xdate()

        figure_canvas.get_tk_widget().place(x=485, y=31, height=300, width=410)
        
    def display_new_user_accumulation_by_date_graph_line(self, frame_root :tk.Frame):
        
        figure = Figure(figsize=(8, 8), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, frame_root)
        axes = figure.add_subplot()
        
        new_user_date :list = self.CoreInit.data.data_tools.get_new_user_grouped_by_date()
        new_user_date_value :list = []
        new_user_date_name :list = []

        user_accumulate :int = 0
        for i in range(len(new_user_date)):
            user_accumulate += int(list(new_user_date[i])[0])
            new_user_date_value.append(user_accumulate)
            new_user_date_name.append(str(list(new_user_date[i])[1]))
        
        Users = np.array(new_user_date_value)
        Dates = new_user_date_name
        
        axes.plot(Dates, Users)
        axes.set_title('ACCUMULATE NEW USER BY DATE', weight='bold', size=14)
        axes.set_ylabel('USERS')
        
        figure.autofmt_xdate()

        figure_canvas.get_tk_widget().place(x=485, y=31, height=300, width=410)
        
    def display_user_login_by_date_graph_bar(self, frame_root :tk.Frame):
        
        figure = Figure(figsize=(8, 8), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, frame_root)
        axes = figure.add_subplot()
        
        new_user_date :list = self.CoreInit.data.data_tools.get_login_user_grouped_by_date()
        new_user_date_value :list = []
        new_user_date_name :list = []

        for i in range(len(new_user_date)):
            new_user_date_value.append(int(list(new_user_date[i])[0]))
            new_user_date_name.append(str(list(new_user_date[i])[1]))
        
        Users = np.array(new_user_date_value)
        Dates = new_user_date_name
        
        axes.bar(Dates, Users)
        axes.set_title('LOGIN USER BY DATE', weight='bold', size=14)
    
        tick_spacing = 2

        axes.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

        figure.autofmt_xdate()
        figure_canvas.get_tk_widget().place(x=485, y=31, height=300, width=410)

