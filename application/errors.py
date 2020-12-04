messages = {
    "username_invalid": "The username must be 3-16 characters long and it can only contain characters a-z, A-Z, and 0-9",
    "username_taken": "An account with given username already exits.",
    "password_short": "The password must be at least 8 characters long.",
    "login_incorrect": "Incorrect username or password.",
    "display_name_invalid": "The display name must be 3-48 characters long and can only contain characters a-z, A-Z, 0-9, and spaces.",
    "sudoku_name_invalid": "The sudoku name must be 3-48 characters long and can only contain characters a-z, A-Z, 0-9, and spaces.",
    "password_confirmation": "The password and the password confirmation do not match."
}

def get_msg(error):
    return messages[error]