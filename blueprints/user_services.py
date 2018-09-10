import flask
from flask import Blueprint
from utils.db_connection import mysql

user_services = Blueprint("user_services", __name__)

@user_services.route("/", methods=["GET"])
def users():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT id, username, name, surname FROM user")
    rows = cursor.fetchall()

    return flask.jsonify(rows)

@user_services.route("/<int:user_id>", methods=["GET"])
def category(user_id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT id, username, name, surname FROM user WHERE id=%s", user_id)
    row = cursor.fetchone()

    return flask.jsonify(row)
