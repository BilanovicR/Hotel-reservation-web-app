import flask
from flask import Blueprint
from flask import request
from flask import session
import datetime

# Da ne bi doslo do ciklicnih zavisnosti uveden je novi modul
# koji sadrzi objekat koji predstavlja konekciju ka bazi podataka.
from utils.db_connection import mysql

bills = Blueprint("bills", __name__)

@bills.route('/getBill/<int:bill_id>', methods=["GET"])
def getBill(bill_id):
    connection = mysql.get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT bill.* FROM bill WHERE bill.id = %s ", (bill_id))
    bill = cursor.fetchone()
    if bill is not None:
        return flask.jsonify(bill, {"success" : True})
    return flask.jsonify({"success": False})