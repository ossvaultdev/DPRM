import DPRM_App as dpa
import web.CoreWeb as cw
import core.CoreInit as ci

def StarUp():
    
    cw.CoreWeb(ci.CoreInit(dpa.get_directory_root())).start_server()

if __name__ == "__main__":
    StarUp()
            