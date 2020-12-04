import re
import db

def check_username(username):
    return re.match("^[0-9a-zA-Z]{3,16}$", username)

def check_display_name(display_name):
    return re.match("^[0-9a-zA-Z ]{3,48}$", display_name)

def check_password(password):
    if 8 > len(password): return False
    return re.match("^.*([0-9][a-zA-Z]|[a-zA-Z][0-9]).*$", password)

def check_sudoku_name(sudoku_name):
    return re.match("^[0-9a-zA-Z -]{3,48}$", sudoku_name)

def check_signup(display_name, username, password, password_confirm):
    if not check_display_name(display_name): return "display_name_invalid"
    if not check_username(username): return "username_invalid"
    if db.is_username_taken(username): return "username_taken"
    if not check_password(password): return "password_invalid"
    if password != password_confirm: return "password_confirmation"
    return None