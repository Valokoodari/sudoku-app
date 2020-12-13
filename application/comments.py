from app import app
from errors import get_msg
from db import add_comment
from flask import redirect, render_template, request, session

@app.route("/comment/new", methods=["POST"])
def new_comment():
    if "user_id" not in session:
        return render_temp("index.html", error=get_msg("comment_no_user"))

    user_id = session["user_id"]
    sudoku_id = request.form["sudoku_id"]
    rating = request.form["rating"]
    content = request.form["comment"]

    add_comment(user_id, sudoku_id, rating, content)

    return redirect("/sudoku/" + sudoku_id)