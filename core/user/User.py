from flask import render_template, url_for

import os 

import core.tools.Constant as cs
import core.tools.DataDefault as df

import core.user.UserData as ud
import core.user.UserTools as ut
import core.user.User as us

import core.user.workspace.WorkSpaceCore as uw

class User:
    
    def __init__(self):
        
        self.user_id :str = ""
        self.user_name :str = ""
        self.user_pwd :str = ""
        self.user_salt_pwd :str = ""
        self.user_first_name :str = ""
        self.user_last_name :str = ""
        self.user_address :str = ""
        self.user_country :str = ""
        self.user_email :str = ""
        self.user_phone :str = ""
        
        self.user_ip :str = ""
        self.error_msg :str = ""
        
        self.user_directoy_path :str = ""
        self.main_data_full_path :str = ""
        
        self.data :ud.UserData = None
        
        self.user_admin :dict = {}            
        self.user_tools :ut.UserTools = ut.UserTools()
        
        self.has_scheduled_task = False
        self.user_login_pwd :str = ""
        
        self.workspace_core :uw.WorkSpaceCore = uw.WorkSpaceCore()
        
        self.current_error_msg :str = ""
            
    def tolist(self) -> list:
        
        user_list :list = []
        
        user_list.append(self.user_id)
        user_list.append(self.user_name)
        user_list.append(self.user_pwd)
        user_list.append(self.user_salt_pwd)
        user_list.append(self.user_first_name)
        user_list.append(self.user_last_name)
        user_list.append(self.user_address)
        user_list.append(self.user_country)
        user_list.append(self.user_email)
        user_list.append(self.user_phone)
        
        user_list.append(self.user_ip)
        user_list.append(self.error_msg)
                         
        return user_list
    
    def todict(self) -> dict:
        
        user_dict :dict = {}
        
        user_dict["user_id"] = self.user_id
        user_dict["user_name"] = self.user_name
        user_dict["user_pwd"] = self.user_pwd
        user_dict["user_salt_pwd"] = self.user_salt_pwd
        user_dict["user_first_name"] = self.user_first_name
        user_dict["user_last_name"] = self.user_last_name
        user_dict["user_address"] = self.user_address
        user_dict["user_country"] = self.user_country
        user_dict["user_email"] = self.user_email
        user_dict["user_phone"] = self.user_phone
        
        return user_dict
    
    def start_login(self):
        
        if not os.path.exists(self.user_directoy_path):
            os.makedirs(self.user_directoy_path)
        
        if self.data == None:
            self.data :ud.UserData = ud.UserData(self.user_directoy_path)
        
        self.user_admin = self.data.set_user_data()
        
        self.workspace_core.read_workspace_user(self.user_directoy_path, self.data)
        
        self.data.set_user_login()
        
        return self.start_session()
    
    def start_session(self):
        
        self.user_tools.reset_user_key_id_list()
        
        id_header_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':header')
        id_nav_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':nav')
        id_content_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':content')
        id_footer_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':footer')
        
        return render_template('workspace/wrks_index.html', id_header_link=id_header_link,
                                                            id_nav_link=id_nav_link,
                                                            id_content_link=id_content_link,
                                                            id_footer_link=id_footer_link)
        
    def display_workspace_nav(self):
        
        new_key_id = self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))
        
        return render_template('workspace/wrks_nav.html', key_id=new_key_id,
                                                          add_workspace_tag=cs.WEB_TAG_ROUTAGE_ADD_WORKSPACE,
                                                          del_workspace_tag=cs.WEB_TAG_ROUTAGE_DEL_WORKSPACE,
                                                          select_workspace_tag=cs.WEB_TAG_ROUTAGE_SELECT_WORKSPACE,
                                                          workspace_core=self.workspace_core)
        
        
    def acquisition_session(self):
        
        self.user_tools.reset_user_key_id_list()
        
        id_header_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':header')
        id_nav_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':nav')
        id_content_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':content_acquisition')
        id_footer_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':footer')
        
        return render_template('workspace/wrks_index.html', id_header_link=id_header_link,
                                                            id_nav_link=id_nav_link,
                                                            id_content_link=id_content_link,
                                                            id_footer_link=id_footer_link)
        
    def display_acquisition_content(self):
        
        id_requester_acquisition_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':acquisition_requester')
        id_result_acquisition_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':acquisition_result')
        id_footer_acquisition_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':acquisition_footer')
        
        return render_template('workspace/acquisition/acqs_content.html', id_requester_acquisition_link=id_requester_acquisition_link,
                                                                          id_result_acquisition_link=id_result_acquisition_link,
                                                                          id_footer_acquisition_link=id_footer_acquisition_link)
        
    def display_acquisition_requester(self):
        
        new_key_id :str = self.user_tools.get_special_user_key_id("R") + "-" + str(int(self.user_id))
        
        self.workspace_core.current_workspace
        
        return render_template('workspace/acquisition/acqs_requester.html', 
                                key_id= new_key_id,
                                new_request_tag=cs.WEB_TAG_ROUTAGE_ADD_REQUEST,
                                delete_request_tag= cs.WEB_TAG_ROUTAGE_DELETE_REQUEST,
                                edit_request_tag= cs.WEB_TAG_ROUTAGE_EDIT_REQUEST,
                                execute_request_tag=cs.WEB_TAG_ROUTAGE_EXECUTE_REQUEST,
                                execute_all_request_tag=cs.WEB_TAG_ROUTAGE_EXECUTE_ALL_REQUEST,
                                workspace=self.workspace_core.current_workspace,
                                user_request_list=self.workspace_core.current_workspace.data.get_user_request_list())    
        
    def transformation_session(self):
        
        self.user_tools.reset_user_key_id_list()
        
        id_header_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':header')
        id_nav_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':nav')
        id_content_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':content_transformation')
        id_footer_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':footer')
        
        return render_template('workspace/wrks_index.html', id_header_link=id_header_link,
                                                            id_nav_link=id_nav_link,
                                                            id_content_link=id_content_link,
                                                            id_footer_link=id_footer_link)
        
        
    def display_transformation_content(self):
        
        id_transformer_transformation_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':transformation_transformer')
        id_result_transformation_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':transformation_result')
        id_footer_transformation_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':transformation_footer')
        
        return render_template('workspace/transformation/trsf_content.html', id_transformer_transformation_link=id_transformer_transformation_link,
                                                                            id_result_transformation_link=id_result_transformation_link,
                                                                            id_footer_transformation_link=id_footer_transformation_link)
        
    def display_transformation_transformer(self):
        
        new_key_id :str = self.user_tools.get_special_user_key_id("R") + "-" + str(int(self.user_id))
        
        self.workspace_core.current_workspace
        
        return render_template('workspace/acquisition/acqs_requester.html', 
                                key_id= new_key_id,
                                new_request_tag=cs.WEB_TAG_ROUTAGE_ADD_REQUEST,
                                delete_request_tag= cs.WEB_TAG_ROUTAGE_DELETE_REQUEST,
                                edit_request_tag= cs.WEB_TAG_ROUTAGE_EDIT_REQUEST,
                                execute_request_tag=cs.WEB_TAG_ROUTAGE_EXECUTE_REQUEST,
                                execute_all_request_tag=cs.WEB_TAG_ROUTAGE_EXECUTE_ALL_REQUEST,
                                workspace=self.workspace_core.current_workspace,
                                user_request_list=self.workspace_core.current_workspace.data.get_user_request_list())    
        
    def exploitation_session(self):
        
        self.user_tools.reset_user_key_id_list()
        
        id_header_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':header')
        id_nav_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':nav')
        id_content_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':content_exploitation')
        id_footer_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':footer')
        
        return render_template('workspace/wrks_index.html', id_header_link=id_header_link,
                                                            id_nav_link=id_nav_link,
                                                            id_content_link=id_content_link,
                                                            id_footer_link=id_footer_link)
        
    def display_exploitation_content(self):
        
        id_transformer_exploitation_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':exploitation_exploiter')
        id_result_exploitation_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':exploitation_result')
        id_footer_exploitation_link = url_for('frame',frame_id_value=self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))+':exploitation_footer')
        
        
        return render_template('workspace/exploitation/expl_content.html', id_exploiter_exploitation_link=id_transformer_exploitation_link,
                                                                           id_result_exploitation_link=id_result_exploitation_link,
                                                                           id_footer_exploitation_link=id_footer_exploitation_link)
    
    def display_scheduler(self):
        
        new_key_id = self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))
        
        key_workspace_name :str = self.workspace_core.current_workspace.name
        
        workspace_scheduler_def :str = self.workspace_core.current_workspace.schedule_code
        
        scheduler_list :list = []
        workspace_scheduler_def :str = ""
        
        detail_backup_def :list = df.DEFAULT_DATA_SYS_BACKUP_DEF
        detail_convert :list = None
        detail_backup :list = None
            
        workspace_scheduler_def = "SELECT A SCHEDULE"
        
        for i in range(len(detail_backup_def)): 
            detail_backup =[]
            detail_convert = list(detail_backup_def[i])
            detail_backup.append(detail_convert[1])
            detail_backup.append(detail_convert[2])
            scheduler_list.append(detail_backup) 
            
            if self.workspace_core.current_workspace.schedule_code == detail_convert[1]:
                workspace_scheduler_def = detail_convert[1]
                
        workspace_home_tag :str = 'content_acquisition'
        scheduler_save_tag :str = cs.WEB_TAG_ROUTAGE_SAVE_SCHEDULER
        
        return render_template('workspace/wrks_scheduler.html', key_id=new_key_id,
                                                                key_workspace_name=key_workspace_name,
                                                                workspace_home_tag=workspace_home_tag,
                                                                scheduler_save_tag=scheduler_save_tag,
                                                                workspace_scheduler_def=workspace_scheduler_def,
                                                                scheduler_list=scheduler_list)  
        
    def display_setting(self, error_message :str = ""):
        
        new_user :us.User = us.User()

        new_user.user_first_name = self.user_first_name
        new_user.user_last_name = self.user_last_name
        new_user.user_address = self.user_address
        new_user.user_country = self.user_country
        new_user.user_email = self.user_email
        new_user.user_phone = self.user_phone
        new_user.user_pwd = self.user_pwd

        new_user.user_login_pwd = self.user_login_pwd

        new_user.error_msg = error_message
        
        new_key_id = self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))
        user_country_def :str= self.data.get_country_definition(self.user_country, self.main_data_full_path)
        
        return render_template('workspace/wrks_settings.html', user_name=self.user_name, 
                                                               country_list=df.DEFAULT_DATA_USER_COUNTRY_DEF, 
                                                               user_country_def=user_country_def,
                                                               new_user=new_user,
                                                               key_id=new_key_id,
                                                               home_tag=cs.WEB_TAG_ROUTAGE_HOME,
                                                               save_setting_tag=cs.WEB_TAG_ROUTAGE_SAVE_SETTING,
                                                               close_account_tag=cs.WEB_TAG_ROUTAGE_CLOSE_ACCOUNT,
                                                               country_code=self.user_country, 
                                                               logout_tag=cs.WEB_TAG_ROUTAGE_LOGOUT,
                                                               save_password_tag=cs.WEB_TAG_ROUTAGE_SAVE_PASSWORD)  
        
    def log_out_session(self):
        
        self.user_tools.reset_user_key_id_list()
        self.data.set_user_logout()
        
        if self.has_scheduled_task:
            ##  KEEP Open Session for Scheduled Task ...
            pass
        

    def user_frame_session(self, frame_id_value :str):
        
        frame_value_list :list = frame_id_value.split(":")
        key_id :str = frame_value_list[0]
        key_id_list :list = key_id.split("-")
        
        if self.user_tools.is_user_key_id_valid(key_id_list[0]):
            
            new_key_id :str = ""
            self.error_msg = ""
            
            if len(frame_value_list) > 1:
               
                if frame_value_list[1] == 'header':
                    
                    new_key_id :str = self.user_tools.get_special_user_key_id("H") + "-" + str(int(self.user_id))
                    
                    return render_template('workspace/wrks_header.html', key_id=new_key_id, 
                                                                         logout_tag=cs.WEB_TAG_ROUTAGE_LOGOUT,
                                                                         setting_tag=cs.WEB_TAG_ROUTAGE_SETTINGS,
                                                                         acquisition_tag=cs.WEB_TAG_ROUTAGE_HEADER_ACQUISITION,
                                                                         transformation_tag=cs.WEB_TAG_ROUTAGE_HEADER_TRANSFORMATION,
                                                                         exploitation_tag=cs.WEB_TAG_ROUTAGE_HEADER_EXPLOITATION,
                                                                         workspace=self.workspace_core.current_workspace)  
                    
                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_HEADER_ACQUISITION:  
                     
                    self.workspace_core.current_workspace.set_select_acquisition()
                    return self.acquisition_session()
                    
                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_HEADER_TRANSFORMATION:   
                    
                    self.workspace_core.current_workspace.set_select_transform()
                    return self.transformation_session()
                
                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_HEADER_EXPLOITATION: 
                    
                    self.workspace_core.current_workspace.set_select_exploitation()  
                    return self.exploitation_session()
                
                if frame_value_list[1] == 'transformation_transformer':   
                    
                    new_key_id = self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))
                    
                    return render_template('workspace/transformation/trsf_transformer.html', key_id=new_key_id,
                                                                                             workspace=self.workspace_core.current_workspace)
                    
                
                if frame_value_list[1] == 'transformation_result':   
                    
                    new_key_id = self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))
                    
                    return render_template('workspace/transformation/trsf_result.html', key_id=new_key_id,
                                                                                        workspace=self.workspace_core.current_workspace)
                    
                if frame_value_list[1] == 'exploitation_result':   
                    
                    new_key_id = self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))
                    
                    return render_template('workspace/exploitation/expl_result.html', key_id=new_key_id,
                                                                                        workspace=self.workspace_core.current_workspace)
                
                    
                if frame_value_list[1] == 'exploitation_exploiter':   
                    
                    new_key_id = self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))
                    
                    return render_template('workspace/exploitation/expl_exploitation.html', key_id=new_key_id,
                                                                                            workspace=self.workspace_core.current_workspace)
                    
                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_TRANSFORMATION_VALIDATION:  
                    
                    self.workspace_core.current_workspace.set_valid_transform()
                    
                    new_key_id :str = self.user_tools.get_special_user_key_id("T") + "-" + str(int(self.user_id))
                    
                    return render_template('workspace/wrks_header.html', key_id=new_key_id, 
                                                                         logout_tag=cs.WEB_TAG_ROUTAGE_LOGOUT,
                                                                         setting_tag=cs.WEB_TAG_ROUTAGE_SETTINGS,
                                                                         acquisition_tag=cs.WEB_TAG_ROUTAGE_HEADER_ACQUISITION,
                                                                         transformation_tag=cs.WEB_TAG_ROUTAGE_HEADER_TRANSFORMATION,
                                                                         exploitation_tag=cs.WEB_TAG_ROUTAGE_HEADER_EXPLOITATION,
                                                                         workspace=self.workspace_core.current_workspace)  
                    
                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_EXPLOITATION_VALIDATION:  
                    
                    self.workspace_core.current_workspace.set_valid_exploitation()
                    
                    new_key_id :str = self.user_tools.get_special_user_key_id("E") + "-" + str(int(self.user_id))
                    
                    return render_template('workspace/wrks_header.html', key_id=new_key_id, 
                                                                         logout_tag=cs.WEB_TAG_ROUTAGE_LOGOUT,
                                                                         setting_tag=cs.WEB_TAG_ROUTAGE_SETTINGS,
                                                                         acquisition_tag=cs.WEB_TAG_ROUTAGE_HEADER_ACQUISITION,
                                                                         transformation_tag=cs.WEB_TAG_ROUTAGE_HEADER_TRANSFORMATION,
                                                                         exploitation_tag=cs.WEB_TAG_ROUTAGE_HEADER_EXPLOITATION,
                                                                         workspace=self.workspace_core.current_workspace)  
                
                if frame_value_list[1] == 'transformation_footer':   
                    
                    new_key_id :str = self.user_tools.get_special_user_key_id("O") + "-" + str(int(self.user_id))
                    
                    return render_template('workspace/transformation/trsf_footer.html', key_id=new_key_id,                                                                                        
                                                                                        select_validation_tag=cs.WEB_TAG_ROUTAGE_TRANSFORMATION_VALIDATION)
                    
                
                if frame_value_list[1] == 'exploitation_footer':   
                    
                    new_key_id :str = self.user_tools.get_special_user_key_id("F") + "-" + str(int(self.user_id))
                    
                    return render_template('workspace/exploitation/expl_footer.html', key_id=new_key_id,                                                                                        
                                                                                      select_validation_tag=cs.WEB_TAG_ROUTAGE_EXPLOITATION_VALIDATION)
                    
                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_SELECT_WORKSPACE:   
                    
                    self.workspace_core.current_workspace.data_base = None
                    
                    self.workspace_core.current_workspace.set_workspace(frame_value_list[2])
              
                    return self.acquisition_session()
                
                                    
                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_ADD_WORKSPACE:   
                    
                    self.current_error_msg = ""
                    self.workspace_core.current_workspace.reset_workspace()
                    frame_value_list[2] = str(frame_value_list[2]).upper()
                    
                    self.current_error_msg = self.user_tools.is_valid_workspace_name(frame_value_list[2])
                    
                    if self.current_error_msg == "":
                        self.current_error_msg = self.workspace_core.add_new_workspace(frame_value_list[2])
                
                    return self.start_session()

                
                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_DEL_WORKSPACE:   
                    
                    self.workspace_core.current_workspace.reset_workspace()
                    self.current_error_msg = self.workspace_core.add_new_workspace(frame_value_list[2])
                    
                    if self.workspace_core.remove_workspace(frame_value_list[2]):
                        self.current_error_msg = frame_value_list[2] + " workspace has been removed from system!"
                    else:
                        self.current_error_msg = "Error: [" + frame_value_list[2] + "] is not a valid workspace name!"
                    
                    return self.start_session()
                    
                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_HOME:
                    
                    self.workspace_core.current_workspace.reset_workspace()
                    
                    return render_template('workspace/wrks_content.html', user_name=self.user_name,
                                                                          error_msg=self.current_error_msg)
                    
                                
                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_SAVE_PASSWORD:
                    
                    self.workspace_core.current_workspace.reset_workspace()
                    self.error_msg = self.user_tools.check_new_password(frame_value_list, self.user_login_pwd)
                    
                    if len(self.error_msg) == 0:
                        
                        if len(frame_value_list) > 2:
                            if self.data.update_user_password(str(frame_value_list[3]).split("=")[1], self.user_id, self.main_data_full_path):
                                return self.display_setting("New Password has been changed in the system")                            
                            else:
                                return self.display_setting("Error on new password change retry again")
                        
                    return self.display_setting("Error: " + self.error_msg)
                

                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_SAVE_SETTING:
                    
                    self.workspace_core.current_workspace.reset_workspace()
                    
                    if not self.is_valid_new_user_data(frame_id_value, True):
                        return self.display_setting(self.error_msg)
                    
                    if self.data.update_user_settings(frame_value_list, self.user_id, self.main_data_full_path):
                        self.update_user_setting(frame_value_list)
                        
                    return render_template('workspace/wrks_content.html', user_name=self.user_name)
                
                
                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_CLOSE_ACCOUNT:
                    self.data.close_account(self.user_id, self.main_data_full_path)
                    return render_template('global/account_closed.html')
                
                    
                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_SETTINGS:
                    return self.display_setting()                
                              
                if frame_value_list[1] == 'content':
                    
                    return render_template('workspace/wrks_content.html', user_name=self.user_name,
                                                                          error_msg=self.current_error_msg)
                
                if frame_value_list[1] == 'content_acquisition':    
                    return self.display_acquisition_content()
                
                if frame_value_list[1] == 'content_transformation':    
                    return self.display_transformation_content()
                
                if frame_value_list[1] == 'content_exploitation':    
                    return self.display_exploitation_content()
                
                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_DELETE_REQUEST:    
                    
                    if len(frame_value_list) > 2:
                        self.workspace_core.current_workspace.data.delete_request(frame_value_list[2])
                        
                    return self.display_acquisition_requester()
                

                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_EDIT_REQUEST:
                    
                    if len(frame_value_list) > 1:

                        self.workspace_core.current_workspace.message = self.workspace_core.current_workspace.check_is_valid_request(
                                                                        frame_value_list, True)
                        
                        if len(self.workspace_core.current_workspace.message) == 0:

                            self.workspace_core.current_workspace.message = ""
                            self.workspace_core.current_workspace.is_error_message = False
                            self.workspace_core.current_workspace.data.update_request(frame_value_list)

                        else:
                            self.workspace_core.current_workspace.is_error_message = True
                            
                        return self.display_acquisition_requester()
                            

                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_ADD_REQUEST:
                    
                    if len(frame_value_list) > 1:

                        self.workspace_core.current_workspace.message = self.workspace_core.current_workspace.check_is_valid_request(
                                                                        frame_value_list)
                        
                        if len(self.workspace_core.current_workspace.message) == 0:

                            self.workspace_core.current_workspace.message = ""
                            self.workspace_core.current_workspace.is_error_message = False
                            self.workspace_core.current_workspace.data.add_new_request(frame_value_list)

                        else:
                            self.workspace_core.current_workspace.is_error_message = True
                            
                        return self.display_acquisition_requester()
                    
                    
                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_SAVE_SCHEDULER:            
                    
                    self.workspace_core.current_workspace.set_schedule(True, 
                                                                       self.data.replace_tag_format(frame_value_list[2]))

                    self.workspace_core.current_workspace.is_error_message = False
                    self.workspace_core.current_workspace.message = ""
                    
                    return self.display_acquisition_content()
                    
                    
                if frame_value_list[1] == 'acquisition_requester':
                    
                    self.workspace_core.current_workspace.is_error_message = False
                    self.workspace_core.current_workspace.message = ""
                    
                    return self.display_acquisition_requester()

                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_EXECUTE_ALL_REQUEST:    
                    
                    self.workspace_core.current_workspace.data_base = self.workspace_core.current_workspace.process.do_api_all_request()
                    self.workspace_core.current_workspace.current_result_name = "ALL REQUEST EXECUTED"
                    
                    return render_template('workspace/acquisition/acqs_result.html', key_id=new_key_id,
                                                                                     workspace=self.workspace_core.current_workspace)
                    
                
                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_EXECUTE_REQUEST:    
                    
                    request_parameter_list :list = []
                    request_parameter_dict :dict = {}
                    
                    if len(frame_value_list) > 1:
                        
                        self.workspace_core.current_workspace.data_base = self.workspace_core.current_workspace.process.do_api_request(frame_value_list[2])
                        
                        request_parameter_list =  self.workspace_core.current_workspace.data.get_user_request_list(frame_value_list[2])
                        request_parameter_dict = request_parameter_list[0]
                        
                        self.workspace_core.current_workspace.current_result_name = request_parameter_dict["name"]
                        
                        new_key_id = self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))
                        
                        return render_template('workspace/acquisition/acqs_result.html', key_id=new_key_id,
                                                                                         workspace=self.workspace_core.current_workspace)
                
                
                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_ACQUISITION_VALIDATION:    
                    
                    self.workspace_core.current_workspace.set_valid_acquisition()
                    
                    new_key_id :str = self.user_tools.get_special_user_key_id("L") + "-" + str(int(self.user_id))
                    
                    return render_template('workspace/wrks_header.html', key_id=new_key_id, 
                                                                         logout_tag=cs.WEB_TAG_ROUTAGE_LOGOUT,
                                                                         setting_tag=cs.WEB_TAG_ROUTAGE_SETTINGS,
                                                                         workspace=self.workspace_core.current_workspace)  
                
                if frame_value_list[1] == cs.WEB_TAG_ROUTAGE_SCHEDULER:      
                    
                    return self.display_scheduler()
                
                
                if frame_value_list[1] == 'acquisition_result':
                    
                    new_key_id = self.user_tools.get_user_key_id() + "-" + str(int(self.user_id))
                    
                    return render_template('workspace/acquisition/acqs_result.html', key_id=new_key_id,
                                                                                     workspace=self.workspace_core.current_workspace)
                
                if frame_value_list[1] == 'acquisition_footer':
                    
                    new_key_id :str = self.user_tools.get_special_user_key_id("O") + "-" + str(int(self.user_id))
                    
                    return render_template('workspace/acquisition/acqs_footer.html', key_id=new_key_id,
                                                                                     select_scheduler_tag=cs.WEB_TAG_ROUTAGE_SCHEDULER,
                                                                                     select_validation_tag=cs.WEB_TAG_ROUTAGE_ACQUISITION_VALIDATION,)
                if frame_value_list[1] == 'nav':
                    
                    return self.display_workspace_nav()

                    
                if frame_value_list[1] == 'footer':
                    return render_template('workspace/wrks_footer.html')
        
        print("tset_error:",frame_value_list)
        return render_template('global/error.html',error_msg="Frame Routage not valid")
    
    
    def update_user_setting(self, frame_value_list :list):
        
        self.user_first_name = str(self.user_tools.replace_tag_format(str(frame_value_list[2]).split("=")[1]))
        self.user_last_name = str(self.user_tools.replace_tag_format(str(frame_value_list[3]).split("=")[1]))
        self.user_address = str(self.user_tools.replace_tag_format(str(frame_value_list[4]).split("=")[1]))
        self.user_country = str(self.user_tools.replace_tag_format(str(frame_value_list[5]).split("=")[1]))
        self.user_email = str(self.user_tools.replace_tag_format(str(frame_value_list[6]).split("=")[1]))
        self.user_phone = str(self.user_tools.replace_tag_format(str(frame_value_list[7]).split("=")[1]))
        
    def is_valid_new_user_data(self, new_user_data: str, from_setting :bool = False) -> bool:
        
        new_user_data_split = new_user_data.split(':')
        
        for i in range(len(new_user_data_split)):
            
            new_user_data_value = str(new_user_data_split[i]).split('=')
            
            if len(new_user_data_value) == 2:
                
                match new_user_data_value[0]:                    
                    case "user_name":                        
                        self.user_name = self.user_tools.replace_tag_format(new_user_data_value[1])
                    case "user_pwd":
                        self.user_pwd = self.user_tools.replace_tag_format(new_user_data_value[1])
                    case "user_first_name":
                        self.user_first_name = self.user_tools.replace_tag_format(new_user_data_value[1])
                    case "user_last_name":
                        self.user_last_name = self.user_tools.replace_tag_format(new_user_data_value[1])
                    case "user_address":
                        self.user_address = self.user_tools.replace_tag_format(new_user_data_value[1])
                    case "user_country":
                        self.user_country = self.user_tools.replace_tag_format(new_user_data_value[1])
                    case "user_email":
                        self.user_email = self.user_tools.replace_tag_format(new_user_data_value[1])
                    case "user_phone":
                        self.user_phone = self.user_tools.replace_tag_format(new_user_data_value[1])
            else:
                if not from_setting:
                    self.error_msg :str = "Data Corupted"
                    return False
        
        if not from_setting:
            if len(self.user_name) == 0:
                self.error_msg :str = "User name not valid, missing value"
                return False
                
            if len(self.user_pwd) == 0:
                self.error_msg :str = "User password not valid, missing value"
                return False
            
        if len(self.user_first_name) == 0:
            self.error_msg :str = "User first name not valid, missing value"
            return False
            
        if len(self.user_last_name) == 0:
            self.error_msg :str = "User last name not valid, missing value"
            return False
        
        if len(self.user_address) == 0:
            self.error_msg :str = "User address not valid, missing value"
            return False    
        
        if not self.user_tools.is_valid_address(self.user_address):
            valid_address_char :str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 :.-,()'    
            self.error_msg :str = "Address not Valid. Character value allowed only: ['" + valid_address_char + "']'"
            return False
        
        if len(self.user_country) == 0:
            self.error_msg :str = "User country not valid, missing value"
            return False
        
        if not self.user_tools.is_valid_email(self.user_email):
            self.error_msg :str = "EMail not Valid [xxxxx@xxx.xx] -> [xxx.xxxx.x.xx@xxx.xx] No special aplha value admited"
            return False
        
        if len(self.user_phone) == 0:
            self.error_msg :str = "User phone not valid, missing value"
            return False
            
        if not self.user_tools.is_valid_phone(self.user_phone):
            valid_phone_number_char :str = '0123456789+.-()'
            self.error_msg :str = "Phone not Valid. Character value allowed only: ['" + valid_phone_number_char + "']'"
            return False

        return True
    