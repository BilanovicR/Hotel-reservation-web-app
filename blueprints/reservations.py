import flask
from flask import Blueprint
from flask import request
from flask import session
import datetime

# Da ne bi doslo do ciklicnih zavisnosti uveden je novi modul
# koji sadrzi objekat koji predstavlja konekciju ka bazi podataka.
from utils.db_connection import mysql

reservations = Blueprint("reservations", __name__)

@reservations.route('/requestedReservation', methods=["PUT"])
def requestedReservation():
    reservation = request.json
    if reservation is not None: 
        session["reservation"] = reservation
        #availableRooms = 0
        arrival = datetime.datetime.strptime(reservation["arrival"], "%Y-%m-%dT%H:%M:%S.%fZ")
        arrival.strftime("%Y-%m-%d")
        departure = datetime.datetime.strptime(reservation["departure"], "%Y-%m-%dT%H:%M:%S.%fZ")
        departure.strftime("%Y-%m-%d")
        cursor = mysql.get_db().cursor()
        statement = "SELECT DISTINCT room.* FROM room WHERE room.id NOT IN(SELECT occupied_room.room_id FROM occupied_room, reservation WHERE occupied_room.reservation_id = reservation.id AND ((reservation.arrival > %s AND reservation.departure < %s) OR (reservation.departure > %s AND reservation.arrival < %s)))"
        cursor.execute(statement, (departure, arrival, arrival, departure))
        roomIDs = cursor.fetchall() #dobavljene sve sobe koje su slobodne u tom terminu
        
        print (roomIDs)
        print (len(roomIDs))
        print(roomIDs is not None)
        print(len(roomIDs) > 0)
        if roomIDs is not None and len(roomIDs) > 0:
            session["availableRooms"] = roomIDs
            return flask.jsonify({"success": True})
        else:
            session.pop("reservation", None)
            return flask.jsonify({"success": False})
    else:
        return flask.jsonify({"success": False})  

@reservations.route('/getReservation', methods = ["GET"])
def getReservation():
    if session.get("reservation") is not None:
        return flask.jsonify(session.get("reservation"))
    else:
        return flask.jsonify({"error": False})


@reservations.route('/makeReservation', methods = ['POST'])
def makeReservation():
    reservation = request.json
    if reservation is not None:
        connection = mysql.get_db()
        arrival = datetime.datetime.strptime(reservation["arrival"], "%Y-%m-%dT%H:%M:%S.%fZ")
        arrival.strftime("%Y-%m-%d")
        departure = datetime.datetime.strptime(reservation["departure"], "%Y-%m-%dT%H:%M:%S.%fZ")
        departure.strftime("%Y-%m-%d")
        cursor = connection.cursor()
        statement = "INSERT INTO reservation(arrival, departure, num_of_guests, reservation_status_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(statement, (arrival, departure, reservation['num_of_guests'], 2))
        connection.commit()
        currentReservationId = cursor.lastrowid #dobijem id insertovane rezervacije
        statement = 'INSERT INTO user_reservation(user_id, reservation_id) VALUES(%s, %s)'
        cursor.execute(statement,(reservation['guest_id'], currentReservationId))
        connection.commit()
        statement = "INSERT INTO occupied_room(room_id, reservation_id) VALUES (%s, %s)"
        cursor.execute(statement, (session.get("availableRooms")[0]["id"], currentReservationId))
        connection.commit()
        days = (departure - arrival).days
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        statement = "INSERT INTO bill(quantity, item_price, date) VALUES (%s, (SELECT room_type.price FROM room_type, room, occupied_room WHERE room_type.id = room.room_type_id AND room.id = occupied_room.room_id AND occupied_room.reservation_id = %s), %s)"        
        cursor.execute(statement, (days, currentReservationId, today))
        connection.commit()
        billID = cursor.lastrowid
        statement = "INSERT INTO bill_reservation(bill_id, reservation_id) VALUES (%s, %s)"
        cursor.execute(statement, (billID, currentReservationId))
        connection.commit()
        session.pop("availableRooms", None)
        session.pop("reservation", None)
        return flask.jsonify({"success": True})
    else:
        return flask.jsonify({"error": False})

@reservations.route('/getMyReservations/<int:user_id>', methods = ['GET'])
def getMyReservations(user_id):
    connection = mysql.get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT reservation.*, reservation_status.status FROM reservation, user_reservation, reservation_status WHERE user_reservation.user_id = %s AND user_reservation.reservation_id = reservation.id AND reservation.reservation_status_id = reservation_status.id", (user_id))
    reservations = cursor.fetchall()
    if reservations is not None:
        return flask.jsonify(reservations, {"success" : True})
    return flask.jsonify({"success": False})

@reservations.route('/getReservations', methods = ['GET'])
def getReservations():
    connection = mysql.get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT reservation.* , occupied_room.room_id, reservation_status.status FROM reservation, occupied_room, reservation_status WHERE reservation.id = occupied_room.reservation_id AND reservation.reservation_status_id = reservation_status.id")
    reservations = cursor.fetchall()
    if reservations is not None:
        return flask.jsonify(reservations, {"success" : True})
    return flask.jsonify({"success": False})

@reservations.route("/cancelReservation/<int:res_id>", methods=["POST"])
def cancelReservation(res_id):
    connection = mysql.get_db()
    cursor = connection.cursor()
    statement = "UPDATE reservation SET reservation.reservation_status_id = 3 WHERE reservation.id = %s"
    cursor.execute(statement, (res_id))
    connection.commit()
    return flask.jsonify({"status": "done"}), 201