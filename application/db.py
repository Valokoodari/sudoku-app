from app import app
from os import getenv
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")

db = SQLAlchemy(app)

def get_sudoku(id: int) -> list:
    sql = "SELECT name, cells, instructions, display, owner_id " \
          "FROM sudokus " \
          "WHERE id = :id"

    result = db.session.execute(sql, { "id": id })
    return result.fetchone();

def get_public_sudokus() -> list:
    sql = "SELECT sudokus.id, sudokus.name, users.display_name " \
          "FROM sudokus, users " \
          "WHERE sudokus.display = 'public' " \
          "AND sudokus.owner_id = users.id"

    result = db.session.execute(sql);
    return result.fetchall();

def get_user_sudokus(user_id: int) -> list:
    sql = "SELECT sudokus.id, sudokus.name, users.display_name " \
          "FROM sudokus, users " \
          "WHERE sudokus.owner_id = users.id " \
          "AND sudokus.owner_id = :user_id"
    
    result = db.session.execute(sql, { "user_id": user_id })
    return result.fetchall()

def get_shared_sudokus(user_id: int) -> list:
    sql = "SELECT sudokus.id, sudokus.name, users.display_name " \
          "FROM sudokus, users, shares " \
          "WHERE shares.user_id = :user_id " \
          "AND sudokus.id = shares.sudoku_id " \
          "AND sudokus.owner_id = users.id"
    
    result = db.session.execute(sql, { "user_id": user_id })
    return result.fetchall()

def get_sudoku_shares(sudoku_id: int) -> list:
    sql = "SELECT user_id FROM shares WHERE sudoku_id = :sudoku_id"

    result = db.session.execute(sql, { "sudoku_id": sudoku_id })
    return list(s[0] for s in result.fetchall());

def add_sudoku(user_id: int, name: str, cells: list, instructions: str, display: str) -> int:
    sql = "INSERT INTO sudokus (owner_id, name, cells, instructions, display) " \
          "VALUES (:user_id, :name, :cells, :instructions, :display)"

    db.session.execute(sql, { "user_id": user_id, "name": name, \
                    "cells": cells, "instructions": instructions, \
                    "display": display })
    db.session.commit()

    result = db.session.execute("SELECT MAX(id) FROM sudokus")

    if (result == None): return -1;

    return result.fetchone()[0]

def share_sudoku(sudoku_id: int, user_id: int):
    sql = "INSERT INTO shares (sudoku_id, user_id) " \
          "VALUES (:sudoku_id, :user_id)"

    db.session.execute(sql, { "sudoku_id": sudoku_id, "user_id": user_id })
    db.session.commit()

def set_sudoku_display(sudoku_id: int, display: str):
    sql = "UPDATE sudokus SET display = :display WHERE id = :id"

    db.session.execute(sql, { "id": sudoku_id, "display": display })
    db.session.commit()

def delete_sudoku(sudoku_id: int):
    set_sudoku_display(sudoku_id, "deleted")

def get_user(username: str) -> list:
    sql = "SELECT id, password_hash, display_name FROM users " \
          "WHERE username = :username"

    result = db.session.execute(sql, { "username": username })
    return result.fetchone()

def is_username_taken(username: str) -> bool:
    sql = "SELECT id FROM users WHERE username = :username"

    result = db.session.execute(sql, { "username": username })
    return result.fetchone() != None

def create_user(username: str, password_hash: str, display_name: str) -> list:
    sql = "INSERT INTO users (username, password_hash, display_name, permission_level) " \
          "VALUES (:username, :password_hash, :display_name, 0)"

    try:
        db.session.execute(sql, { "username": username, \
                        "password_hash": password_hash, \
                        "display_name": display_name })

        db.session.commit()
        return get_user(username)
    except:
        return None

def add_comment(user_id: int, sudoku_id: int, rating: int, content: str):
    sql = "INSERT INTO comments (user_id, sudoku_id, rating, content) " \
          "VALUES (:user_id, :sudoku_id, :rating, :content)"

    db.session.execute(sql, { "user_id": user_id, "sudoku_id": sudoku_id, \
                              "rating": rating, "content": content })
    db.session.commit()

def get_comments_by_sudoku(sudoku_id: int) -> list:
    sql = "SELECT users.display_name, comments.rating, comments.content " \
          "FROM comments, users " \
          "WHERE sudoku_id = :sudoku_id " \
          "AND users.id = comments.user_id"

    result = db.session.execute(sql, { "sudoku_id": sudoku_id })

    return result.fetchall()