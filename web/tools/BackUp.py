import datetime as dt
import zipfile
import shutil
import os

from datetime import timedelta, datetime

import core.CoreInit as ci

class BackUp():
    
    def __init__(self, CoreInit :ci.CoreInit):
      
        self.web_core :ci.CoreInit = CoreInit
      
    def zip_directory(self, folder_path, zip_file):
            
            parent_folder = os.path.dirname(folder_path)
            
            for folder_name, subfolders, filenames in os.walk(folder_path):
                for filename in filenames:
                    file_path = os.path.join(folder_name, filename)
                    relative_path = file_path.replace(parent_folder + '\\','')
                    zip_file.write(file_path, relative_path)
            
    def check_to_make_backup(self):
        
        if self.web_core.data.admin_server_data["is_backup_activate"] == "TRUE":
            if len(self.web_core.data.admin_server_data["backup_path_directory"]) > 0:
                if not os.path.exists(self.web_core.data.admin_server_data["backup_path_directory"]):    
                    os.makedirs(self.web_core.data.admin_server_data["backup_path_directory"])
                    
                backup_cycle_id :int = int(self.web_core.data.admin_server_data["backup_time_cycle"])
                backup_cycle_code :str = self.web_core.data.data_tools.get_backup_cycle_by_id(backup_cycle_id)
                
                if len(self.web_core.data.admin_server_data["last_backup_date"]) == 0:
                    self.web_core.data.admin_server_data["last_backup_date"] = str(dt.datetime.now()+timedelta(days=-100))
                    self.web_core.data.data_tools.sql_update_all_system_admin_values(self.web_core.data.admin_server_data)
                
                date_format = '%Y-%m-%d %H:%M:%S'    
                current_date :datetime = dt.datetime.now()
                Last_backup_date :datetime = datetime.strptime(self.web_core.data.admin_server_data["last_backup_date"].split(".")[0], date_format)
                has_to_make_backup :bool = False
                
                if (current_date.year != Last_backup_date.year) or (current_date.month != Last_backup_date.month) or (current_date.day != Last_backup_date.day):

                    backup_day_code :int = int(backup_cycle_code.split(",")[0].replace("D",""))-1
                    backup_day_hour :int = int(backup_cycle_code.split(",")[1].replace(":",""))*100
                    current_day_hour :int = int((current_date.hour*10000)+(current_date.minute*100)+(current_date.second))
                    
                    if backup_day_code == -1:
                        if current_day_hour > backup_day_hour:
                            has_to_make_backup = True
                    else:
                        if backup_day_code == current_date.weekday():
                            if current_day_hour > backup_day_hour:
                                has_to_make_backup = True
                        
                    if has_to_make_backup:

                        self.web_core.data.admin_server_data["last_backup_date"] = str(dt.datetime.now())
                        self.web_core.data.data_tools.sql_update_all_system_admin_values(self.web_core.data.admin_server_data)
                        self.web_core.data.data_tools.set_system_log("BACKUP","Server make backup")
                        
                        Date_format = '%Y%m%d_%H%M%S'    
                        current_date_str :str = current_date.strftime(Date_format)
                        
                        backup_directory :str = self.web_core.data.admin_server_data["backup_path_directory"]
                        backup_directory = os.path.join(backup_directory, "DPRM_BACKUP_" + current_date_str)
                        
                        shutil.copytree(self.web_core.data_base_directory_path(), backup_directory)
                        
                        zip_file = zipfile.ZipFile(os.path.join(self.web_core.data.admin_server_data["backup_path_directory"], "DPRM_BACKUP_" + current_date_str+ ".zip"), 'w')
                        self.zip_directory(backup_directory, zip_file)
                        
                        shutil.rmtree(backup_directory)
                        
                        try:
                            os.rmdir(backup_directory)
                        except:
                            pass
