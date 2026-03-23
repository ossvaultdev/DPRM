import random

class UserTools:
    
    def __init__(self ):
        
        self.user_key_id_list :list = []
    
    def reset_user_key_id_list(self):
        
        self.user_key_id_list.clear()
        
    def is_user_key_id_valid(self, user_key_id :str) -> bool:
        
        for i in range(len(self.user_key_id_list)):
            
            if user_key_id == self.user_key_id_list[i]:
                
                if not "." in user_key_id:
                    self.user_key_id_list.pop(i)
                    
                return True
            
        return False
    
    def get_special_user_key_id(self, special_key :str) -> str:
        
        self.remove_all_special_user_key_id(special_key)
        
        header_key_id :str = self.get_user_key_id()
        
        for i in range(len(self.user_key_id_list)):
            if self.user_key_id_list[i] == header_key_id:
                self.user_key_id_list.pop(i)
                header_key_id += "." + special_key
                self.user_key_id_list.append(header_key_id)
                
        return header_key_id
    
    def remove_all_special_user_key_id(self, special_key :str):
        
        for i in range(len(self.user_key_id_list)):
            if str(self.user_key_id_list[i])[-2::] == "." + special_key:                
                self.user_key_id_list.pop(i)
                return 
        
        
    def get_user_key_id(self) -> str:
        
        """ 
            Create a new keyID only private access frame user 
        """
        
        Random_lenght :int = 0
        new_key_id_value :str = ""
        
        
        valid_List_char :str = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        len_list_char :int = len(valid_List_char) - 1
        
        new_key_id_value = ""
        Random_lenght = random.randint(25, 50)
        
        for _ in range(Random_lenght):
            new_key_id_value += valid_List_char[random.randint(0, len_list_char)]
            
        self.user_key_id_list.append(new_key_id_value)
        
        return new_key_id_value
    
    def replace_tag_format(self, value_to_format :str) -> str:
        
        value_to_format = value_to_format.replace('<tag_two_point_h>', ':')
        value_to_format = value_to_format.replace('<tag_equal_value>', '=')
        
        return value_to_format
    
    def is_valid_string(self, value_to_check :str, valid_value :str) -> bool:
        
        has_Value :bool = False
        
        for i in range(len(value_to_check)):
            has_Value = False
            for j in range(len(valid_value)):
                if(value_to_check[i] == valid_value[j]):
                    has_Value = True
                    
            if not has_Value:
                return False 
         
        return True
    
    def is_valid_email(self, check_email :str) -> bool:
        
        valid_email_char :str = '.0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        user_email_split = check_email.split('@')
        
        if len(user_email_split) == 2:
            
            if ((self.is_valid_string(user_email_split[0], valid_email_char)) and (self.is_valid_string(user_email_split[1], valid_email_char))):
                return True
            
        return False
    
    def is_valid_address(self, check_address :str) -> bool:
        
        valid_address_char :str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 :.-,()'
        
        if self.is_valid_string(check_address, valid_address_char):
            return True
        
        return False                
    
    def is_valid_phone(self, check_phone :str) -> bool:
        
        valid_phone_number_char :str = '0123456789+.-()'
        
        if self.is_valid_string(check_phone, valid_phone_number_char):
            return True
        
        return False      
    

    def check_new_password(self, frame_value_list :list, user_login_pwd :str) -> str:
        
        if len(frame_value_list) != 5:
            return "Password data Corrupted!"
        
        if str(frame_value_list[2]).split("=")[1] != user_login_pwd:
            return "Password is no correct!"
        
        # Test len SHA256 : User Password ...
        if len(str(frame_value_list[3]).split("=")[1]) !=len("15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225"):
            return "New Password is data missing!"
        
        if str(frame_value_list[3]).split("=")[1] != str(frame_value_list[4]).split("=")[1]:
            return "New Password and retype password are not the same!"

        return ""
    
    def is_valid_workspace_name(self, new_workspace_name :str) -> str:
        
        valid_workspace_char :str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890_-'
        
        if len(new_workspace_name) < 4:
            return "Error: New Workspace Name length has to be at least 4 characters long!"
        
        if len(new_workspace_name) > 15:
            return "Error: New Workspace Name length has to be at maximum of 15 characters long!"
        
        if not self.is_valid_string(new_workspace_name, valid_workspace_char):
            return 'Error: New Workspace Name has not valid format!\n\n' + 'Character value allowed only: [' + valid_workspace_char + ']'
        
        
        return ""