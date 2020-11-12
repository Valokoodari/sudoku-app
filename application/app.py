from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sudoku/<int:id>")
def sudoku(id):
    result = db.session.execute("SELECT cells FROM sudokus")
    cells = result.fetchall()[id][0]
    return render_template("sudoku.html", numbers=cells)
    # TODO - 404 if sudoku with given id doesn't exist

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/new", methods=["POST"])
def new():
    if "user_id" not in session:
        print("User id not found!")
        # TODO - Not logged in ERROR

    name = request.form["name"]
    cells = [];
    for row in range(0, 9):
        cells.append([]);
        for col in range(0, 9):
            cells[row].append(request.form["cell"+str(row)+str(col)])
    instructions = request.form["instructions"]
    if ("public" in request.form):
        display = 3
    else:
        display = 1

    sql = "INSERT INTO sudokus (owner_id, name, cells, instructions, display) VALUES (:user_id, :name, :cells, :instructions, :display)"
    db.session.execute(sql, {"user_id":session["user_id"], "name":name, "cells":cells, "instructions":instructions, "display":display})
    db.session.commit()

    result = db.session.execute("SELECT COUNT(*) FROM sudokus")

    return redirect("/sudoku/" + str(result.fetchone()[0]-1))
    # TODO - error handling

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT id, password_hash, display_name FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if (user == None):
        print("Invalid Username!")
        # TODO - invalid username
    else:
        password_hash = user[1]
        if check_password_hash(password_hash, password):
            session["user_id"] = user[0]
            session["display_name"] = user[2]
        else:
            print("Invalid Password!")
            # TODO - invalid password

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

    if (password != confirm):
        print("TODO");
        # TODO - Passwords do not match
    else:
        sql = "INSERT INTO users (username, password_hash, display_name, permission_level) VALUES (:username,:password_hash,:display_name,0)"
        db.session.execute(sql, {"username":username, "password_hash":password_hash, "display_name":display})
        db.session.commit()

        sql = "SELECT id, display_name FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone();
        print(user);
        
        session["user_id"] = user[0];
        session["display_name"] = user[1];
        
    return redirect("/")
