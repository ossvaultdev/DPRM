import requests
import xml.etree.ElementTree as ET
import xmltodict
import json
import os 

import core.tools.DataTransform as dtf
import core.tools.DataBase as db
    
import core.user.workspace.WorkSpaceData as wd

class WorkSpaceProcess:
    
    def __init__(self, data :wd.WorkSpaceData):
        
        self.data = data

    def reset(self):
        pass
    
    def do_api_all_request(self) -> db.DataBase:
        
        request_parameter_list :list = []
        request_parameter_dict :dict = {}
        data_base :db.DataBase = db.DataBase()
        
        request_parameter_list =  self.data.get_user_request_list()
        
        for i in range(len(request_parameter_list)):
            request_parameter_dict = request_parameter_list[i]
            data_base.append(self.do_api_request(request_parameter_dict["request_id"]), str(i+1))
        
        return data_base
    
    def do_api_request(self, request_id :str) -> db.DataBase:
        
        response_request :requests.Response = None
        response_dict :dict = {}
        request_parameter_list :list = []
        request_parameter_dict :dict = {}
        request_time_out :int = 4
        web_api_request :str = ""
        web_api_name :str = ""
        data_json :str = ""        
        
        header_dict :dict = {}
        query_dict :dict = {}
        
        request_parameter_list =  self.data.get_user_request_list(request_id)
        request_parameter_dict = request_parameter_list[0]

        web_api_request = request_parameter_dict["request_base"] 
        web_api_name = request_parameter_dict["name"]
        
        if len(request_parameter_dict["request_header"]) > 0:
            
            header_split :list = request_parameter_dict["request_header"].split(" ")
        
            try:
                            
                for header in header_split:
                    
                    header_split_next :list = str(header).split(",")
                    
                    header_split_next[0] = str(header_split_next[0])[1:-1:]
                    header_split_next[1] = str(header_split_next[1])[1:-1:]
                    
                    header_dict[header_split_next[0]] = header_split_next[1]
            except:
                pass
            
        if len(request_parameter_dict["request_query"]) > 0:
            
            query_split :list = request_parameter_dict["request_query"].split(" ")
        
            try:
                for query in query_split:
                    
                    query_split_next :list = str(query).split(",")
                    
                    query_split_next[0] = str(query_split_next[0])[1:-1:]
                    query_split_next[1] = str(query_split_next[1])[1:-1:]
                    
                    query_dict[query_split_next[0]] = query_split_next[1]
            except:
                pass
        
        # -------------------------------------------------------------------------------------------------------------------------
        # -----       USED FOR DEVELOPMENT PURPOSE    -----------------------------------------------------------------------------        
        # -------------------------------------------------------------------------------------------------------------------------
        # if web_api_name == "CATEGORY SERIES":            
            
        #     file_path = os.path.join(os.path.dirname(__file__), "TEMP_DATA", "fred_category_series.json")
        #     with open(file_path, "r", encoding="utf-8") as f:
        #         data_json = f.read()
                
        #     response_dict = json.loads(data_json)
                        
        # if web_api_name == "SERIE OBSERVATIONS":
            
        #     file_path = os.path.join(os.path.dirname(__file__), "TEMP_DATA", "fred_serie_observations.json")
        #     with open(file_path, "r", encoding="utf-8") as f:
        #         data_json = f.read()
                
        #     response_dict = json.loads(data_json)
        
        # if web_api_name == "MAPI SHAPE FILE":
            
        #     file_path = os.path.join(os.path.dirname(__file__), "TEMP_DATA", "fred_mapi_shape_file.json")
        #     with open(file_path, "r", encoding="utf-8") as f:
        #         data_json = f.read()
                
        #     response_dict = json.loads(data_json)
            
        # if web_api_name == "MAPI SERIES DATA":
            
        #     file_path = os.path.join(os.path.dirname(__file__), "TEMP_DATA", "fred_mapi_series_data.json")
        #     with open(file_path, "r", encoding="utf-8") as f:
        #         data_json = f.read()
                
        #     response_dict = json.loads(data_json)

        # if web_api_name == "DOW 30":
            
        #     file_path = os.path.join(os.path.dirname(__file__), "TEMP_DATA", "DOW_30.json")
        #     with open(file_path, "r", encoding="utf-8") as f:
        #         data_json = f.read()
                
        #     response_dict = json.loads(data_json)
        # -------------------------------------------------------------------------------------------------------------------------
        # -----       USED FOR DEVELOPMENT PURPOSE    -----------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------------------------------------------

        if len(response_dict) == 0:
            
            try:
                
                response_request = requests.get(web_api_request, headers=header_dict, params=query_dict, timeout=request_time_out)
                
                if str(response_request.status_code)[:1:] == "2":
                
                    if self.is_xml(response_request.text):
                        
                        response_dict = xmltodict.parse(response_request.text, attr_prefix="")
                        
                    elif self.is_valid_json(response_request.text):
                            
                        response_dict = json.loads(response_request.text)
                    else:
                        
                        for ligne in response_request.text.splitlines():
                            if ":" in ligne:
                                cle, valeur = ligne.split(":", 1)
                                response_dict[cle.strip()] = valeur.strip()

            
            except Exception as e:
                print("Error on request : ",e)
                
        data_tansform : dtf.DataTransform = dtf.DataTransform()

        return data_tansform.get_database_from_json(response_dict)
        
    def is_xml(self, data :str):
        
        try:
            ET.fromstring(data)
            return True
        except ET.ParseError:
            return False
        
    def is_valid_json(self, data :str):
        
        try:
            json.loads(data)
            return True
        except (ValueError, TypeError):
            return False
        