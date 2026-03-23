# ASCDEV SYSTEM DEV ©Copyright
import os 
import random
import string

import core.CoreData as ca
import core.tools.Constant as cs
import core.tools.Constant as cs

import core.user.CoreUser as cr

class CoreInit:
    
    def __init__(self,  common_root_ini_path: str):
    
        self.common_root_ini_path = common_root_ini_path + cs.INIT_DIRECTORY_CORE
        self.data = None
        self.admin_login = ""
        self.admin_pwd_change :bool = False        
        
        self.KEY_ID_LIST :list = []
        self.is_web_server_task :bool = True
        
        self.CoreUsers :cr.CoreUser = None
        
        self.init_core()
    
    def data_base_directory_path(self) -> str:
        
        return self.common_root_ini_path + cs.INIT_DIRECTORY_DATA
    
    def users_directory_path(self) -> str:
        
        return self.data_base_directory_path() + cs.INIT_DIRECTORY_USERS
    
    def data_base_full_path_name(self) -> str:
        
        return self.data_base_directory_path() + cs.INIT_DATA_BASE_FILE_NAME

    def init_core(self):
        """ 
            Initialisation data config for admin application and web server
        """

        self.check_directory_app()
        self.data =  ca.CoreData(self.data_base_full_path_name())
        
        self.check_core_data()
        
    def check_core_data(self):
        
        if not self.is_valid_ip_port_format(self.data.admin_server_data["server_ip_port"]):
            self.data.admin_server_data["server_ip_port"] = cs.INIT_DEFAULT_SERV_IP_PORT
            self.data.data_tools.sql_change_admin_value("server_ip_port",cs.INIT_DEFAULT_SERV_IP_PORT)
                                
        self.check_path_file_admin("python_path")
        self.check_path_file_admin("web_server_path")
        
        self.check_max_users_allowed()

    
    def is_valid_ip_port_format(self, server_ip_port :str) -> bool:
        
        server_ip_port_list :list = []
        server_ip :list = []

        if len(server_ip_port) == 0:
            return False
        
        for i in range(len(server_ip_port)):
            for j in range(len(string.ascii_lowercase)):
                if server_ip_port[i] == string.ascii_lowercase[j]:
                    return False
            for j in range(len(string.ascii_uppercase)):
                if server_ip_port[i] == string.ascii_uppercase[j]:
                    return False
                
        server_ip_port_list = server_ip_port.split(":")
        
        if len(server_ip_port_list) == 2:
            if str(server_ip_port_list[1]).isnumeric:
                if int(server_ip_port_list[1]) > 0 and int(server_ip_port_list[1]) < 65536:
                
                        server_ip = server_ip_port_list[0].split(".")        
                        
                        if len(server_ip) == 4:
                            
                            for i in range(len(server_ip)):
                                if not(int(server_ip[i]) > -1 and int(server_ip[i]) < 256):
                                    return False
                                
                            return True
                    
        return False
    
    def is_valid_email_format(self, email_value :str) -> bool:
        
        email_list :list = []
        email_list_low :list = []
        email_list_hight :list = []
        
        if len(email_value) == 0:
            return False
        
        email_list = email_value.split("@")
        
        if len(email_list) == 2:
            email_list_low = email_list[0].split(".")
            email_list_hight = email_list[1].split(".")
            if len(email_list_hight) == 2:
                
                for i in range(len(email_list_low)):
                    for j in range(len(email_list_low[i])):
                        if string.punctuation.find(email_list_low[i][j]) > -1:
                            return False
                        
                for i in range(len(email_list_hight)):
                    for j in range(len(email_list_hight[i])):
                        if string.punctuation.find(email_list_hight[i][j]) > -1:
                            return False
        
        return True
    
    def check_path_file_admin(self, field_admin_file_path :str):
        
        if len(self.data.admin_server_data[field_admin_file_path]) > 0:
            if not os.path.exists(self.data.admin_server_data[field_admin_file_path]):
                self.data.admin_server_data[field_admin_file_path] = ""
                self.data.data_tools.sql_change_admin_value(field_admin_file_path,"")
        
        
    def check_directory_app(self):
        """ 
            Check directory path for database and users
        """
        
        if not os.path.exists(self.data_base_directory_path()):
            os.makedirs(self.data_base_directory_path())

        if not os.path.exists(self.users_directory_path()):
            os.makedirs(self.users_directory_path())            
            
    def check_max_users_allowed(self):
        """ 
            Check max value for user limit on server             
        """
        
        if not self.is_max_users_allowed(str(self.data.admin_server_data["max_users_allowed"])):
            self.data.admin_server_data["max_users_allowed"] = 100000
            self.data.data_tools.sql_change_admin_value("max_users_allowed",str(self.data.admin_server_data["max_users_allowed"]))
            
    def is_max_users_allowed(self, max_user_value :str):
        """ 
            Check valid value for max user allowed
        """
        
        if len(max_user_value) == 0:
            return False
        else:
            
            for i in range(len(max_user_value)):
                if not string.digits.find(max_user_value[i]) > -1:
                    return False
                        
            if not str(max_user_value).isnumeric and not str(int(max_user_value)) == max_user_value:
                return False
            elif int(max_user_value) < 1 or int(max_user_value) > 1000000000:
                return False
        
        return True
    
    def init_key_id_list(self, number_key :int, To_remove_first_list :bool = True):
        """ 
            Create default keyId list to checking right request on public acess frame
        """
        
        self.reset_key_id_list(number_key, False)
        self.reset_key_id_list(number_key, False)
        self.reset_key_id_list(number_key, False)
        
    def reset_key_id_list(self, number_key :int, To_remove_first_list :bool = True):
        
        """ 
            Reset default keyId list only public access frame
        """
        
        new_key_id_list :list = []
        
        Random_lenght :int = 0
        new_salt_value :str = ""
        
        valid_List_char :str = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        len_list_char :int = len(valid_List_char)- 1
        
        for _ in range(number_key):
            new_salt_value = ""
            Random_lenght = random.randint(15, 25)
            for _ in range(Random_lenght):
                new_salt_value += valid_List_char[random.randint(0, len_list_char)]
                
            new_key_id_list.append(new_salt_value)
            
        self.KEY_ID_LIST.append(new_key_id_list)    
        
        if To_remove_first_list:
            self.KEY_ID_LIST.pop(0)
        
    def get_random_key_id(self) -> str:
        """ 
            Get a random keyId from list only public access frame
        """
        
        return self.KEY_ID_LIST[2][random.randint(0, len(self.KEY_ID_LIST[2])- 1)]
    
    def is_random_key_id(self, key_id :str) -> bool:
        """ 
            Check if is a valid random keyId from list only public access frame
        """
        
        for i in range(3):
            if key_id in self.KEY_ID_LIST[i]:
                return True
            
        return False
    