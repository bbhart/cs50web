import os

from flask import Flask, render_template, request, session
from flask_session import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up DB connection 
engine = create_engine('postgresql://bhart@localhost/postgres')
db = scoped_session(sessionmaker(engine))

# Set up Flask routes
@app.route("/", methods=["GET", "POST"])
def index():
    flights = db.execute("SELECT * from flights").fetchall()
    return render_template("index.html", flights=flights)



