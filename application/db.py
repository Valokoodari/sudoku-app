from app import app
from os import getenv
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")

db = SQLAlchemy(app)

def get_sudoku(id):
    sql = "SELECT name,cells,instructions,display,owner_id,user_ids " \
          "FROM sudokus WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone();

def get_sudokus():
    sql = "SELECT sudokus.id,sudokus.name,users.display_name FROM sudokus,users " \
          "WHERE sudokus.display=3 AND sudokus.owner_id = users.id"
    result = db.session.execute(sql);
    return result.fetchall();

def get_user_sudokus(user_id):
    sql = "SELECT sudokus.id,sudokus.name,users.display_name FROM sudokus,users " \
          "WHERE sudokus.owner_id = users.id AND sudokus.owner_id=:user_id"
    
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall();

def add_sudoku(user_id, name, cells, instructions, display):
    sql = "INSERT INTO sudokus (owner_id, name, cells, instructions, display) " \
          "VALUES (:user_id, :name, :cells, :instructions, :display)"
    db.session.execute(sql, {"user_id":user_id, "name":name, "cells":cells, \
                    "instructions":instructions, "display":display})
    db.session.commit()

    result = db.session.execute("SELECT MAX(id) FROM sudokus")

    if (result == None):
        return -1;

    return result.fetchone()[0]

def get_user(username):
    sql = "SELECT id, password_hash, display_name FROM users " \
          "WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()

def create_user(username, password_hash, display_name):
    sql = "INSERT INTO users (username, password_hash, display_name, permission_level) " \
          "VALUES (:username,:password_hash,:display_name,0)"
    db.session.execute(sql, {"username":username, \
               "password_hash":password_hash, "display_name":display_name})
    db.session.commit()