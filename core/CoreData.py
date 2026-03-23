import hashlib
import os

import core.tools.DataTools as dt  

class CoreData:
    
    def __init__(self,  data_base_full_path_name: str):
        
        self.data_base_full_path_name = data_base_full_path_name
        self.admin_server_data :dict = []
        self.data_tools = dt.DataTools(data_base_full_path_name)
        
        self.init_data()
        
    def init_data(self):
        """
        Init and read data base admin
        """
        if not os.path.exists(self.data_base_full_path_name):
            self.data_tools.create_default_database()
            
        self.data_tools.check_default_system_table()            
        
        self.admin_server_data = self.data_tools.get_admin_server_data()
        
        self.data_tools.sql_update_all_system_admin_values(self.admin_server_data)
        
    def change_admin_password(self, new_password :str):
        """
        Change admin password in database
        """
        new_password_hash :str = hashlib.sha256(new_password.encode()).hexdigest()
        
        if self.admin_server_data["admin_password"] != new_password_hash:
            if self.data_tools.sql_change_admin_password(new_password_hash):
                self.admin_server_data["admin_password"] = new_password_hash
                
    def get_full_command_launch_server(self) -> str:
        """
        Get full command to launch web server
        """
        full_cmd_path_server :str = ""
        
        if len(self.admin_server_data["python_path"]) > 0 and len(self.admin_server_data["web_server_path"]) > 0:
            full_cmd_path_server = self.admin_server_data["python_path"] + " '" + self.admin_server_data["web_server_path"] + "'"
        
        return full_cmd_path_server
    
    def sql_change_admin_value(self, field_to_update :str, value_to_update :str):
        
        if len(field_to_update) > 0 and  len(value_to_update) > 0:
            self.data_tools.sql_change_admin_value(field_to_update , value_to_update)
            self.admin_server_data[field_to_update] = value_to_update
            
    def get_current_backup_definition(self) -> str:
        
        return self.data_tools.get_backup_definition_by_id(int(self.admin_server_data["backup_time_cycle"]))        
    
    def get_backup_id_by_definition(self, definition :str) -> str:
        
         return str(self.data_tools.get_backup_id_by_definition(definition))
    
    
        
            