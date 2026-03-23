from enum import Enum

class field_type(Enum):
    
    TEXT = 1
    NUM = 2
    DATE = 3
    
class DataField:
    
    def __init__(self, field_name :str ):
        
        self.name :str = field_name
        self.values :list = []
        
    def add_value(self, value :str = "", type :field_type = field_type.TEXT):
      
        value :DataValue = DataValue(value, type)  
        self.values.append(value)
        
class DataValue:
    
    def __init__(self, value :str, type :field_type):
        
        self.value :str = value
        self.type :field_type = type 
    
class DataTable:
    
    def __init__(self, table_name :str, signature :str = ""):
        
        self.name = table_name
        self.fields :list = []
        self.signature :str = signature
        self.rows :list = []
        
    def add_field(self, field_name :str):
        
        if not self.is_field_exist(field_name):
            field :DataField = DataField(field_name)
            self.fields.append(field)
        
    def is_field_exist(self, field_name :str) -> bool:
        
        for i in range(len(self.fields)):
            if self.fields[i].name == field_name:
                return True
                
        return False
        
    def remove_field(self, field_name :str):
        
        for i in range(len(self.fields)):
            if self.fields[i].name == field_name:
                self.fields.pop(i)
                break
            
    def get_field(self, field_name :str) -> DataField:
        
        if not self.is_field_exist(field_name):
            self.add_field(field_name)
        
        for i in range(len(self.fields)):
            if self.fields[i].name == field_name:
                return self.fields[i]
        
class DataBase:
    
    def __init__(self):
        
        self.tables :list = []
        
    def append(self, data_base_ref :any, id :str = ""):
        
        data_base :DataBase = data_base_ref
        
        for i in range(len(data_base.tables)):            
            if id != "": 
                data_base.tables[i].name = str(id) + "_" + data_base.tables[i].name
                
            self.tables.append(data_base.tables[i])
        
    def create_rows_matrix(self):
        
        for table in self.tables:
            
            table.rows = []
            
            count_field :int = len(table.fields)
            count_row :int = len(table.fields[0].values)
            
            for k in range(count_row):
                row :list = []     
                for l in range(count_field):
                    try:
                        row.append(str(table.fields[l].values[k].value))
                    except:
                        row.append("")
                    
                table.rows.append(row)    
        
    def get_table(self, table_name :str) -> DataTable:
        
        for i in range(len(self.tables)):
            if self.tables[i].name == table_name:
                return self.tables[i]
                
        return None
    
    def get_count_table_by_index(self, index :int) -> int:
        
        return self.get_count_by_table(self.get_table(str(self.tables[index].name)))
    
    def get_count_table_by_name(self, table_name :str) -> int:
        
        return self.get_count_by_table(self.get_table(table_name))
    
    def get_count_by_table(self, table :DataTable) -> int:
        
        field :DataField = None
        
        for field_list in table.fields:
            field = field_list
            return len(field.values)
                
        return 0
        
    def get_field(self, table_name :str, field_name :str) -> DataField:
        
        for i in range(len(self.tables)):
            if self.tables[i].name == table_name:
                self.tables[i].add_field(field_name)
                for j in range(len(self.tables[i]).fields):
                    if self.tables[i].fields[j].name == field_name:
                        return self.tables[i].fields[j]
        
        return None
    
    def add_table(self, table_name :str, signature :str):
        
        if self.table_signature_exist(signature) == "":
            table :DataTable = DataTable(table_name, signature)
            self.tables.append(table)
        
    def remove_table(self, table_name :str):
        
        for i in range(len(self.tables)):
            if self.tables[i].name == table_name:
                self.tables.pop(i)
                break
        
    def add_field(self, table_name :str, field_name :str):
        
        for i in range(len(self.tables)):
            if self.tables[i].name == table_name:
                self.tables[i].add_field(field_name)
                break
                
    def remove_field(self, table_name :str, field_name :str):
        
        for i in range(len(self.tables)):
            if self.tables[i].name == table_name:
                self.tables[i].add_field(field_name)
                for j in range(len(self.tables[i].fields)):
                    if self.tables[i].fields[j].name == field_name:
                        self.tables[i].fields.pop(j)
                        break
                
    def add_field_value(self, table_name :str, field_name :str, field_value :str, field_type :field_type = field_type.TEXT):
        
        field :DataField = self.get_field(table_name, field_name)
        field.add_value(field_value, field_type.TEXT)
        
    def table_exist(self, table_name :str) -> bool:
        
        if self.get_table(table_name) == table_name:
            return True
        
        return False
    
    def table_signature_exist(self, signature :str) -> str:
        
        for i in range(len(self.tables)):
            if self.tables[i].signature == signature:
                return self.tables[i].name
        
        return ""
        
