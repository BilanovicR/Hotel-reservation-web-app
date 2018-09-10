import flask
from flask import Blueprint
from flask import request
from flask import session
import hashlib
import datetime

# Da ne bi doslo do ciklicnih zavisnosti uveden je novi modul
# koji sadrzi objekat koji predstavlja konekciju ka bazi podataka.
from utils.db_connection import mysql

membership = Blueprint("membership", __name__)

@membership.route("/register", methods = ["POST"])
def register():
    data = request.json #objekat koji funkciji salje iz kontrolera
    db = mysql.get_db()
    cursor = db.cursor()
    statement = "INSERT INTO user(first_name, last_name, date_of_birth, gender, email, username, password, role_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    hashedPassword = hashlib.md5(data["password"].encode())
    stringToDate = datetime.datetime.strptime(data["date_of_birth"], "%Y-%m-%dT%H:%M:%S.%fZ")
    
    cursor.execute(statement, (data["first_name"], data["last_name"], stringToDate, data["gender"], data["email"], data["username"], hashedPassword.hexdigest(), 3))
    db.commit()

    return flask.jsonify({"status": "done"}), 201 #status Created

@membership.route("/updateProfile", methods=["PUT"])
def updateProfile():
    data = request.json
    db = mysql.get_db()
    cursor = db.cursor()
    hashedPassword = hashlib.md5(data["password"].encode())
    stringToDate = datetime.datetime.strptime(data["date_of_birth"], "%Y-%m-%dT%H:%M:%S.%fZ")
    statement = "UPDATE user SET first_name =%s, last_name =%s, date_of_birth =%s, gender=%s, email =%s, username =%s, password =%s, role_id=%s WHERE id=%s"
    
    cursor.execute(statement, (data["first_name"], data["last_name"], stringToDate, data["gender"], data["email"], data["username"], hashedPassword.hexdigest(), 3, data["id"]))
    db.commit()

    return flask.jsonify({"status": "done"}), 201