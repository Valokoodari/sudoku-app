from app import app
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

import re
import db
import errors
import validation as iv

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sudoku/<int:id>")
def sudoku(id):
    sudoku = db.get_sudoku(id)

    if sudoku == None: return render_template("sudokus.html", error=errors.get_msg("sudoku_id_not_found"))
    
    # Check the permissions
    display = sudoku[3]
    owner_id = sudoku[4]
    shared_to = db.get_sudoku_shares(id)
    if (shared_to == None):
        shared_to = []

    if display == "public" or display == "link":
        return render_template("sudoku.html", name=sudoku[0], \
               cells=sudoku[1], rules=sudoku[2])
    elif display == "private" and "user_id" in session:
        user_id = session["user_id"]
        if user_id == owner_id or user_id in shared_to:
            return render_template("sudoku.html", name=sudoku[0], \
                   cells=sudoku[1], rules=sudoku[2])

    # The user doesn't have the permission to view the sudoku
    return render_template("sudokus.html", \
           error="You don't have the permissions to view that sudoku!")

@app.route("/sudokus")
def sudokus():
    sudokus = db.get_public_sudokus();

    user_sudokus = None
    if "user_id" in session:
        user_sudokus = db.get_user_sudokus(session["user_id"]);

    return render_template("sudokus.html", sudokus=sudokus, user_sudokus=user_sudokus);

@app.route("/new", methods=["GET", "POST"])
def new():
    # The user must be logged in to submit a new sudoku
    if "user_id" not in session:
        return render_template("index.html", error="You must be logged in!");
    
    if request.method == "GET":
        return render_template("create.html")

    name = request.form["name"]
    cells = [];
    for row in range(0, 9):
        cells.append([]);
        for col in range(0, 9):
            cells[row].append(request.form["cell"+str(row)+str(col)])
    instructions = request.form["instructions"]
    display = request.form["display"]

    id = db.add_sudoku(session["user_id"], name, cells, instructions, display)

    if (id < 0):
        return render_template("create.html", error="Sudoku could not be saved.")

    return redirect("/sudoku/" + str(id))
    # TODO - error handling

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = db.get_user(username);

    if (user == None):
        return render_template("index.html", \
               error=errors.get_msg("login_incorrect"))
    else:
        password_hash = user[1]
        if check_password_hash(password_hash, password):
            session["user_id"] = user[0]
            session["display_name"] = user[2]
        else:
            return render_template("index.html", \
                   error=errors.get_msg("login_incorrect"))

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

    error = iv.check_signup(display, username, password, confirm)
    if error: return render_template("index.html", error=error)

    db.create_user(username, password_hash, display)

    user = db.get_user(username)

    session["user_id"] = user[0]
    session["display_name"] = user[2]
        
    return redirect("/")
