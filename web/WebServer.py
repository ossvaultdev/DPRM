from flask import Flask, request, render_template

import threading
import sys

import core.tools.Constant as cs
import core.user.User as cu
import core.CoreInit as ci

import web.tools.ThreadProcess as tp
import web.WebRoute as wb

# IN CASE OF ........................................................
# import sys
# root_dir : str = os.path.dirname(os.path.dirname(__file__))
# sys.path.append(root_dir)
# IN CASE OF ........................................................

app = Flask(__name__)
web_core :ci.CoreInit = None
web_route :wb.WebRoute = None

web_thread_process = threading.Thread()

class WebServer():
    
    def __init__(self, CoreInit :ci.CoreInit):
        
        global web_core
        web_core = CoreInit
        
        global web_route
        web_route = wb.WebRoute(web_core)
        
        self.TreadProcess :tp.ThreadProcess = tp.ThreadProcess(web_core)
        
        web_server_ip_port :str = web_core.data.admin_server_data["server_ip_port"]
        web_server_ip :str = web_server_ip_port.split(":")[0]
        web_server_port :int = int(web_server_ip_port.split(":")[1])
        
        self.web_thread_process = threading.Thread(target=self.TreadProcess.thread_process_task)
        self.web_thread_process.start()
        
        web_core.data.data_tools.set_system_log("START","Starting Server")
        
        # ----------------------------------------------------------------------------
        # REMOVE DEBUG FOR RELEASE ---------------------------------------------------
        IS_SERVER_DEBUG :bool = False
        # REMOVE DEBUG FOR RELEASE ---------------------------------------------------
        # ----------------------------------------------------------------------------
        
        app.run(host=web_server_ip, port=web_server_port, debug=IS_SERVER_DEBUG)    
        
        web_core.is_web_server_task = False
        web_core.data.data_tools.set_system_log("STOP","Server Stoped")        
        self.web_thread_process = None
        sys.exit()
        
           
    @app.route('/', methods = ['POST', 'GET']) 
    def main(): 
        
        if request.method == 'POST': 
            
            key_id :str = request.form['KEY_ID'] 
            
            if len(key_id.split("-")) > 1:

                if request.form['KEY_VALUE'] == cs.WEB_TAG_ROUTAGE_LOGOUT:
                       
                       return web_route.session_logout(key_id)

                return web_route.session_frame(request.form['KEY_ID'] + ":" + request.form['KEY_VALUE'])
            
            if web_core.is_random_key_id(key_id):
            
                key_value :str = request.form['KEY_VALUE'] 
                
                if key_value.split(":")[0] == cs.WEB_TAG_REQUEST_SIGNIN:
                    
                    return web_route.user_signin(cu.User())                    

                if key_value.split(":")[0] == cs.WEB_TAG_REQUEST_LOGIN:
                                    
                    return web_route.user_login(cu.User())
                                    
                if key_value.split(":")[0] == cs.WEB_TAG_REQUEST_LOGIN_SUBMIT:
                    
                    return web_route.user_login_submit(key_value, request.remote_addr)

                if key_value.split(":")[0] == cs.WEB_TAG_REQUEST_SIGNIN_SUBMIT:
                    
                    return web_route.user_signin_submit(key_value, request.remote_addr)

        return web_route.user_home()
    
    
    @app.route('/frame/<frame_id_value>', methods = ['POST', 'GET']) 
    def frame(frame_id_value):
        
        key_id :str = ""
        
        if len(frame_id_value) > 0:
            
            key_id = str(frame_id_value).split(":")[0]
            
            if len(key_id.split("-")) > 1:
                
                return web_route.session_frame(frame_id_value)
        
            if web_core.is_random_key_id(key_id):
        
                if len(str(frame_id_value).split(":")[1]) > 0:
                    return web_route.user_frame(str(frame_id_value).split(":")[1])    
        
        return render_template('global/error.html',error_msg="Frame ID not valid")
    