
function HomeSubmit() 
{             
    document.getElementById("KEY_ID").value = "";          
    document.getElementById("KEY_VALUE").value = "";          
    document.getElementById("UserSelection").submit();
}

function RegisterSubmit() 
{   
    let user_name = document.getElementById("USR_NAME").value
    let user_pwd1 = document.getElementById("USR_PWD_1").value
    let user_pwd2 = document.getElementById("USR_PWD_2").value

    let user_first_name = document.getElementById("USR_FIRST_NAME").value
    let user_last_name = document.getElementById("USR_LAST_NAME").value

    let user_address = document.getElementById("USR_ADDRESS").value
    let user_country = document.getElementById("USR_COUNTRY").value
    let user_email = document.getElementById("USR_EMAIL").value
    let user_phone = document.getElementById("USR_PHONE").value

    let user_error_default = 'ERROR IN REGISTRATION: \nUser '
    
    if (user_name.length == 0)
    {
        return WindowsMessage(user_error_default + "Name is not filled!");
    }

    if (user_pwd1.length == 0)
    {
        return WindowsMessage(user_error_default + "Password is not filled!");
    }

    if (user_pwd1.length < 8)
    { 
        return WindowsMessage(user_error_default + "Password has to be at least 8 characters long!");
    }

    let valid_pwd_char = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ?!&%ç*"+-/_-'

    if (!is_valid_string(user_pwd1, valid_pwd_char))
    {
        return WindowsMessage(user_error_default + 'password is not valid format!\n\n' + 'Character value allowed only: [' + valid_pwd_char + ']')
    }
    
    if (user_pwd1 != user_pwd2)
    {
        return WindowsMessage(user_error_default + "Password and Re-Type Password are not the same!");
    }

    if (user_first_name.length == 0)
    {
        return WindowsMessage(user_error_default + "First Name is not filled!");
    }

    if (user_last_name.length == 0)
    {
        return WindowsMessage(user_error_default + "Last Name is not filled!");
    }

    if (user_address.length == 0)
    {
        return WindowsMessage(user_error_default + "Address is not filled!");
    }

    if (user_country.length == 0)
    {
        return WindowsMessage(user_error_default + "Country is not filled!");
    }

    if (user_country == "Country Selection")
    {
        return WindowsMessage(user_error_default + "Country is not filled!");
    }

    if (user_email.length == 0)
    {
        return WindowsMessage(user_error_default + "EMail is not filled!");
    }

    if (user_phone.length == 0)
    {
        return WindowsMessage(user_error_default + "Phone is not filled!");
    }

    let valid_email_char = '.0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    let user_email_split = user_email.split('@')
    let has_valid_email = false

    if (user_email_split.length == 2)
    {
        if ((is_valid_string(user_email_split[0], valid_email_char)) && (is_valid_string(user_email_split[1], valid_email_char)))
        {
            has_valid_email = true
        }
    }

    if(!has_valid_email)
    {
        return WindowsMessage(user_error_default + 'email has not valid format!\n\n' + 'Character value allowed only: [1*[@]+' + valid_email_char + ']')
    }
    
    let valid_phone_number_char = '0123456789+.-()'
    
    if (!is_valid_string(user_phone, valid_phone_number_char))
    {
        return WindowsMessage(user_error_default + 'phone has not valid format!\n\n' + 'Character value allowed only: [' + valid_phone_number_char + ']')
    }

    let valid_address_char = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 :.-,()'

    if (!is_valid_string(user_address, valid_address_char))
    {
        return WindowsMessage(user_error_default + 'address has not valid format!\n\n' + 'Character value allowed only: [' + valid_address_char + ']')
    }
    
    let user_data_sign_in_value = ""
    
    user_data_sign_in_value = 'user_name=' + replace_value_by_tag(user_name) + ":";
    user_data_sign_in_value += 'user_pwd=' + Sha256.hash(user_pwd1) + ":";
    user_data_sign_in_value += 'user_first_name=' + replace_value_by_tag(user_first_name) + ":";
    user_data_sign_in_value += 'user_last_name=' + replace_value_by_tag(user_last_name) + ":";
    user_data_sign_in_value += 'user_address=' + replace_value_by_tag(user_address) + ":";
    user_data_sign_in_value += 'user_country=' + replace_value_by_tag(user_country) + ":";
    user_data_sign_in_value += 'user_email=' + replace_value_by_tag(user_email) + ":";
    user_data_sign_in_value += 'user_phone=' + replace_value_by_tag(user_phone);

    document.getElementById("KEY_VALUE").value = document.getElementById("KEY_REQUEST_SIGNIN_SUBMIT").value + ':' + user_data_sign_in_value;          
    document.getElementById("UserSelection").submit(); 

    
}

