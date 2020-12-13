from app import app
from flask import render_template

import accounts
import sudokus
import comments

@app.route("/")
def index():
    return render_template("index.html")
