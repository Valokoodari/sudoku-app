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
            session["user_id"] = user[0]
            session["display_name"] = user[2]
            session["csrf_token"] = os.urandom(16).hex()
        else:
            return redirect("/?err=login_incorrect")

    return redirect("/")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["display_name"]
    return redirect("/")

@app.route("/signup", methods=["POST"])
def signup():
    display = request.form["display"]
    username = request.form["username"]
    password = request.form["password"]
    confirm = request.form["confirm"]
    password_hash = generate_password_hash(password)

    error = check_signup(display, username, password, confirm)
    if error: return render_template("index.html", error=get_msg(error))

    user = create_user(username, password_hash, display)

    if user:
        session["user_id"] = user[0]
        session["display_name"] = user[2]
        return redirect("/")
    else:
        return redirect("/?err=signup_db_error")