import core.user.workspace.WorkSpaceData as wd
import core.user.workspace.WorkspaceProcess as wp

import core.tools.DataBase as db

class WorkSpace:
    
    def __init__(self, user_directory_path :str):
        
        self.user_directory_path = user_directory_path
        self.data :wd.WorkSpaceData = None
        self.process :wp.WorkSpaceProcess = None
        self.admin_workspace :dict = {}
        
        self.name :str = ""
        
        self.is_active_workspace :bool = False
        
        self.is_on_acquisition :bool = False
        self.is_on_transformation :bool = False
        self.is_on_exploitation :bool = False
        
        self.is_valid_acquisition :bool = False
        self.is_valid_transformation :bool = False
        self.is_valid_exploitation :bool = False
        
        self.is_scheduled :bool = False
        self.schedule_code :str = ""
                
        self.is_error_message :bool = False
        self.message :str = ""
        
        self.current_result_name :str = ""
        
        self.data_base :db.DataBase = None
        self.data_base_transform :db.DataBase = None
        
    def reset_workspace(self):
        
        self.name = ""
        self.admin_workspace.clear()
        
        self.is_active_workspace = False
        
        self.is_on_acquisition = False
        self.is_on_transformation = False
        self.is_on_exploitation = False
        
        self.is_valid_acquisition = False
        self.is_valid_transformation = False
        self.is_valid_exploitation = False
        
        if not self.process == None:
            self.process.reset()
                
        self.is_error_message = False
        self.message = ""
        
    def set_workspace(self, worspace_name):
        
        self.name = worspace_name
        self.data = wd.WorkSpaceData(self.user_directory_path, self.name)
        self.process = wp.WorkSpaceProcess(self.data)
        
        self.set_workspace_admin_data()
        
    def set_workspace_admin_data(self):
        
        self.admin_workspace.clear()        
        self.admin_workspace = self.data.get_workspace_user_admin_data()
        
        self.is_on_acquisition = True if self.admin_workspace["is_on_acquisition"] == "TRUE" else False
        self.is_on_transformation = True if self.admin_workspace["is_on_transformation"] == "TRUE" else False
        self.is_on_exploitation = True if self.admin_workspace["is_on_exploitation"] == "TRUE" else False
        
        self.is_valid_acquisition = True if self.admin_workspace["is_valid_acquisition"] == "TRUE" else False
        self.is_valid_transformation = True if self.admin_workspace["is_valid_transformation"] == "TRUE" else False
        self.is_valid_exploitation = True if self.admin_workspace["is_valid_exploitation"] == "TRUE" else False
        
        self.is_active_workspace = True


    def check_is_valid_request(self, request_data_list :list, is_edit :bool = False) -> str:

        request_value :dict = {}

        for i in range(len(request_data_list)):
            try:
                request_value[str(request_data_list[i]).split("=")[0]] = str(request_data_list[i]).split("=")[1]
            except:
                request_value[str(request_data_list[i]).split("=")[0]] = ""
        try:

            if len(request_value["request_name"]) < 4:
                return "New request name has to be at least 4 characters long" 
               
            if len(request_value["request_name"]) > 25:
                return "New request name has to be at maximum 25 characters long" 
            
            if len(request_value["request_http"]) < 8:
                return "New request base has to be at least 8 characters long" 
            
            if not is_edit:
                if self.data.is_request_name_exist(request_value["request_name"]):
                    return "New request name already exist" 

        except:
            return "New request has corupted data" 

        return "" 
    
    def set_select_acquisition(self):
        
        self.is_on_acquisition = True
        self.is_on_transformation = False
        self.is_on_exploitation = False
    
    def set_select_transform(self):
        
        self.is_on_acquisition = False
        self.is_on_transformation = True
        self.is_on_exploitation = False
    
    def set_select_exploitation(self):
        
        self.is_on_acquisition = False
        self.is_on_transformation = False
        self.is_on_exploitation = True
    
    def set_valid_acquisition(self):
        
        self.is_valid_acquisition = True
        self.admin_workspace["is_valid_acquisition"] = "TRUE"
        self.data.set_workspace_user_admin_data(self.admin_workspace)
        
    def set_valid_transform(self):
        
        self.is_valid_transformation = True
        self.admin_workspace["is_valid_transformation"] = "TRUE"
        self.data.set_workspace_user_admin_data(self.admin_workspace)
        
    def set_valid_exploitation(self):
        
        self.is_valid_exploitation = True
        self.admin_workspace["is_valid_exploitation"] = "TRUE"
        self.data.set_workspace_user_admin_data(self.admin_workspace)
        
    def set_schedule(self, is_schedule :bool, schedule_code :str):
        
        self.is_scheduled = is_schedule
        
        if not self.is_scheduled:
            self.schedule_code = ""
            self.admin_workspace["is_scheduled"] = "FALSE"
            self.admin_workspace["schedule_code"] = ""    
        else:
            self.schedule_code = schedule_code
            self.admin_workspace["is_scheduled"] = "TRUE"
            self.admin_workspace["schedule_code"] = schedule_code   
        
        self.data.set_workspace_user_admin_data(self.admin_workspace)
        
    
    
        
        
        