
import shutil
import os

import core.user.UserData as ud
import core.user.workspace.WorkSpace as ws

class WorkSpaceCore:
    
    def __init__(self ):
        
        self.workspace :dict = {}
        self.workspace_list :list = []
        self.has_workspace :bool = False
        self.user_directoy_path :str = ""

        self.data :ud.UserData = None
        self.current_workspace :ws.WorkSpace = None
        
    def read_workspace_user(self, user_directory_path :str, user_data :ud.UserData):
        
        workspace_checked :list = []

        self.user_directoy_path = user_directory_path
        self.data = user_data
        
        workspace_dirs = os.listdir(self.user_directoy_path)
        self.workspace_list = self.data.get_workspace_list()
        self.current_workspace_name = self.data.get_default_workspace_name()

        if len(self.workspace_list) > 0:
            self.has_workspace = True

        for workspace in workspace_dirs:
            if os.path.isdir(os.path.join(self.user_directoy_path, workspace)):
                if not workspace in self.workspace_list:
                    try:
                        shutil.rmtree(os.path.join(self.user_directoy_path, workspace))
                    except:
                        pass
                else:

                    workspace_checked.append(workspace)

        if len(self.workspace_list) != len(workspace_checked):
            for i in range(len(self.workspace_list)):
                if not str(self.workspace_list[i]) in workspace_checked:
                    self.add_workspace(self.workspace_list[i])
                    
        if len(self.current_workspace_name) == 0:
            if len(self.workspace_list) > 0:
                self.current_workspace_name = self.workspace_list[0]
                self.data.set_default_workspace_name(self.current_workspace_name)
                
        if len(self.workspace_list) == 0:
            self.current_workspace_name = ""
            self.data.set_default_workspace_name("")
            
        self.current_workspace :ws.WorkSpace = ws.WorkSpace(self.user_directoy_path)
            
    def is_workspace_name_exist(self, workspace_name :str) -> bool:
        
        for i in range(len(self.workspace_list)):
            if self.workspace_list[i] == workspace_name:
                return True
        
        return False
        
    def add_new_workspace(self, workspace_name :str) -> str:
        
        if self.is_workspace_name_exist(workspace_name):
            return "Error: [" + str(workspace_name) + "] New workspace name already exist in your account!"    
        
        try:
            self.data.add_new_workspace(workspace_name)
            self.add_workspace(workspace_name)
            self.workspace_list.append(workspace_name)        
        except:
            return "Error: [" + str(workspace_name) + "] New workspace name not able to be create in your account [Conflit Name]!"    
        
        return ""
    
    def add_workspace(self, workspace_name :str) -> str:
        
        os.makedirs(os.path.join(self.user_directoy_path, workspace_name))
        
        if not self.has_workspace:
            self.has_workspace = True
    
    def remove_workspace(self, workspace_name :str) -> bool:
        
        self.data.delete_workspace(workspace_name)
        
        if self.is_workspace_name_exist(workspace_name):
            
            for i in range(len(self.workspace_list)):
                if self.workspace_list[i] == workspace_name:
                    self.workspace_list.pop(i)

                    try:
                        shutil.rmtree(os.path.join(self.user_directoy_path, workspace_name))
                    except:
                        pass
                    
                    if len(self.workspace_list) == 0:
                        self.has_workspace = False
                        
                    return True
                
        return False 