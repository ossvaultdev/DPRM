function Logindev()
{
    document.getElementById("USR_NAME").value = "NOMADES"
    document.getElementById("USR_PWD_1").value = "..."

    LoginSubmit()

}
function HomeSubmit() 
{             
    document.getElementById("KEY_ID").value = "";          
    document.getElementById("KEY_VALUE").value = "";          
    document.getElementById("UserSelection").submit();
}

function LoginSubmit() 
{          
    let user_name = document.getElementById("USR_NAME").value
    let user_pwd1 = document.getElementById("USR_PWD_1").value

    let user_error_default = 'ERROR IN LOGIN: \nUser '

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

    let user_data_sign_in_value = ""

    user_data_sign_in_value = replace_value_by_tag(user_name) + ":";
    user_data_sign_in_value += Sha256.hash(user_pwd1);

    document.getElementById("KEY_VALUE").value = document.getElementById("KEY_REQUEST_LOGIN_SUBMIT").value + ':' + user_data_sign_in_value;          
    document.getElementById("UserSelection").submit();
}