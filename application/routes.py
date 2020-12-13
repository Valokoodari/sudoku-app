from app import app
from errors import get_msg
from flask import render_template,request

import accounts
import sudokus
import comments

@app.route("/")
def index():
    error_msg = None
    if "err" in request.args:
        error_msg = get_msg(request.args["err"])

    return render_template("index.html", error=error_msg)
