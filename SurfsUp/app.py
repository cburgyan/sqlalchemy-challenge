# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import pandas as pd
import datetime as dt

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)




#################################################
# Flask Routes
#################################################
precipitationRoute = '/api/v1.0/precipitation'
stationsRoute = '/api/v1.0/stations'
tobsRoute = '/api/v1.0/tobs'

@app.route('/')
def home():
    routes = f"<br><a href='{precipitationRoute}'>{precipitationRoute}</a><br>\
    <a href='{stationsRoute}'>{stationsRoute}</a><br>\
    <a href='{tobsRoute}'>{tobsRoute}</a>"
    return "Home" + routes

@app.route(precipitationRoute)
def precipitationPage():
    # Perform a query to retrieve the data and precipitation scores
    recent12Months = session.query(measurement.date, measurement.prcp).filter(measurement.date >=
                                                                              '2016-08-23').order_by(
        measurement.date).filter(measurement.prcp != None).order_by(measurement.date).all()
    # print(recent12Months)

    precipDictionary = {}
    count = 0
    for row in recent12Months:
        if row[0] not in precipDictionary:
            precipDictionary[row[0]] = []
        precipDictionary[row[0]].append(row[1])
        count += 1

    # print(len(precipDictionary))
    # print(count)
    # print(precipDictionary)

    return jsonify(precipDictionary)

@app.route(stationsRoute)
def stationPage():
    pass



if __name__ == "__main__":
    app.run(debug=True)