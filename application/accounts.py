import os
from app import app
from errors import get_msg
from validation import check_signup
from db import create_user, get_user
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = get_user(username);

    if (user == None):
        redirect("/?err=login_incorrect")
    else:
        password_hash = user[1]
        if check_password_hash(password_hash, password):
            set_session_details(user)
        else:
            return redirect("/?err=login_incorrect")

    return redirect("/")

@app.route("/logout")
def logout():
    clear_session_details()
    return redirect("/")

@app.route("/signup", methods=["POST"])
def signup():
    display = request.form["display"]
    username = request.form["username"]
    password = request.form["password"]
    confirm = request.form["confirm"]
    password_hash = generate_password_hash(password)

    error = check_signup(display, username, password, confirm)
    if error: return redirect("index.html?err=" + error)

    user = create_user(username, password_hash, display)

    if user:
        set_session_details(user)
        return redirect("/")
    else:
        return redirect("/?err=signup_db_error")

def set_session_details(user):
    session["user_id"] = user[0]
    session["display_name"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()

def clear_session_details():
    del session["user_id"]
    del session["display_name"]
    del session["csfr_token"]