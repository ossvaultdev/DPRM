import os 

import lm.MainWindows.WindowsMain as mw
import core.tools.Constant as cs

class TensorFlowApp():
  
    def __init__(self,  common_root_ini_path: str):
    
        self.common_root_ini_path = os.path.join(common_root_ini_path, cs.INIT_DIRECTORY_TENSORFLOW)
        
    def open_application(self):
        
        current_windows = mw.WindowsMain(self.common_root_ini_path)
        current_windows.get_windows()  
        