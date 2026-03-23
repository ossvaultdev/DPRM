import core.tools.DataBase as db

KEY_LINK_FIELD_ID_NAME :str= "KEY_LINK_ID"
KEY_TABLE_LIST_ID_NAME :str = "TABLE_LIST_"
KEY_FIELD_LIST_ID_NAME :str = "FIELD_LIST_"

KEY_BASE_TABLE_NAME :str = "MAIN"
KEY_SIGNATURE_BASE_NAME  :str = "field_"


class DataTransform:
    
    def __init__(self ):
        
        self.counter_link_id :int = 0
        self.counter_table_list_name_id :int = 0
    
    def get_database_from_json(self, data_json_dict :dict) -> db.DataBase:
        
        data_base :db.DataBase = db.DataBase()
        
        self.create_table_from_json_dict(KEY_BASE_TABLE_NAME, KEY_BASE_TABLE_NAME, data_base, data_json_dict)
        
        self.clean_database(data_base)
        data_base.create_rows_matrix()
        
        return data_base
    
    def clean_database(self, data_base :db.DataBase):
        
        count_table :int = len(data_base.tables)
        
        for i in range(count_table):
            if data_base.get_count_table_by_index(count_table - i - 1) < 2:
                del data_base.tables[count_table - i - 1]
                
        count_table = len(data_base.tables)
        
        for i in range(count_table):
            if len(data_base.tables[count_table - i - 1].fields) == 0:
                del data_base.tables[count_table - i - 1]
                
    def get_signature_keys_field(self, key_dict :dict.keys) ->str:
        
        signature :str = ""
        
        for key in key_dict:
            signature += "'" + str(key) + "'."
        
        if len(signature) > 0:
            signature = signature[:-1]
        
        return signature
    
    def get_signature_list(self, list_data :list) ->str:
                
        signature :str = ""
        
        for i in range(len(list_data)):
            signature += KEY_SIGNATURE_BASE_NAME + str(i) + "',"
        
        if len(signature) > 0:
            signature = signature[:-1]
        
        return signature
    
    def create_table_from_json_dict(self, key_field_link_id :str = KEY_BASE_TABLE_NAME, table_name :str = KEY_BASE_TABLE_NAME, 
                                          data_base :db.DataBase = None , dict_to_list :dict = None):
    
        table : db.DataTable = None
        key_dict :dict.keys = None
        
        self.counter_link_id += 1 
        key_dict = dict_to_list.keys()
        
        if not data_base.table_exist(table_name):
            signature :str = self.get_signature_keys_field(key_dict)
            data_base.add_table(table_name, signature)
            
        table = data_base.get_table(table_name)
        
        for key in key_dict:
            
            table.add_field(key)
            key_lind_id :str = key + "_" + str(self.counter_link_id)
            
            if type(dict_to_list[key]) == dict:
                
                signature :str  = self.get_signature_keys_field(dict(dict_to_list[key]).keys())
                new_table_name :str = data_base.table_signature_exist(signature)
                
                if new_table_name == "":
                    new_table_name = key
                    data_base.add_table(new_table_name, signature)
                               
                table.get_field(key).add_value(key_lind_id)
                self.create_table_from_json_dict(key_lind_id, new_table_name, data_base, dict(dict_to_list[key]))
                
            elif type(dict_to_list[key]) == list:
                
                table.get_field(key).add_value(key_lind_id)
                self.create_table_from_list(key_lind_id , list(dict_to_list[key]), data_base)
                      
            else:
                
                table.get_field(key).add_value(str(dict_to_list[key]))
        
        table.add_field(KEY_LINK_FIELD_ID_NAME)
        table.get_field(KEY_LINK_FIELD_ID_NAME).add_value(key_field_link_id)    
                
    def create_table_from_list(self, key_lind_id :str, list_data :list, data_base :db.DataBase = None):
        
        signature :str  = self.get_signature_list(list_data)
        table_name :str = data_base.table_signature_exist(signature)
        
        if table_name == "":
            self.counter_table_list_name_id += 1 
            table_name = KEY_TABLE_LIST_ID_NAME + str(self.counter_table_list_name_id)
            data_base.add_table(table_name, signature)
            
        table = data_base.get_table(table_name)
        
        for i in range(len(list_data)):

            field_key_name :str = KEY_FIELD_LIST_ID_NAME + str(i)
            table.add_field(field_key_name)
                    
            if type(list_data[i]) == dict:
                
                signature :str  = self.get_signature_keys_field(dict(list_data[i]).keys())
                new_table_name :str = data_base.table_signature_exist(signature)
                
                if new_table_name == "":
                    new_table_name = field_key_name
                    data_base.add_table(new_table_name, signature)
                    
                key_lind_id :str = field_key_name + "_" + str(self.counter_link_id)
                table.get_field(field_key_name).add_value(key_lind_id)
                
                self.create_table_from_json_dict(key_lind_id, new_table_name, data_base, dict(list_data[i]))                
            
            elif type(list_data[i]) == list:
                
                self.create_table_from_list(key_lind_id , list(list_data[i]), data_base)
            
            else:
        
                table.get_field(field_key_name).add_value(str(list_data[i]))
          
        table.add_field(KEY_LINK_FIELD_ID_NAME)
        table.get_field(KEY_LINK_FIELD_ID_NAME).add_value(key_lind_id)      
        
                