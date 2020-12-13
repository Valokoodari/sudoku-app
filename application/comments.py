from app import app
from errors import get_msg
from db import add_comment
from flask import redirect, render_template, request, session

@app.route("/comment/new", methods=["POST"])
def new_comment():
    sudoku_id = request.form["sudoku_id"]

    error = None
    if "user_id" not in session:
        error = "comment_no_user"
    elif "csrf_token" not in session or "csrf_token" not in request.form:
        error = "no_csrf_token"
    elif session["csrf_token"] != request.form["csrf_token"]:
        error = "invalid_csrf_token"

    if error: redirect("/sudoku/" + sudoku_id + "?err=" + error)

    user_id = session["user_id"]
    rating = request.form["rating"]
    content = request.form["comment"]

    add_comment(user_id, sudoku_id, rating, content)

    return redirect("/sudoku/" + sudoku_id)