from flask import render_template

import core.user.User as cu

class CoreUser():
    
    def __init__(self, users_directory_path :str , main_data_full_path :str):
        
        self.users_directory_path = users_directory_path
        self.users :dict = {}
        self.main_data_full_path = main_data_full_path
    
    def login(self, user :cu.User):
        
        if user.user_id in self.users:
        
            user = self.users[str(user.user_id)]
            
            return user.start_session()
        
        else:
            self.users[str(user.user_id)] = user
            
        user.user_directoy_path = self.users_directory_path + str(user.user_id)
        user.main_data_full_path = self.main_data_full_path
        
        return user.start_login()
        
    def logout(self, key_id :str):

        key_id_list :list = key_id.split("-")
        user :cu.User =  self.users[str(key_id_list[1])]

        if user.user_tools.is_user_key_id_valid(key_id_list[0]):
        
            user.log_out_session()
    
            if not user.has_scheduled_task:

                self.users.pop(str(key_id_list[1]))
                
        
    def session_frame(self, frame_id_value :str):
        
        frame_id_list :list = str(frame_id_value).split(":")
        key_id :str = frame_id_list[0]
        key_id_list :list = key_id.split("-")
        
        if len(key_id_list) >= 2:
            
            if str(key_id_list[1]) in self.users:
                
                user :cu.User = self.users[str(key_id_list[1])]
                return user.user_frame_session(frame_id_value)
            
        return render_template('global/error.html', error_msg="Frame Routage not valid in workspace")
    