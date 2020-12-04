from app import app
from errors import get_msg
from validation import check_sudoku_name
from flask import redirect, render_template, request, session
from db import get_sudoku, get_sudoku_shares, get_public_sudokus, get_user_sudokus, add_sudoku

@app.route("/sudoku/<int:id>")
def sudoku(id):
    sudoku = get_sudoku(id)

    if sudoku == None: return render_template("sudokus.html", error=get_msg("sudoku_id_not_found"))
    
    display = sudoku[3]
    owner_id = sudoku[4]
    shared_to = get_sudoku_shares(id)
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

    return render_template("sudokus.html", error=get_msg("sudoku_no_permission"))

@app.route("/sudokus")
def sudokus():
    sudokus = get_public_sudokus();

    user_sudokus = None
    if "user_id" in session:
        user_sudokus = get_user_sudokus(session["user_id"]);

    return render_template("sudokus.html", sudokus=sudokus, user_sudokus=user_sudokus);

@app.route("/new", methods=["GET", "POST"])
def new():
    # The user must be logged in to submit a new sudoku
    if "user_id" not in session:
        return render_template("index.html", error="You must be logged in!")
    
    if request.method == "GET":
        return render_template("create.html")

    name = request.form["name"]
    if not check_sudoku_name(name):
        return render_template("create.html", error=get_msg("sudoku_name_invalid"))

    cells = [];
    for row in range(0, 9):
        cells.append([])
        for col in range(0, 9):
            cells[row].append(request.form["cell"+str(row)+str(col)])
    instructions = request.form["instructions"]
    display = request.form["display"]

    id = add_sudoku(session["user_id"], name, cells, instructions, display)

    if (id < 0):
        return render_template("create.html", error=get_msg("sudoku_db_error"))

    return redirect("/sudoku/" + str(id))