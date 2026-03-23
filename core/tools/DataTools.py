import sqlite3
import random
import hashlib
import datetime

import core.user.User as cu

TABLE_NAME_SYS_ADMIN :str = "sys_admin"
TABLE_NAME_SYS_LOG :str = "sys_log"
TABLE_NAME_SYS_BACKUP_DEF :str = "sys_backup_definition"
TABLE_NAME_SYS_PROXY_REQUEST :str = "sys_proxy_request"
TABLE_NAME_SYS_REDIRECTION_SERVER :str = "sys_redirection_server"

TABLE_NAME_USER_MAIN :str = "user_main"
TABLE_NAME_USER_LOG :str = "user_log"
TABLE_NAME_USER_COUNTRY :str = "user_country"

class DataTools:
    
    def __init__(self, database_path :str):
        self.database_path = database_path
    
    def create_default_database(self):        
        """
        Create a default admin data base
        """
        with sqlite3.connect(self.database_path) as conn:
            pass

    def sql_execute_statement(self, sql_statements :str):
        """
        Execute SQL code to default database and commit
        """
        try:
            with sqlite3.connect(self.database_path) as conn:
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
            with sqlite3.connect(self.database_path) as conn:
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
            print("Error on [SQL execute default statements on CoreData database]: ", e, "\n", sql_statements)
            
        return return_array_list_value

    def sql_get_count_from_table(self, table_name :str) -> int:
        """
        Execute SQL code to default database
        """

        sql_statements :str = "SELECT COUNT(*) FROM " + table_name

        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql_statements)
                rows = cursor.fetchall()
                strvalue :str = " ".join(map(str,rows)).replace('(','').replace(')','').replace(',','')
                return int(strvalue)

        except sqlite3.OperationalError as e:
            print("Error on [SQL execute default statements on CoreData database]: ", e, "\n", sql_statements)
            return False
        
    def sql_is_count_exist_statements(self, sql_statements :str) -> bool:
        """
        Execute SQL code to default database if count > 0 then True
        """

        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql_statements)
                rows = cursor.fetchall()
                strvalue :str = " ".join(map(str,rows)).replace('(','').replace(')','').replace(',','')

                if int(strvalue) > 0:
                    return True 
            
                return False

        except sqlite3.OperationalError as e:
            print("Error on [SQL execute default statements on CoreData database]: ", e, "\n", sql_statements)
            return False
    
        
    def get_admin_server_data(self) -> dict:
        """
        Read all admin server data from data base
        """
        admin_server_data :dict[str] = {}
        
        try:
            with sqlite3.connect(self.database_path) as conn:
                
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM " + TABLE_NAME_SYS_ADMIN)
                rows = cursor.fetchall()
                
                for row in rows:
                    row = list(row)
                    admin_server_data[str(row[0])] = str(row[1])

        except sqlite3.OperationalError as e:
            print("Error on [Read data admin server system table]: ", e)
            
        return admin_server_data
            
    def check_default_system_table(self):
        """
        Create and create if needed default system table
        """
        import core.tools.DataDefault as df
        
        sql_list_default_table :list[str] = []
        
        if not self.is_table_exist(TABLE_NAME_SYS_ADMIN):
            sql_list_default_table.append(self.sql_default_admin_system_table())
            
        if not self.is_table_exist(TABLE_NAME_SYS_LOG):
            sql_list_default_table.append(self.sql_default_admin_log_table())
            
        if not self.is_table_exist(TABLE_NAME_USER_MAIN):
            sql_list_default_table.append(self.sql_default_user_system_table())
            
        if not self.is_table_exist(TABLE_NAME_USER_LOG):
            sql_list_default_table.append(self.sql_default_user_log_table())    
            
        if not self.is_table_exist(TABLE_NAME_USER_COUNTRY):
            sql_list_default_table.append(self.sql_default_user_country_table())   

        if not self.is_table_exist(TABLE_NAME_SYS_BACKUP_DEF):
            sql_list_default_table.append(self.sql_default_admin_backup_definition_table())   
            
        if not self.is_table_exist(TABLE_NAME_SYS_PROXY_REQUEST):
            sql_list_default_table.append(self.sql_default_admin_proxy_request_table())   
        
        if not self.is_table_exist(TABLE_NAME_SYS_REDIRECTION_SERVER):
            sql_list_default_table.append(self.sql_default_admin_redirection_server_table())   
            
        if len(sql_list_default_table) > 0:            
            try:
                with sqlite3.connect(self.database_path) as conn:
                    cursor = conn.cursor()
                    
                    for statement in sql_list_default_table:
                        cursor.execute(statement)

                    conn.commit()

            except sqlite3.OperationalError as e:
                print("Error on [Create default system table]: ", e)
        
        self.check_default_system_admin_table_values()

        if self.sql_get_count_from_table(TABLE_NAME_SYS_BACKUP_DEF) != len(df.DEFAULT_DATA_SYS_BACKUP_DEF):
            self.sql_default_data_set_admin_backup_definition()
            
        if self.sql_get_count_from_table(TABLE_NAME_USER_COUNTRY) != len(df.DEFAULT_DATA_USER_COUNTRY_DEF):
            self.sql_default_data_set_user_country_definition()
        
    def check_default_system_admin_table_values(self):
        
        import core.tools.DataDefault as df
        
        try:
            with sqlite3.connect(self.database_path) as conn:
                
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM " + TABLE_NAME_SYS_ADMIN)
                rows = cursor.fetchall()
                
                add_default_list :dict = {}
                
                for dict_values in df.DEFAULT_DATA_SYS_ADMIN:
                    
                    has_default_value :bool = False
                    
                    for row in rows:
                        row_value :tuple = tuple(row)     
                        
                        if row_value[0] == dict_values:
                            has_default_value = True
                            break
                    
                    if not has_default_value:
                            add_default_list[dict_values] = df.DEFAULT_DATA_SYS_ADMIN[dict_values]   
                
                if len(add_default_list) > 0:
                    
                    sql_values :str = ""
                    
                    for dict_values in add_default_list:
                        
                        sql_values += "('" + dict_values + "','" + add_default_list[dict_values] + "'),"
                        
                    sql_values = sql_values[0:len(sql_values)-1]
                    
                    sql_statements :str = "INSERT INTO " + TABLE_NAME_SYS_ADMIN + "(name,value)\nVALUES" + sql_values 
                    
                    try:
                        with sqlite3.connect(self.database_path) as conn:
                            cursor = conn.cursor()
                            cursor.execute(sql_statements)
                            conn.commit()

                    except sqlite3.OperationalError as e:
                        print("Error on [Create default values on sys_admin table]: ", e, "\n", sql_statements)
            
        except sqlite3.OperationalError as e:
            pass
            
    
    def is_table_exist(self, table_name: str) -> bool:
        """
        Check if table exist on selected database
        """
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM " + table_name)
            return True            
            
        except sqlite3.OperationalError as e:
            return False
        
    def sql_default_admin_system_table(self) -> str:
        
        sql_statements :str = """CREATE TABLE IF NOT EXISTS """ + TABLE_NAME_SYS_ADMIN + """ (
                                        name text NOT NULL, 
                                        value text NOT NULL
                                    );"""
        return sql_statements
    
        
    def sql_default_admin_log_table(self) -> str:
        
        sql_statements :str = """CREATE TABLE IF NOT EXISTS """ + TABLE_NAME_SYS_LOG + """ (
                                        id INTEGER PRIMARY KEY, 
                                        type text NOT NULL, 
                                        description text NOT NULL, 
                                        date DATE
                                    );"""
        return sql_statements
    
    
    def sql_default_user_system_table(self) -> str:
        
        sql_statements :str = """CREATE TABLE IF NOT EXISTS """ + TABLE_NAME_USER_MAIN + """ (
                                        id INTEGER PRIMARY KEY, 
                                        name text NOT NULL, 
                                        salt_pwd text NOT NULL, 
                                        password text NOT NULL, 
                                        first_name text NOT NULL, 
                                        last_name text NOT NULL, 
                                        address text NOT NULL, 
                                        country text NOT NULL, 
                                        email text NOT NULL, 
                                        phone  text NOT NULL,
                                        is_active INTEGER NOT NULL DEFAULT 1,
                                        created_date DATE NOT NULL
                                    );"""
        return sql_statements
    
        
    def sql_default_user_log_table(self) -> str:
        
        sql_statements :str = """CREATE TABLE IF NOT EXISTS """ + TABLE_NAME_USER_LOG + """ (
                                        id INTEGER PRIMARY KEY, 
                                        user_name text NOT NULL, 
                                        user_ip text NOT NULL, 
                                        type text NOT NULL, 
                                        description text NOT NULL, 
                                        date DATE
                                    );"""
        return sql_statements
    
    def sql_default_user_country_table(self) -> str:
        
        sql_statements :str = """CREATE TABLE IF NOT EXISTS """ + TABLE_NAME_USER_COUNTRY + """ (
                                        id text PRIMARY KEY, 
                                        name text NOT NULL
                                    );"""
        return sql_statements
    
    def sql_default_admin_backup_definition_table(self) -> str:
        
        sql_statements :str = """CREATE TABLE IF NOT EXISTS """ + TABLE_NAME_SYS_BACKUP_DEF + """ ( 
                                        backup_id INTEGER NOT NULL,
                                        backup_code text not null,
                                        definition text NOT NULL
                                    );"""
        return sql_statements
    
    def sql_default_admin_proxy_request_table(self) -> str:
        
        sql_statements :str = """CREATE TABLE IF NOT EXISTS """ + TABLE_NAME_SYS_PROXY_REQUEST + """ ( 
                                        id INTEGER PRIMARY KEY, 
                                        name text not null,
                                        HTTP text not null,
                                        HTTPS text not null
                                    );"""
        return sql_statements
    
    def sql_default_admin_redirection_server_table(self) -> str:
        
        sql_statements :str = """CREATE TABLE IF NOT EXISTS """ + TABLE_NAME_SYS_REDIRECTION_SERVER + """ ( 
                                        id INTEGER PRIMARY KEY, 
                                        name text not null,
                                        max_users INTEGER not null,
                                        ip_port text not null
                                    );"""
        return sql_statements
    
    def sql_default_data_set_admin_backup_definition(self):

        import core.tools.DataDefault as df
        
        sql_substatements :str = ""
        
        self.sql_execute_statement("DELETE FROM " + TABLE_NAME_SYS_BACKUP_DEF)
        
        for i in range(len(df.DEFAULT_DATA_SYS_BACKUP_DEF)):
            sql_substatements += "(" + str(df.DEFAULT_DATA_SYS_BACKUP_DEF[i][0]) + ",'" + df.DEFAULT_DATA_SYS_BACKUP_DEF[i][1] + "','" + df.DEFAULT_DATA_SYS_BACKUP_DEF[i][2] + "')"

            if i < len(df.DEFAULT_DATA_SYS_BACKUP_DEF) -1:
                sql_substatements += ","

        sql_statements :str = """INSERT INTO """ + TABLE_NAME_SYS_BACKUP_DEF + """ ( 
                                                   backup_id, backup_code, definition
                                    )VALUES""" + sql_substatements
        
        self.sql_execute_statement(sql_statements)
        
        
    def sql_default_data_set_user_country_definition(self):

        import core.tools.DataDefault as df
        
        sql_substatements :str = ""
        
        self.sql_execute_statement("DELETE FROM " + TABLE_NAME_USER_COUNTRY)
        
        for i in range(len(df.DEFAULT_DATA_USER_COUNTRY_DEF)):
            sql_substatements += "('" + df.DEFAULT_DATA_USER_COUNTRY_DEF[i][0] + "','" + df.DEFAULT_DATA_USER_COUNTRY_DEF[i][1] + "')"

            if i < len(df.DEFAULT_DATA_USER_COUNTRY_DEF) -1:
                sql_substatements += ","

        sql_statements :str = """INSERT INTO """ + TABLE_NAME_USER_COUNTRY + """ ( 
                                                   id, name
                                    )VALUES""" + sql_substatements
        
        self.sql_execute_statement(sql_statements)
        
    def get_default_values_backup_definition(self) -> list:
        
        definition_list :list[str] = []
        
        try:
            with sqlite3.connect(self.database_path) as conn:
                
                cursor = conn.cursor()
                
                cursor.execute("SELECT definition FROM " + TABLE_NAME_SYS_BACKUP_DEF)
                rows = cursor.fetchall()
                
                for row in rows:
                    row = list(row)
                    definition_list.append(row[0])

        except sqlite3.OperationalError as e:
            print("Error on [Read backup definition server system table]: ", e)
            
        return definition_list
    
    
    def get_default_values_country_definition(self) -> list:
        
        definition_list :list[str] = []
        
        try:
            with sqlite3.connect(self.database_path) as conn:
                
                cursor = conn.cursor()
                
                cursor.execute("SELECT name FROM " + TABLE_NAME_USER_COUNTRY)
                rows = cursor.fetchall()
                
                for row in rows:
                    row = list(row)
                    definition_list.append(row[0])

        except sqlite3.OperationalError as e:
            print("Error on [Read country name user system table]: ", e)
            
        return definition_list

    
    def get_user_log_values(self) -> list:
        
        definition_list :list[str] = []
        
        try:
            with sqlite3.connect(self.database_path) as conn:
                
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM " + TABLE_NAME_USER_LOG + " ORDER BY date desc")
                rows = cursor.fetchall()
                
                for row in rows:
                    definition_list.append(list(row))

        except sqlite3.OperationalError as e:
            print("Error on [Read user log system table]: ", e)
            
        return definition_list
    
    def get_server_log_values(self) -> list:
        
        definition_list :list[str] = []
        
        try:
            with sqlite3.connect(self.database_path) as conn:
                
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM " + TABLE_NAME_SYS_LOG + " ORDER BY date desc")
                rows = cursor.fetchall()
                
                for row in rows:
                    definition_list.append(list(row))

        except sqlite3.OperationalError as e:
            print("Error on [Read server log system table]: ", e)
            
        return definition_list
    
    def get_user_list_values(self, active_only :bool = True) -> list:
        
        definition_list :list[str] = []
        
        try:
            with sqlite3.connect(self.database_path) as conn:
                
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM " + TABLE_NAME_USER_MAIN + " where is_active = " + ("1" if active_only else "0"))
                rows = cursor.fetchall()
                
                for row in rows:
                    definition_list.append(list(row))

        except sqlite3.OperationalError as e:
            print("Error on [Read server log system table]: ", e)
            
        return definition_list
    
    def desactive_user(self, user_id :str):

        if len(user_id) > 0:

            sql_statements :str = ""

            sql_statements = "UPDATE " + TABLE_NAME_USER_MAIN + "\n"
            sql_statements += "SET is_active = 0 "
            sql_statements += "WHERE user_main.id = " + user_id

            self.sql_execute_statement(sql_statements)
            
    def get_definition_country_by_code(self, country_code :str) -> str:
        
        return str(self.sql_get_execute_statement("SELECT name FROM " + TABLE_NAME_USER_COUNTRY + " WHERE id='" + country_code + "'")[0][0])    
            
    def get_code_country_by_definition(self, country_definition :str) -> str:
        
        return str(self.sql_get_execute_statement("SELECT id FROM " + TABLE_NAME_USER_COUNTRY + " WHERE name='" + country_definition + "'")[0][0])    
    
    def get_backup_cycle_by_id(self, selected_backup_id :int) -> str:
        
        return str(self.sql_get_execute_statement("SELECT backup_code FROM " + TABLE_NAME_SYS_BACKUP_DEF + " WHERE backup_id=" + str(selected_backup_id))[0][0])
    
    def get_backup_definition_by_id(self, selected_backup_id :int) -> str:
        
        return str(self.sql_get_execute_statement("SELECT definition FROM " + TABLE_NAME_SYS_BACKUP_DEF + " WHERE backup_id=" + str(selected_backup_id))[0][0])
    
    def get_backup_id_by_definition(self, selected_backup_definition :str) -> int:
        
        return int(self.sql_get_execute_statement("SELECT backup_id FROM " + TABLE_NAME_SYS_BACKUP_DEF + " WHERE definition='" + selected_backup_definition + "'")[0][0])
        
    def sql_change_admin_password(self, new_password_hash :str) -> bool:
        
        sql_statements :str = ""
        
        sql_statements = "UPDATE " + TABLE_NAME_SYS_ADMIN + "\n"
        sql_statements += "SET value ='" + new_password_hash + "'" + "\n"
        sql_statements += "WHERE name = 'admin_password'" + "\n"
        
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql_statements)
                conn.commit()

        except sqlite3.OperationalError as e:
            print("Error on [Update admin password on sys_admin table]: ", e, "\n", sql_statements)
            return False
        
        return True
    
    def sql_update_all_system_admin_values(self, admin_server_data :dict) -> bool:
        
        sql_statements :str = ""
        sql_statements_list :list [str] = []
        
        for dict_val in admin_server_data:
            
            sql_statements = "UPDATE " + TABLE_NAME_SYS_ADMIN + "\n"
            sql_statements += "SET value ='" + str(admin_server_data[dict_val]) + "'" + "\n"
            sql_statements += "WHERE name = '" + dict_val + "'" + "\n"
            
            sql_statements_list.append(sql_statements)
        
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                
                for i in range(len(sql_statements_list)):
                    cursor.execute(sql_statements_list[i])
                    
                conn.commit()

        except sqlite3.OperationalError as e:
            print("Error on [Update all value on sys_admin table]: ", e, "\n", sql_statements_list)
            return False
        
        return True
    
    def sql_change_admin_value(self, field_to_update :str, value_to_update :str) -> bool:
        
        sql_statements :str = ""
        
        sql_statements = "UPDATE " + TABLE_NAME_SYS_ADMIN + "\n"
        sql_statements += "SET value ='" + value_to_update + "'" + "\n"
        sql_statements += "WHERE name = '" + field_to_update + "'\n"
        
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql_statements)
                conn.commit()

        except sqlite3.OperationalError as e:
            print("Error on [Update admin value by field on sys_admin table]: ", e, "\n", sql_statements)
            return False
        
        return True
    
    def is_valid_new_user(self, user :cu.User) -> bool:

        if int(self.sql_get_execute_statement("SELECT count(*) FROM " + TABLE_NAME_USER_MAIN + " WHERE is_active=1 and name='" + user.user_name + "'")[0][0]) > 0:
            return False
        
        return True
    
    def is_valid_new_user_by_name(self, user_name :str ) -> bool:

        if int(self.sql_get_execute_statement("SELECT count(*) FROM " + TABLE_NAME_USER_MAIN + " WHERE is_active=1 and name='" + user_name + "'")[0][0]) > 0:
            return False
        
        return True
    
    def is_valid_login_user(self, user :cu.User) -> bool:
        
        user_salt_pwd :str = self.sql_get_execute_statement("SELECT salt_pwd FROM " + TABLE_NAME_USER_MAIN + " WHERE is_active=1 and name='" + user.user_name + "'")[0][0]
        user_password :str = self.sql_get_execute_statement("SELECT password FROM " + TABLE_NAME_USER_MAIN + " WHERE is_active=1 and name='" + user.user_name + "'")[0][0]
        
        if hashlib.sha256(str(user_salt_pwd+user.user_pwd+user_salt_pwd).encode()).hexdigest() == user_password:
            return True
        
        return False
    
    def get_user_data_login(self, user :cu.User):
        
        user_detail_list :list = self.sql_get_execute_statement("SELECT * FROM " + TABLE_NAME_USER_MAIN + " WHERE is_active=1 and name='" + user.user_name + "'")
        
        if user_detail_list != None:
            if len(user_detail_list) > 0:
                if len(user_detail_list[0]) > 1:
                    user.user_id = user_detail_list[0][0]
                    user.user_salt_pwd = user_detail_list[0][2]
                    user.user_pwd = user_detail_list[0][3]
                    user.user_first_name = user_detail_list[0][4]
                    user.user_last_name = user_detail_list[0][5]
                    user.user_address = user_detail_list[0][6]
                    user.user_country = user_detail_list[0][7]
                    user.user_email = user_detail_list[0][8]
                    user.user_phone = user_detail_list[0][9]
            
    def get_user_data_by_id(self, user :cu.User):
        
        user_detail_list :list = self.sql_get_execute_statement("SELECT * FROM " + TABLE_NAME_USER_MAIN + " WHERE is_active=1 and id=" + user.user_id)
        
        if user_detail_list != None:
            if len(user_detail_list) > 0:
                if len(user_detail_list[0]) > 1:
                    user.user_name = user_detail_list[0][1]
                    user.user_salt_pwd = user_detail_list[0][2]
                    user.user_pwd = user_detail_list[0][3]
                    user.user_first_name = user_detail_list[0][4]
                    user.user_last_name = user_detail_list[0][5]
                    user.user_address = user_detail_list[0][6]
                    user.user_country = user_detail_list[0][7]
                    user.user_email = user_detail_list[0][8]
                    user.user_phone = user_detail_list[0][9]

    def get_user_grouped_by_country(self) -> list:

        sql_statements :str = ""

        sql_statements = "SELECT count(*), uc.name\n"
        sql_statements += "FROM user_main um, user_country uc\n"
        sql_statements += "WHERE um.country = uc.id\n"
        sql_statements += "GROUP BY um.country\n"

        return self.sql_get_execute_statement(sql_statements)
    
    def get_new_user_grouped_by_date(self) -> list:

        sql_statements :str = ""

        sql_statements = "SELECT count(*), DATE(created_date)\n"
        sql_statements += "FROM " + TABLE_NAME_USER_MAIN +"\n"
        sql_statements += "GROUP BY DATE(created_date)\n"

        return self.sql_get_execute_statement(sql_statements)
    
    def get_login_user_grouped_by_date(self) -> list:

        sql_statements :str = ""

        sql_statements = "SELECT count(*), DATE(date)\n"
        sql_statements += "FROM " + TABLE_NAME_USER_LOG +"\n"
        sql_statements += "WHERE type = 'LOGIN'\n"
        sql_statements += "GROUP BY DATE(date)\n"

        return self.sql_get_execute_statement(sql_statements)
    
    def get_new_salt_pwd(salt) -> str:
        
        Random_lenght :int = 16
        new_salt_value :str = ""
        
        valid_List_char :str = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        len_list_char :int = len(valid_List_char)- 1
        
        for _ in range(Random_lenght):
            new_salt_value += valid_List_char[random.randint(0, len_list_char)]
            
        return new_salt_value
        
    
    def add_new_user(self, user :cu.User):
        
        new_salt_pwd :str = self.get_new_salt_pwd()
        new_pwd :str = new_salt_pwd+user.user_pwd+new_salt_pwd
        
        sql_substatements = "('" + user.user_name +  "','" 
        sql_substatements +=  new_salt_pwd +  "','" 
        sql_substatements +=  hashlib.sha256(new_pwd.encode()).hexdigest() +  "','" 
        sql_substatements +=  user.user_first_name +  "','" 
        sql_substatements +=  user.user_last_name +  "','" 
        sql_substatements +=  user.user_address +  "','" 
        sql_substatements +=  user.user_country +  "','" 
        sql_substatements +=  user.user_email +  "','" 
        sql_substatements +=  user.user_phone +  "','" 
        sql_substatements +=  str(datetime.datetime.now()) + "')"
        
        sql_statements :str = """INSERT INTO """ + TABLE_NAME_USER_MAIN + """ ( 
                                                    name, salt_pwd, password, first_name, last_name, 
                                                    address, country, email, phone, created_date
                                        )VALUES""" + sql_substatements
                                        
        try:

            self.sql_execute_statement(sql_statements)                                    
            
        except:
            pass                            
        
    def reset_user_password(self, user_id: str, reset_pwd :str):
        
        sql_statements :str = ""
        
        reset_pwd = hashlib.sha256(reset_pwd.encode()).hexdigest() 
        user_salt_pwd :str = self.get_salt_pwd_by_user_id(user_id)
        
        new_pwd :str = user_salt_pwd+reset_pwd+user_salt_pwd

        sql_statements = "UPDATE " + TABLE_NAME_USER_MAIN + "\n"
        sql_statements += "SET password = '" + hashlib.sha256(new_pwd.encode()).hexdigest() + "'\n" 
        sql_statements += "WHERE user_main.id = " + str(user_id)
        
        try:

            self.sql_execute_statement(sql_statements)                                    
            
        except:
            pass          
        
    def get_salt_pwd_by_user_id(self, user_id :str) -> str:
        
        try:
            with sqlite3.connect(self.database_path) as conn:
                
                cursor = conn.cursor()
                
                cursor.execute("SELECT salt_pwd FROM user_main WHERE id = " + str(user_id))
                rows = cursor.fetchall()
                
                for row in rows:
                    return str(row[0])

        except sqlite3.OperationalError as e:
            print("Error on [Read salt pwd definition on user table]: ", e)
            
        return ""
        
    def update_user(self, user :cu.User):
        
        sql_statements :str = ""
        
        sql_statements = "UPDATE " + TABLE_NAME_USER_MAIN + "\n"
        sql_statements += "SET first_name = '" + user.user_first_name + "',"
        sql_statements +=    " last_name = '" + user.user_last_name + "',"
        sql_statements +=    " address = '" + user.user_address + "',"
        sql_statements +=    " country = '" + user.user_country + "',"
        sql_statements +=    " email = '" + user.user_email + "',"
        sql_statements +=    " phone = '" + user.user_phone + "' " + "\n"
        sql_statements += "WHERE user_main.id = " + user.user_id

        try:

            self.sql_execute_statement(sql_statements)                                    
            
        except:
            pass          
        
    def set_user_log(self, user :cu.User, log_type :str, log_description :str):
        
        sql_substatements = "('" + user.user_name +  "','" 
        sql_substatements +=  user.user_ip +  "','" 
        sql_substatements +=  log_type +  "','" 
        sql_substatements +=  log_description +  "','" 
        sql_substatements +=  str(datetime.datetime.now()) + "')"
        
        sql_statements :str = """INSERT INTO """ + TABLE_NAME_USER_LOG + """ ( 
                                                    user_name, user_ip, type, description, date
                                        )VALUES""" + sql_substatements
        try:

            self.sql_execute_statement(sql_statements)                                    
            
        except:
            pass                                                                    
        
    def set_system_log(self, log_type :str, log_description :str):
        
        sql_substatements = "('" + log_type +  "','" 
        sql_substatements +=  log_description +  "','" 
        sql_substatements +=  str(datetime.datetime.now()) + "')"
        
        sql_statements :str = """INSERT INTO """ + TABLE_NAME_SYS_LOG + """ ( 
                                                    type, description, date
                                        )VALUES""" + sql_substatements
        try:

            self.sql_execute_statement(sql_statements)                                    
            
        except:
            pass                                                                    
        