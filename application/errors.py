messages = {
    "username_invalid": "The username must be 3-16 characters long and it can only contain characters a-z, A-Z, and 0-9",
    "username_taken": "An account with given username already exits.",
    "login_incorrect": "Incorrect username or password.",
    "signup_db_error": "Account creation failed for an unknown reason, please contact @Valokoodari",
    "display_name_invalid": "The display name must be 3-48 characters long and can only contain characters a-z, A-Z, 0-9, and spaces.",
    "sudoku_name_invalid": "The sudoku name must be 3-48 characters long and can only contain characters a-z, A-Z, 0-9, spaces, and hyphens (-).",
    "sudoku_id_not_found": "A sudoku with the given id doesn't exist.",
    "sudoku_no_permission": "You don't have the permissions to view that sudoku.",
    "sudoku_db_error": "The sudoku couldn't be saved for an unknown reason, please contact @Valokoodari.",
    "password_confirmation": "The password and the password confirmation do not match.",
    "password_invalid": "The password must be at least 8 characters long and it must contain at least one number 0-9 and at least one letter a-z or A-Z.",
    "comment_no_user": "You must be logged in to comment.",
    "create_no_user": "You must be logged in to create sudokus!"
}

def get_msg(error_name):
    if error_name == None:
        return None
    if error_name in messages:
        return messages[error_name]
    return "Unknown error code: " + error_name