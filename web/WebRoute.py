from flask import render_template, url_for

import core.CoreInit as ci
import core.user.User as cu
import core.user.CoreUser as cr 

import core.tools.Constant as cs
import core.tools.DataDefault as df

class WebRoute():
    
    def __init__(self, CoreInit :ci.CoreInit):
        
        self.web_core :ci.CoreInit = CoreInit
        self.web_core.CoreUsers = cr.CoreUser(self.web_core.users_directory_path(), self.web_core.data.data_base_full_path_name)
        
    def user_home(self):
        
        company_name = self.web_core.data.admin_server_data["company_name"]
        title ="DPRM PROJECT " 
        key_id = self.web_core.get_random_key_id()
        
        id_header_link = url_for('frame',frame_id_value=key_id+':index_header')
        id_content_link = url_for('frame',frame_id_value=key_id+':index_content')
        id_footer_link = url_for('frame',frame_id_value=key_id+':footer')
        
        return render_template('index/index.html', title=title, 
                                                   company_name=company_name,  
                                                   id_header_link=id_header_link,
                                                   id_content_link=id_content_link,
                                                   id_footer_link=id_footer_link)  
        
    def user_signin(self, user :cu.User):
        
        company_name = self.web_core.data.admin_server_data["company_name"]
        title ="SINGIN " 
        key_id = self.web_core.get_random_key_id()
        
        if len(user.error_msg) == 0 :
            id_header_link = url_for('frame',frame_id_value=key_id+':sign_in_header')
        else:
            id_header_link = url_for('frame',frame_id_value=key_id+':sign_in_header_error')
        
        id_content_link = url_for('frame',frame_id_value=key_id+':sign_in_content')
        id_footer_link = url_for('frame',frame_id_value=key_id+':footer')
        
        return render_template('signin/sign_in.html', title=title, company_name=company_name,                                                
                                                      id_header_link=id_header_link,
                                                      id_content_link=id_content_link,
                                                      id_footer_link=id_footer_link)       
        
    def user_login(self, user :cu.User):
        
        company_name = self.web_core.data.admin_server_data["company_name"]
        title ="LOGIN "           
        key_id = self.web_core.get_random_key_id()
        
        if len(user.error_msg) == 0 :
            id_header_link = url_for('frame',frame_id_value=key_id+':login_header')
        else:
            id_header_link = url_for('frame',frame_id_value=key_id+':login_header_error')
        
        id_content_link = url_for('frame',frame_id_value=key_id+':login_content')
        id_footer_link = url_for('frame',frame_id_value=key_id+':footer')
        
        return render_template('login/login.html', title=title, company_name=company_name, 
                                             id_header_link=id_header_link,
                                             id_content_link=id_content_link,
                                             id_footer_link=id_footer_link)
        
    def user_signin_submit(self, key_value :str, user_ip: str):    
        
        key_value = key_value[len(cs.WEB_TAG_REQUEST_SIGNIN_SUBMIT + ":"):]
                    
        user = cu.User()                
        
        if user.is_valid_new_user_data(key_value):
            if self.web_core.data.data_tools.is_valid_new_user(user):

                user.user_ip = user_ip
                user.error_msg = ""
                
                user.user_login_pwd = user.user_pwd
                self.web_core.data.data_tools.add_new_user(user)
                self.web_core.data.data_tools.set_user_log(user, "CREATE","")
                self.web_core.data.data_tools.set_user_log(user, "LOGIN","")
                
                self.web_core.data.data_tools.get_user_data_login(user)
                    
                return self.web_core.CoreUsers.login(user)
                
            user.error_msg = "User name already exist, please choose an other one!"
            
        return self.user_signin(user)         
        
    def user_login_submit(self, key_value :str, user_ip: str):
        
        key_value = key_value[len(cs.WEB_TAG_REQUEST_LOGIN_SUBMIT + ":"):]
        key_value_list = key_value.split(":")
        
        user = cu.User()  
                                        
        if len(key_value_list) == 2:                    
            
            user.user_name = key_value_list[0]
            user.user_pwd = key_value_list[1]
            
            if not self.web_core.data.data_tools.is_valid_new_user(user):
                if self.web_core.data.data_tools.is_valid_login_user(user):
                    
                    user.error_msg = ""
                    user.user_ip = user_ip
                    user.user_login_pwd = user.user_pwd
                    
                    self.web_core.data.data_tools.set_user_log(user, "LOGIN","")

                    self.web_core.data.data_tools.get_user_data_login(user)

                    return self.web_core.CoreUsers.login(user)
        
        user.error_msg = "Error on Login or Password!"
        return self.user_login(user)
    
    def user_frame(self, frame_id_value :str):
        
        company_name = self.web_core.data.admin_server_data["company_name"]
        frame_routage_list :list = frame_id_value.split("_")
        
        if len(frame_routage_list) > 1:
            if frame_routage_list[0] == "index":
                return self.user_frame_index(frame_id_value)
            
            if frame_routage_list[0] == "login":
                return self.user_frame_login(frame_id_value)
            
            if frame_routage_list[0] == "sign":
                return self.user_frame_SignIn(frame_id_value)

        if frame_id_value == 'footer':
            return render_template('global/footer.html', company_name=company_name)
        
        return render_template('global/error.html',error_msg="Frame Routage not valid")
        
    def user_frame_index(self, frame_id_value :str):
        
        key_id = self.web_core.get_random_key_id()
        
        if frame_id_value == 'index_header':
            user_tag = "PLEASE MAKE A SELECTION"
            return render_template('index/indx_header.html', signin_tag=cs.WEB_TAG_REQUEST_SIGNIN, 
                                                             login_tag=cs.WEB_TAG_REQUEST_LOGIN,
                                                             key_id=key_id,
                                                             user_tag=user_tag)        
        if frame_id_value == 'index_content':
            return render_template('index/indx_content.html')
        
        return render_template('global/error.html',error_msg="Frame Routage not valid in Index")
    
    def user_frame_login(self, frame_id_value :str):
        
        user_tag = "USER LOGIN FORM FOR DPRM PROJECT"
        key_id = self.web_core.get_random_key_id()
        
        if frame_id_value == 'login_header':
            user = cu.User()  
            return render_template('login/login_header.html', user_tag=user_tag,
                                                        user=user)        
        if frame_id_value == 'login_header_error':
            user = cu.User()  
            user.error_msg = "Error on Login or Password!"
            return render_template('login/login_header.html', user_tag=user_tag,
                                                        user=user)        
        if frame_id_value == 'login_content':
            user = cu.User()  
            return render_template('login/login_content.html',key_id=key_id, 
                                                        login_submit_tag=cs.WEB_TAG_REQUEST_LOGIN_SUBMIT, 
                                                        user=user)
        
        return render_template('global/error.html',error_msg="Frame Routage not valid in Login")
    
    def user_frame_SignIn(self, frame_id_value :str):
        
        user_tag = "USER SIGN IN FORM FOR DPRM PROJECT"
        key_id = self.web_core.get_random_key_id()
        
        if frame_id_value == 'sign_in_header':
            user = cu.User()  
            return render_template('signin/sign_in_header.html', user_tag=user_tag,
                                                                 new_user=user)        
            
        if frame_id_value == 'sign_in_header_error':
            user = cu.User()  
            user.error_msg = "User name already exist, please choose an other one!"
            return render_template('signin/sign_in_header.html', user_tag=user_tag,
                                                                 new_user=user)        
            
        if frame_id_value == 'sign_in_content':
            user = cu.User()  
            return render_template('signin/sign_in_content.html',key_id=key_id, 
                                                                 signin_submit_tag=cs.WEB_TAG_REQUEST_SIGNIN_SUBMIT, 
                                                                 country_list=df.DEFAULT_DATA_USER_COUNTRY_DEF, 
                                                                 new_user=user)
    
        return render_template('global/error.html',error_msg="Frame Routage not valid in SignIn")
    
    def session_logout(self, key_id :str):

        self.web_core.CoreUsers.logout(key_id)

        return self.user_home()


    def session_frame(self, frame_id_value :str):
    
        return self.web_core.CoreUsers.session_frame(frame_id_value)    
    