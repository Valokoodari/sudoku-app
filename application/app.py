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
    return render_template("layout.html")

@app.route("/sudoku/<int:id>")
def sudoku(id):
    result = db.session.execute("SELECT cells FROM sudokus")
    cells = result.fetchall()[id][0]
    return render_template("sudoku.html", numbers=cells)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT password_hash FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if (user == None):
        print("Invalid Username!")
        # TODO - invalid username
    else:
        password_hash = user[0]
        if check_password_hash(password_hash, password):
            session["username"] = username
        else:
            print("Invalid Password!")
            # TODO - invalid password

    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
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
        session["username"] = username
        
    return redirect("/")

