import datetime as dt
import time

import core.CoreInit as ci
import web.tools.BackUp as bk

NUMBER_KEY_ID_LIST :int = 101

class ThreadProcess():
    
    def __init__(self, CoreInit :ci.CoreInit):
        
        self.web_core = CoreInit
        self.BackUp :bk.BackUp = bk.BackUp(self.web_core)
        self.web_core.init_key_id_list(NUMBER_KEY_ID_LIST)
        
    def thread_process_task(self):
        
        self.web_core.is_web_server_task = True    
        start_time_span :dt.datetime = dt.datetime.now()
        key_id_list_reset_counter :int = 1
        
        while self.web_core.is_web_server_task:

            time.sleep(1)  
            
            current_time_span :dt.datetime = dt.datetime.now()
            diff_time_span = current_time_span - start_time_span
            
            if diff_time_span.total_seconds() > 60:
                
                key_id_list_reset_counter += 1
                
                if key_id_list_reset_counter > 10:
                    key_id_list_reset_counter = 1
                
                    self.web_core.reset_key_id_list(NUMBER_KEY_ID_LIST)
        
                self.BackUp.check_to_make_backup()
                
                start_time_span :dt.datetime = dt.datetime.now()
        
        self.web_thread_process = None