import sqlite3
import datetime
import os

import core.tools.Constant as cs

TABLE_NAME_WORSPACE_ADMIN :str = "workspace_admin"
TABLE_NAME_WORKSPACE_API_REQUEST :str = "api_request"

DEFAULT_DATA_WORKSPACE_ADMIN :dict = {"is_on_acquisition":"TRUE",                                  
                                      "is_on_transformation":"FALSE",
                                      "is_on_exploitation":"FALSE",
                                      "is_valid_acquisition":"FALSE",
                                      "is_valid_transformation":"FALSE",
                                      "is_valid_exploitation":"FALSE",
                                      "is_scheduled":"FALSE",
                                      "schedule_code":""}

class WorkSpaceData:
    
    def __init__(self, user_directory_path :str, workspace_name :str):
        
        self.user_directory_path = user_directory_path
        self.workspace_name = workspace_name
        
        self.user_workspace_full_path_data_base :str = os.path.join(self.user_directory_path, workspace_name, cs.WORKSPACE_DEFAULT_DATA_BASE_NAME)
        
        self.set_user_workspace_data()
    
    def set_user_workspace_data(self) -> dict:
        
        if not os.path.exists(self.user_workspace_full_path_data_base):
            self.create_default_database()
            
        self.check_default_workspace_user_table()
        
        return self.get_workspace_user_admin_data()
    
    def create_default_database(self):        
        """
        Create a default workspace user data base
        """
        with sqlite3.connect(self.user_workspace_full_path_data_base) as conn:
            pass
        
    def is_table_exist(self, table_name: str) -> bool:
        """
        Check if table exist on workspace database
        """
        try:
            with sqlite3.connect(self.user_workspace_full_path_data_base) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM " + table_name)
            return True            
            
        except sqlite3.OperationalError as e:
            return False
        
    def sql_execute_statement(self, sql_statements :str):
        """
        Execute SQL code to default database and commit
        """
        try:
            with sqlite3.connect(self.user_workspace_full_path_data_base) as conn:
                cursor = conn.cursor()
                cursor.execute(sql_statements)
                conn.commit()

        except sqlite3.OperationalError as e:
            print("Error on [SQL execute default statements on CoreData database]: ", e, "\n", sql_statements)
            return False
        
    def sql_get_execute_statement(self, sql_statements :str) -> list:
        """
        Execute SQL code to default database to extract data by row
        """
        
        return_array_list_value :list = []
        
        try:
            with sqlite3.connect(self.user_workspace_full_path_data_base) as conn:
                cursor = conn.cursor()
                cursor.execute(sql_statements)
                rows = cursor.fetchall()
                for row in rows:
                    row_detail_list :list = []
                    row = list(row)
                    for i in range(len(row)):
                        row_detail_list.append(row[i])
                    
                    return_array_list_value.append(row_detail_list)

        except sqlite3.OperationalError as e:
            print("Error on [SQL execute default statements on Workspace database]: ", e, "\n", sql_statements)
            
        return return_array_list_value
        
    def replace_tag_format(self, value_to_format :str) -> str:
        
        value_to_format = value_to_format.replace('<tag_two_point_h>', ':')
        value_to_format = value_to_format.replace('<tag_equal_value>', '=')
        
        return value_to_format
        
    def check_default_workspace_user_table(self):
        """
        Create and create if needed default workspace user table
        """
        
        sql_list_default_table :list[str] = []
        
        if not self.is_table_exist(TABLE_NAME_WORSPACE_ADMIN):
            sql_list_default_table.append(self.sql_default_workspace_admin_user_table())
            
        if not self.is_table_exist(TABLE_NAME_WORKSPACE_API_REQUEST):
            sql_list_default_table.append(self.sql_default_workspace_api_request_table())
            
            
        if len(sql_list_default_table) > 0:            
            try:
                with sqlite3.connect(self.user_workspace_full_path_data_base) as conn:
                    cursor = conn.cursor()
                    
                    for statement in sql_list_default_table:
                        cursor.execute(statement)

                    conn.commit()

            except sqlite3.OperationalError as e:
                print("Error on [Create default workspace user table]: ", e)
                
        self.check_default_workspace_admin_table_values()
        
    def sql_default_workspace_admin_user_table(self) -> str:
        
        sql_statements :str = """CREATE TABLE IF NOT EXISTS """ + TABLE_NAME_WORSPACE_ADMIN + """ (
                                        name text NOT NULL, 
                                        value text NOT NULL
                                    );"""
        return sql_statements
    
    def sql_default_workspace_api_request_table(self) -> str:
        
        sql_statements :str = """CREATE TABLE IF NOT EXISTS """ + TABLE_NAME_WORKSPACE_API_REQUEST + """ (
                                        id INTEGER PRIMARY KEY, 
                                        name text NOT NULL,                                         
                                        description text, 
                                        api_key text,
                                        request_base text NOT NULL, 
                                        request_type text,
                                        request_header text, 
                                        request_query text, 
                                        extract_valid_key text, 
                                        extract_start_key text, 
                                        extract_end_key text, 
                                        is_valid_request INTEGER NOT NULL DEFAULT 0,
                                        is_locked_request INTEGER NOT NULL DEFAULT 0,
                                        creation_date DATE
                                    );"""                                    
        return sql_statements
        
    def check_default_workspace_admin_table_values(self):
        
        try:
            with sqlite3.connect(self.user_workspace_full_path_data_base) as conn:
                
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM " + TABLE_NAME_WORSPACE_ADMIN)
                rows = cursor.fetchall()
                
                add_default_list :dict = {}
                
                for dict_values in DEFAULT_DATA_WORKSPACE_ADMIN:
                    
                    has_default_value :bool = False
                    
                    for row in rows:
                        row_value :tuple = tuple(row)     
                        
                        if row_value[0] == dict_values:
                            has_default_value = True
                            break
                    
                    if not has_default_value:
                            add_default_list[dict_values] = DEFAULT_DATA_WORKSPACE_ADMIN[dict_values]   
                
                if len(add_default_list) > 0:
                    
                    sql_values :str = ""
                    
                    for dict_values in add_default_list:
                        
                        sql_values += "('" + dict_values + "','" + add_default_list[dict_values] + "'),"
                        
                    sql_values = sql_values[0:len(sql_values)-1]
                    
                    sql_statements :str = "INSERT INTO " + TABLE_NAME_WORSPACE_ADMIN + "(name,value)\nVALUES" + sql_values 
                    
                    try:
                        with sqlite3.connect(self.user_workspace_full_path_data_base) as conn:
                            cursor = conn.cursor()
                            cursor.execute(sql_statements)
                            conn.commit()

                    except sqlite3.OperationalError as e:
                        print("Error on [Create default values on workspace user_admin table]: ", e, "\n", sql_statements)
            
        except sqlite3.OperationalError as e:
            pass
        
    def get_workspace_user_admin_data(self) -> dict:
        """
        Read all workspace admin user data from data base
        """
        workspace_admin_user_data :dict[str] = {}
        
        try:
            with sqlite3.connect(self.user_workspace_full_path_data_base) as conn:
                
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM " + TABLE_NAME_WORSPACE_ADMIN)
                rows = cursor.fetchall()
                
                for row in rows:
                    row = list(row)
                    workspace_admin_user_data[str(row[0])] = str(row[1])

        except sqlite3.OperationalError as e:
            print("Error on [Read workspace data user server system table]: ", e)
            
        return workspace_admin_user_data
    
    def set_workspace_user_admin_data(self, workspace_admin_user_data :dict):
        
        sql_statements :str = ""
        sql_statements_list :list [str] = []
        
        for dict_val in workspace_admin_user_data:
            
            sql_statements = "UPDATE " + TABLE_NAME_WORSPACE_ADMIN + "\n"
            sql_statements += "SET value ='" + str(workspace_admin_user_data[dict_val]) + "'" + "\n"
            sql_statements += "WHERE name = '" + dict_val + "'" + "\n"
            
            sql_statements_list.append(sql_statements)
        
        try:
            with sqlite3.connect(self.user_workspace_full_path_data_base) as conn:
                cursor = conn.cursor()
                
                for i in range(len(sql_statements_list)):
                    cursor.execute(sql_statements_list[i])
                    
                conn.commit()

        except sqlite3.OperationalError as e:
            print("Error on [Update all value on workspace_admin table]: ", e, "\n", sql_statements_list)
            return False
        
        return True
        
        
    
    def delete_request(self, request_id :str):
        
        sql_statements :str = """DELETE FROM """ + TABLE_NAME_WORKSPACE_API_REQUEST + "\n"
        sql_statements += " WHERE id = " + request_id
        
        try:

            self.sql_execute_statement(sql_statements)                                    
            
        except:
            pass    
    
    def add_new_request(self, new_request :list):

        request_value :dict = {}

        for i in range(len(new_request)):
            try:
                request_value[str(new_request[i]).split("=")[0]] = str(new_request[i]).split("=")[1]
            except:
                request_value[str(new_request[i]).split("=")[0]] = ""

        sql_substatements :str = ""

        sql_substatements = "('" + self.replace_tag_format(str(request_value["request_name"])) +  "','" 
        sql_substatements +=  self.replace_tag_format(str(request_value["request_description"]))  +  "','" 
        sql_substatements +=  self.replace_tag_format(str(request_value["request_api_key"]))  +  "','" 
        sql_substatements +=  self.replace_tag_format(str(request_value["request_http"]))  +  "','"
        sql_substatements +=  self.replace_tag_format(str(request_value["request_type"]))  +  "','"
        sql_substatements +=  self.replace_tag_format(str(request_value["request_header"]))  +  "','"
        sql_substatements +=  self.replace_tag_format(str(request_value["request_query"]))  +  "','"
        sql_substatements +=  self.replace_tag_format(str(request_value["request_valid_key"]))  +  "','" 
        sql_substatements +=  self.replace_tag_format(str(request_value["request_start_key"]))  +  "','"
        sql_substatements +=  self.replace_tag_format(str(request_value["request_end_key"]))  +  "','"
        sql_substatements +=  str(datetime.datetime.now()) + "')"
        
        sql_statements :str = """INSERT INTO """ + TABLE_NAME_WORKSPACE_API_REQUEST + """ ( 
                                                    name, description, api_key, request_base, request_type, 
                                                    request_header, request_query, extract_valid_key, 
                                                    extract_start_key, extract_end_key, creation_date
                                        )VALUES""" + sql_substatements                            
        try:

            self.sql_execute_statement(sql_statements)                                    
            
        except:
            pass    


    def update_request(self, update_request :list):

        request_value :dict = {}

        for i in range(len(update_request)):
            try:
                request_value[str(update_request[i]).split("=")[0]] = str(update_request[i]).split("=")[1]
            except:
                request_value[str(update_request[i]).split("=")[0]] = ""
                
        sql_statements :str = ""
                
        sql_statements = "UPDATE " + TABLE_NAME_WORKSPACE_API_REQUEST + "\n"
        sql_statements += "SET name = '" + self.replace_tag_format(str(request_value["request_name"])) + "',"
        sql_statements +=    " description = '" + self.replace_tag_format(str(request_value["request_description"])) + "',"
        sql_statements +=    " api_key = '" + self.replace_tag_format(str(request_value["request_api_key"])) + "',"
        sql_statements +=    " request_base = '" + self.replace_tag_format(str(request_value["request_http"])) + "',"
        sql_statements +=    " request_type = '" + self.replace_tag_format(str(request_value["request_type"])) + "',"
        sql_statements +=    " request_header = '" + self.replace_tag_format(str(request_value["request_header"])) + "',"
        sql_statements +=    " request_query = '" + self.replace_tag_format(str(request_value["request_query"])) + "',"
        sql_statements +=    " extract_valid_key = '" + self.replace_tag_format(str(request_value["request_valid_key"])) + "',"
        sql_statements +=    " extract_start_key = '" + self.replace_tag_format(str(request_value["request_start_key"])) + "',"
        sql_statements +=    " extract_end_key = '" + self.replace_tag_format(str(request_value["request_end_key"])) + "' " + "\n"
        sql_statements += "WHERE id = " + str(request_value["request_id"])

        try:

            self.sql_execute_statement(sql_statements)
            
        except:
            return False
        
        return True

    def is_request_name_exist(self, workspace_name :str) -> bool:

        if int(self.sql_get_execute_statement("SELECT count(*) FROM " + 
                                              TABLE_NAME_WORKSPACE_API_REQUEST + 
                                              " WHERE name='" + workspace_name + "'")[0][0]) > 0:
            return True
        
        return False
    
    def get_user_request_list(self, request_id :str = "-1") -> list:
        
        sql_statements :str = ""
        request_list :list = []
        
        if request_id == "-1":
            sql_statements = "SELECT * FROM " + TABLE_NAME_WORKSPACE_API_REQUEST
        else:
            sql_statements = "SELECT * FROM " + TABLE_NAME_WORKSPACE_API_REQUEST
            sql_statements += " WHERE id = " + str(request_id)
            
        
        request_list = self.sql_get_execute_statement(sql_statements)
        
        user_request_list :list = []
        
        for i in range(len(request_list)):
            
            data_request :dict = {}
            
            data_request["request_id"] = str(request_list[i][0])
            data_request["name"] = str(request_list[i][1])
            data_request["description"] = str(request_list[i][2])
            data_request["api_key"] = str(request_list[i][3])
            data_request["request_base"] = str(request_list[i][4])
            data_request["request_type"] = str(request_list[i][5])
            data_request["request_header"] = str(request_list[i][6])
            data_request["request_query"] = str(request_list[i][7])
            data_request["request_valid_key"] = str(request_list[i][8])
            data_request["request_start_key"] = str(request_list[i][9])
            data_request["request_end_key"] = str(request_list[i][10])
            
            user_request_list.append(data_request)
            
        return user_request_list