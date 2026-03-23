import datetime

import core.CoreInit as ci
import web.WebServer as ws

class CoreWeb():
  
  def __init__(self, CoreInit :ci.CoreInit):
    
    self.CoreInit = CoreInit
    
    if len(self.CoreInit.data.admin_server_data["first_server_start_date"]) == 0:
      self.CoreInit.data.admin_server_data["first_server_start_date"] = str(datetime.datetime.now()).split(".")[0].replace("-",".")
      
    self.CoreInit.data.admin_server_data["last_server_start_date"] = str(datetime.datetime.now()).split(".")[0].replace("-",".")
    
    self.CoreInit.data.data_tools.sql_update_all_system_admin_values(self.CoreInit.data.admin_server_data)
    
    
  def get_core_data_base_path(self) -> str:

    return self.CoreInit.data_base_path
  
  def start_server(self):
    
    web_server = ws.WebServer(self.CoreInit)
    
    
