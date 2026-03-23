import os
import lm.TensorFlowApp as tfa

def StarUp():    
    
    tfa.TensorFlowApp(get_directory_root()).open_application()
    
def get_directory_root() -> str:
    
    this_file_full_path :str = os.path.realpath(__file__)
    this_file_name :str = os.path.basename(__file__)    

    return this_file_full_path[:-len(this_file_name)]    
    
if __name__ == "__main__":
    StarUp()
    