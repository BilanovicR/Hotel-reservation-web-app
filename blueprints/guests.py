import flask
from flask import Blueprint
from flask import request
from flask import session
import datetime

# Da ne bi doslo do ciklicnih zavisnosti uveden je novi modul
# koji sadrzi objekat koji predstavlja konekciju ka bazi podataka.
from utils.db_connection import mysql

guests = Blueprint("guests", __name__)

@guests.route('/getGuests', methods = ['GET'])
def getGuests():
    connection = mysql.get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT user.* FROM user, role WHERE user.role_id = role.id AND role.role = "GUEST"')
    guests = cursor.fetchall()
    if guests is not None:
        return flask.jsonify(guests, {"success" : True})
    return flask.jsonify({"success": False})
