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
    sql = "SELECT name,cells,instructions FROM sudokus WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    sudoku = result.fetchone();

    # Redirect to the error page if the sudoku doesn't exist
    if sudoku == None:
        return render_template("error.html", error="A sudoku with the given id doesn't exits.")

    return render_template("sudoku.html", name=sudoku[0], cells=sudoku[1], rules=sudoku[2])
    # TODO - Check permissions

@app.route("/create")
def create():
    # The user must be logged in to create a sudoku
    if "user_id" not in session:
        return render_template("error.html", error="You must be logged in!");

    return render_template("create.html")

@app.route("/new", methods=["POST"])
def new():
    # The user must be logged in to submit a new sudoku
    if "user_id" not in session:
        return render_template("error.html", error="You must be logged in!");

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

    return redirect("/sudoku/" + str(result.fetchone()[0]))
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
