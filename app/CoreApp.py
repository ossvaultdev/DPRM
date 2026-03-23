import core.CoreInit as ci
import app.MainWindows.WindowsLogin as lw   
import app.MainWindows.WindowMain as aw

# https://www.pythontutorial.net/tkinter/

class CoreApp():
  
  def __init__(self, CoreInit :ci.CoreInit):
    
    self.CoreInit = CoreInit
    self.exit_button = None
        
  def get_core_data_base_path(self) -> str:
    
    return self.CoreInit.data_base_path
  
    
  def open_application(self):
    
    current_windows = lw.LoginWindows
    current_windows.get_windows(self)
    
    if len(self.CoreInit.admin_login)> 0 and self.CoreInit.admin_login == self.CoreInit.data.admin_server_data["admin_password"]:
      current_windows = aw.AdminWindows
      current_windows.get_windows(self)  
      
    # current_windows = aw.AdminWindows
    # current_windows.get_windows(self)  
      

      
    
  

    
  
  
    
    
    
  
    

