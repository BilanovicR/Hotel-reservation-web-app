import flask
from flask import Blueprint
from flask import request
from flask import session
import hashlib
import datetime

# Da ne bi doslo do ciklicnih zavisnosti uveden je novi modul
# koji sadrzi objekat koji predstavlja konekciju ka bazi podataka.
from utils.db_connection import mysql

simple_login = Blueprint("simple_login", __name__)

@simple_login.route("/login", methods=["POST"])
def login():
    login_user = request.json
    cursor = mysql.get_db().cursor()
    hashedPassword = hashlib.md5(login_user["password"].encode())
    cursor.execute("SELECT * FROM user WHERE username=%s AND password=%s", (login_user["username"], hashedPassword.hexdigest()))
    user = cursor.fetchone()

    if user is not None:
        session["user"] = user
        user['password'] = ''
        return flask.jsonify({"success": True})

    return flask.jsonify({"success": False})

@simple_login.route("/isLoggedin", methods=["GET"])
def is_loggedin():
    # Vraca true ako je korisnik ulogovan,
    # u suprotnom vraca false.
    return flask.jsonify(session.get("user") is not None)

@simple_login.route("/logout", methods=["GET"])
def logout():
    session.pop("user", None)
    session.pop("reservation", None)
    session.pop("availableRooms", None)
    return flask.jsonify({"success": True})


@simple_login.route("/loggedInUser", methods=["GET"])
def logged_in_user():
    if session.get("user") is not None:
        login_user = request.json
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM user WHERE user.id=%s", (session.get("user")["id"]))
        user = cursor.fetchone()
        user["password"] = ""

        return flask.jsonify(user)
    else:
        return "Access denied!", 401

@simple_login.route("/authorized", methods = ["POST"])
def authorized():
    login_user = request.json
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT user.id FROM user, role WHERE user.id=%s AND user.role_id = role.id AND role.role = "ADMIN"', (login_user["id"]))
    admin = cursor.fetchone()
    if admin is not None:
        return flask.jsonify({"success": True})
    return flask.jsonify({"success": False})

