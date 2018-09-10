import datetime
import flask
from flask import Flask
from utils.db_connection import mysql
from flask import request
from flask import session

from blueprints.simple_login import simple_login
from blueprints.user_services import user_services
from blueprints.membership import membership
from blueprints.reservations import reservations
from blueprints.guests import guests
from blueprints.bill import bills


app = Flask(__name__, static_url_path="")

app.secret_key = "NEKI_RANDOM_STRING"

app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = ""
app.config["MYSQL_DATABASE_DB"] = "projekat"
app.config["MYSQL_DATABASE_HOST"] = "localhost"

mysql.init_app(app)

app.register_blueprint(simple_login)
app.register_blueprint(user_services, url_prefix="/users")
app.register_blueprint(membership)
app.register_blueprint(reservations)
app.register_blueprint(guests)
app.register_blueprint(bills)

@app.route("/")
@app.route("/index")
@app.route("/index.html")
def home():
    return app.send_static_file("index.html")
app.run("0.0.0.0", 8000, threaded=True, debug = True)
