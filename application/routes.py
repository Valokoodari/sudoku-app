from app import app
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

import db

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sudoku/<int:id>")
def sudoku(id):
    sudoku = db.get_sudoku(id);

    # Redirect to the error page if the sudoku doesn't exist
    if sudoku == None:
        return render_template("error.html", \
               error="A sudoku with the given id doesn't exits.")
    
    # Check the permissions
    display = sudoku[3]
    owner_id = sudoku[4]
    shared_to = sudoku[5]
    if (shared_to == None):
        shared_to = []

    if display == 3 or display == 2: # Public sudoku, display to anyone
        return render_template("sudoku.html", name=sudoku[0], \
               cells=sudoku[1], rules=sudoku[2])
    elif display == 1 and "user_id" in session:
        user_id = session["user_id"]
        if user_id == owner_id or user_id in shared_to:
            return render_template("sudoku.html", name=sudoku[0], \
                   cells=sudoku[1], rules=sudoku[2])

    # The user doesn't have the permission to view the sudoku
    return render_template("error.html", \
           error="You don't have the permissions to view that sudoku!")

@app.route("/sudokus")
def sudokus():
    sudokus = db.get_sudokus();

    print(sudokus)

    return render_template("error.html", error="WIP");

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
        display = 3 # public
    else:
        display = 1 # private
    # 0 "deleted", 2 anyone with the link

    id = db.add_sudoku(session["user_id"], name, cells, instructions, display)

    if (id < 0):
        return render_template("error.html", error="Sudoku could not be saved.")

    return redirect("/sudoku/" + str(id))
    # TODO - error handling

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = db.get_user(username);

    if (user == None):
        return render_template("error.html", \
               error="Invalid username or password!")
    else:
        password_hash = user[1]
        if check_password_hash(password_hash, password):
            session["user_id"] = user[0]
            session["display_name"] = user[2]
        else:
            return render_template("error.html", \
                   error="Invalid username or password!")

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

    # Check if the passwords do not match
    if (password != confirm):
        return render_template("error.html", error="The passwords do not match!")

    # Check if the username is already taken
    user = db.get_user(username)
    if (user != None):
        return render_template("error.html", \
               error="An account with given username already exits.")

    # Create the new account
    db.create_user(username, password_hash, display)

    user = db.get_user(username)

    session["user_id"] = user[0]
    session["display_name"] = user[2]
        
    return redirect("/")
