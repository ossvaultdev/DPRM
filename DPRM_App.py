import os

import app.CoreApp as ca
import core.CoreInit as ci

def StarUp():
    """
    Init and start main application admin programm
    """
    
    ca.CoreApp(ci.CoreInit(get_directory_root())).open_application()
    
def get_directory_root() -> str:
    """
    Return full directory root for base main programm      
    """
    
    this_file_full_path :str = os.path.realpath(__file__)
    this_file_name :str = os.path.basename(__file__)    

    return this_file_full_path[:-len(this_file_name)]    
    
if __name__ == "__main__":
    StarUp()
    