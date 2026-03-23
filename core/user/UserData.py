import sqlite3
import hashlib
import datetime
import os 

import core.tools.Constant as cs

TABLE_NAME_USER_ADMIN :str = "user_admin"
TABLE_NAME_USER_WORKSPACE :str = "user_workspace"

DEFAULT_DATA_USER_ADMIN :dict = {"default_workspace":"",                                  
                                 "last_user_login_date":"",
                                 "last_user_logout_date":""}

class UserData:
    
    def __init__(self, user_directory_path :str):
        
        self.user_directory_path = user_directory_path
        self.user_full_path_data_base :str = os.path.join(self.user_directory_path, cs.USR_DEFAULT_MAIN_DATA_BASE_NAME)
         
    def set_user_data(self) -> dict:
        
        if not os.path.exists(self.user_full_path_data_base):
            self.create_default_database()
            
        self.check_default_user_table()
        
        return self.get_user_admin_data()
        
                
    def create_default_database(self):        
        """
        Create a default user data base
        """
        with sqlite3.connect(self.user_full_path_data_base) as conn:
            pass
        
    def create_database(self, full_path_data_base :str):        
        """
        Create a default user data base
        """
        with sqlite3.connect(full_path_data_base) as conn:
            pass
        
    def is_table_exist(self, table_name: str) -> bool:
        """
        Check if table exist on selected database
        """
        try:
            with sqlite3.connect(self.user_full_path_data_base) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM " + table_name)
            return True            
            
        except sqlite3.OperationalError as e:
            return False
        
    def is_table_exist_on_data_base(self, table_name: str, full_path_data_base :str) -> bool:
        """
        Check if table exist on selected database
        """
        try:
            with sqlite3.connect(full_path_data_base) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM " + table_name)
            return True            
            
        except sqlite3.OperationalError as e:
            return False
        
    def check_default_user_table(self):
        """
        Create and create if needed default user table
        """
        
        sql_list_default_table :list[str] = []
        
        if not self.is_table_exist(TABLE_NAME_USER_ADMIN):
            sql_list_default_table.append(self.sql_default_admin_user_table())
            
        if not self.is_table_exist(TABLE_NAME_USER_WORKSPACE):
            sql_list_default_table.append(self.sql_default_workspace_user_table())
            
        if len(sql_list_default_table) > 0:            
            try:
                with sqlite3.connect(self.user_full_path_data_base) as conn:
                    cursor = conn.cursor()
                    
                    for statement in sql_list_default_table:
                        cursor.execute(statement)

                    conn.commit()

            except sqlite3.OperationalError as e:
                print("Error on [Create default user table]: ", e)
                
        self.check_default_system_admin_table_values()
                
    def check_default_system_admin_table_values(self):
        
        try:
            with sqlite3.connect(self.user_full_path_data_base) as conn:
                
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM " + TABLE_NAME_USER_ADMIN)
                rows = cursor.fetchall()
                
                add_default_list :dict = {}
                
                for dict_values in DEFAULT_DATA_USER_ADMIN:
                    
                    has_default_value :bool = False
                    
                    for row in rows:
                        row_value :tuple = tuple(row)     
                        
                        if row_value[0] == dict_values:
                            has_default_value = True
                            break
                    
                    if not has_default_value:
                            add_default_list[dict_values] = DEFAULT_DATA_USER_ADMIN[dict_values]   
                
                if len(add_default_list) > 0:
                    
                    sql_values :str = ""
                    
                    for dict_values in add_default_list:
                        
                        sql_values += "('" + dict_values + "','" + add_default_list[dict_values] + "'),"
                        
                    sql_values = sql_values[0:len(sql_values)-1]
                    
                    sql_statements :str = "INSERT INTO " + TABLE_NAME_USER_ADMIN + "(name,value)\nVALUES" + sql_values 
                    
                    try:
                        with sqlite3.connect(self.user_full_path_data_base) as conn:
                            cursor = conn.cursor()
                            cursor.execute(sql_statements)
                            conn.commit()

                    except sqlite3.OperationalError as e:
                        print("Error on [Create default values on user_admin table]: ", e, "\n", sql_statements)
            
        except sqlite3.OperationalError as e:
            pass
            
    def sql_default_admin_user_table(self) -> str:
        
        sql_statements :str = """CREATE TABLE IF NOT EXISTS """ + TABLE_NAME_USER_ADMIN + """ (
                                        name text NOT NULL, 
                                        value text NOT NULL
                                    );"""
        return sql_statements
    
    def sql_default_workspace_user_table(self) -> str:
        
        sql_statements :str = """CREATE TABLE IF NOT EXISTS """ + TABLE_NAME_USER_WORKSPACE + """ (
                                        id INTEGER PRIMARY KEY, 
                                        name text NOT NULL, 
                                        description text NOT NULL, 
                                        creation_date DATE
                                    );"""
                                    
        return sql_statements
    
    def get_user_admin_data(self) -> dict:
        """
        Read all admin user data from data base
        """
        admin_user_data :dict[str] = {}
        
        try:
            with sqlite3.connect(self.user_full_path_data_base) as conn:
                
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM " + TABLE_NAME_USER_ADMIN)
                rows = cursor.fetchall()
                
                for row in rows:
                    row = list(row)
                    admin_user_data[str(row[0])] = str(row[1])

        except sqlite3.OperationalError as e:
            print("Error on [Read data user server system table]: ", e)
            
        return admin_user_data
    
    def get_country_definition(self, country_id :str,  main_data_full_path :str) -> str:
        
        try:
            with sqlite3.connect(main_data_full_path) as conn:
                
                cursor = conn.cursor()
                
                cursor.execute("SELECT name FROM user_country WHERE id = '" + country_id + "'")
                rows = cursor.fetchall()
                
                for row in rows:
                    return str(row[0])
                    

        except sqlite3.OperationalError as e:
            print("Error on [Read data contry definition user table]: ", e)
            
        return ""    
    
    def replace_tag_format(self, value_to_format :str) -> str:
        
        value_to_format = value_to_format.replace('<tag_two_point_h>', ':')
        value_to_format = value_to_format.replace('<tag_equal_value>', '=')
        
        return value_to_format
    
    def sql_execute_statement(self, sql_statements :str, data_base_path :str):
        """
        Execute SQL code to default database and commit
        """
        try:
            with sqlite3.connect(data_base_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql_statements)
                conn.commit()

        except sqlite3.OperationalError as e:
            print("Error on [SQL execute default statements on CoreData database]: ", e, "\n", sql_statements)
            return False
        
    def sql_get_execute_statement(self, sql_statements :str, database_path :str) -> list:
        """
        Execute SQL code to default database to extract data by row
        """
        
        return_array_list_value :list = []
        
        try:
            with sqlite3.connect(database_path) as conn:
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
            print("Error on [SQL execute default statements on " + database_path + " database]: ", e, "\n", sql_statements)
            
        return return_array_list_value
    
    def update_user_settings(self, frame_value_list :list, user_id :str, main_data_full_path :str) -> bool:
        
        sql_statements :str = ""
                
        sql_statements = "UPDATE " + "user_main" + "\n"
        sql_statements += "SET first_name = '" + str(self.replace_tag_format(frame_value_list[2].split("=")[1])) + "',"
        sql_statements +=    " last_name = '" + str(self.replace_tag_format(frame_value_list[3].split("=")[1])) + "',"
        sql_statements +=    " address = '" + str(self.replace_tag_format(frame_value_list[4].split("=")[1])) + "',"
        sql_statements +=    " country = '" + str(self.replace_tag_format(frame_value_list[5].split("=")[1])) + "',"
        sql_statements +=    " email = '" + str(self.replace_tag_format(frame_value_list[6].split("=")[1])) + "',"
        sql_statements +=    " phone = '" + str(self.replace_tag_format(frame_value_list[7].split("=")[1])) + "' " + "\n"
        sql_statements += "WHERE user_main.id = " + str(user_id)
        
        try:

            self.sql_execute_statement(sql_statements, main_data_full_path)
            
        except:
            return False
        
        return True
    
    def get_salt_pwd_by_user_id(self, user_id :str, main_data_full_path :str) -> str:
        
        try:
            with sqlite3.connect(main_data_full_path) as conn:
                
                cursor = conn.cursor()
                
                cursor.execute("SELECT salt_pwd FROM user_main WHERE id = " + str(user_id))
                rows = cursor.fetchall()
                
                for row in rows:
                    return str(row[0])

        except sqlite3.OperationalError as e:
            print("Error on [Read salt pwd definition on user table]: ", e)
            
        return ""
    
    def update_user_password(self, new_password :str, user_id :str, main_data_full_path :str) -> bool:

        sql_statements :str = ""

        user_salt_pwd :str = self.get_salt_pwd_by_user_id(user_id, main_data_full_path)
        new_user_pwd :str = user_salt_pwd + new_password + user_salt_pwd
        new_user_pwd = hashlib.sha256(new_user_pwd.encode()).hexdigest() 
                
        sql_statements = "UPDATE user_main" + "\n"
        sql_statements += "SET password = '" + new_user_pwd + "'\n"
        sql_statements += "WHERE user_main.id = " + str(user_id)
        
        try:
            self.sql_execute_statement(sql_statements, main_data_full_path)
        except:
            return False
        
        return True
        
    def close_account(self, user_id :str, main_data_full_path :str) -> bool:
        
        sql_statements :str = ""
        
        sql_statements = "UPDATE " + "user_main" + "\n"
        sql_statements += "SET is_active = 0\n"
        sql_statements += "WHERE user_main.id = " + str(user_id)
        
        try:

            self.sql_execute_statement(sql_statements, main_data_full_path)
            
        except:
            return False
        
        return True

    def get_workspace_list(self) -> list:

        workspace_list :list = []

        sql_statements :str = """SELECT name FROM """ + TABLE_NAME_USER_WORKSPACE 

        sql_row_result_list :list = self.sql_get_execute_statement(sql_statements, self.user_full_path_data_base)

        for i in range(len(sql_row_result_list)):
            workspace_list.append(sql_row_result_list[i][0])

        return workspace_list
    
    def add_new_workspace(self, workspace_name :str):

        sql_substatements :str = ""

        sql_substatements = "('" + workspace_name +  "','" 
        sql_substatements += "','"
        sql_substatements +=  str(datetime.datetime.now()) + "')"
        
        sql_statements :str = """INSERT INTO """ + TABLE_NAME_USER_WORKSPACE + """ ( 
                                                    name, description, creation_date
                                        )VALUES""" + sql_substatements      

        try:

            self.sql_execute_statement(sql_statements, self.user_full_path_data_base)                                    
            
        except:
            pass     

    def delete_workspace(self, workspace_name :str):  

        sql_statements :str = "DELETE FROM " + TABLE_NAME_USER_WORKSPACE  
        sql_statements += " WHERE name = '" + workspace_name + "'"

        try:

            self.sql_execute_statement(sql_statements, self.user_full_path_data_base)                                    
            
        except:
            pass    
        
    def set_user_login(self) -> bool:
        
        sql_statements :str = ""
        
        sql_statements = "UPDATE " + TABLE_NAME_USER_ADMIN + "\n"
        sql_statements += "SET value = '" + str(datetime.datetime.now()) + "'\n"
        sql_statements += "WHERE name = 'last_user_login_date'" 
        
        try:

            self.sql_execute_statement(sql_statements, self.user_full_path_data_base)
            
        except:
            return False
        
        return True
    
    def set_user_logout(self) -> bool:
        
        sql_statements :str = ""
        
        sql_statements = "UPDATE " + TABLE_NAME_USER_ADMIN + "\n"
        sql_statements += "SET value = '" + str(datetime.datetime.now()) + "'\n"
        sql_statements += "WHERE name = 'last_user_logout_date'" 
        
        try:

            self.sql_execute_statement(sql_statements, self.user_full_path_data_base)
            
        except:
            return False
        
        return True
    
    def get_default_workspace_name(self) -> str:
        
        return str(self.sql_get_execute_statement("SELECT value FROM " + TABLE_NAME_USER_ADMIN + 
                                                  " WHERE name='default_workspace'", 
                                                  self.user_full_path_data_base)[0][0])
    
    def set_default_workspace_name(self, workspace_name :str) -> bool:
        
        sql_statements :str = ""
        
        sql_statements = "UPDATE " + TABLE_NAME_USER_ADMIN + "\n"
        sql_statements += "SET value = '" + workspace_name + "'\n"
        sql_statements += "WHERE name = 'default_workspace'" 
        
        try:

            self.sql_execute_statement(sql_statements, self.user_full_path_data_base)
            
        except:
            return False
        
        return True
        