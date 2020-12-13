from app import app
from errors import get_msg
from validation import check_sudoku_name
from flask import redirect, render_template, request, session
from db import get_sudoku, get_sudoku_shares, get_public_sudokus, get_user_sudokus, \
               add_sudoku, delete_sudoku, get_user, share_sudoku, set_sudoku_display, \
               get_comments_by_sudoku, get_shared_sudokus

@app.route("/sudoku/<int:id>")
def sudoku(id):
    error_msg = None
    if "err" in request.args:
        error_msg = get_msg(request.args["err"])

    sudoku = get_sudoku(id)

    if sudoku == None:
        return redirect("/sudokus?err=sudoku_id_not_found")
    
    display = sudoku[3]
    owner_id = sudoku[4]
    shared_to = get_sudoku_shares(id)
    if (shared_to == None):
        shared_to = []

    send = False
    if display == "public" or display == "link":
        send = True
    elif display == "private" and "user_id" in session:
        user_id = session["user_id"]
        if user_id == owner_id or user_id in shared_to:
            send = True

    comments = get_comments_by_sudoku(id)

    if send:
        return render_template("sudoku.html", name=sudoku[0], id=id, \
                   cells=sudoku[1], rules=sudoku[2], owner_id=owner_id, \
                   comments=comments, error=error_msg)

    return redirect("/sudokus?err=sudoku_no_permission")

@app.route("/sudokus")
def sudokus():
    error_msg = None
    if "err" in request.args:
        error_msg = get_msg(request.args["err"])

    sudokus = get_public_sudokus()

    user_sudokus = None
    shared_sudokus = None
    if "user_id" in session:
        user_sudokus = get_user_sudokus(session["user_id"])
        shared_sudokus = get_shared_sudokus(session["user_id"])

    return render_template("sudokus.html", sudokus=sudokus,
                    shared_sudokus=shared_sudokus, user_sudokus=user_sudokus,
                    error=error_msg);

@app.route("/sudoku/new", methods=["GET", "POST"])
def new_sudoku():
    error_msg = None
    if "err" in request.args:
        error_msg = get_msg(request.args["err"])

    if "user_id" not in session:
        return redirect("/?err=create_no_user")
    
    if request.method == "GET":
        return render_template("create.html", error=error_msg)

    name = request.form["name"]
    if not check_sudoku_name(name):
        return redirect("/sudoku/new?err=sudoku_name_invalid")

    cells = [];
    for row in range(0, 9):
        cells.append([])
        for col in range(0, 9):
            cells[row].append(request.form["cell"+str(row)+str(col)])
    instructions = request.form["instructions"]
    display = request.form["display"]

    id = add_sudoku(session["user_id"], name, cells, instructions, display)

    if (id < 0):
        redirect("/sudoku/new?err=sudoku_db_error")

    return redirect("/sudoku/" + str(id))

@app.route("/edit", methods=["POST"])
def edit():
    edit_type = request.form["action"]
    sudoku_id = request.form["sudoku_id"]

    sudoku = get_sudoku(sudoku_id)

    if not "user_id" in session:
        return redirect("/sudoku/" + sudoku_id + "?err=edit_no_user")
    if sudoku[4] != session["user_id"]:
        return redirect("/sudoku/" + sudoku_id + "?err=edit_wrong_user")

    if edit_type == "delete":
        delete_sudoku(sudoku_id)
        return redirect("/sudokus")

    if edit_type == "share":
        username = request.form["username"]
        user = get_user(username)
        if user:
            share_sudoku(sudoku_id, user[0])

    if edit_type == "display":
        display = request.form["display"]
        set_sudoku_display(sudoku_id, display)

    return redirect("/sudoku/" + sudoku_id)