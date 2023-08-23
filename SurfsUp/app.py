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
tobsStartRoute = '/api/v1.0/<start>'

tobsStartRouteStr = '/api/v1.0/&lt;start&gt;'
tobsStartEndRoute = '/api/v1.0/<start>/<end>'
tobsStartEndRouteStr = '/api/v1.0/&lt;start&gt;/&lt;end&gt;'


@app.route('/')
def home():
    routes = f"<br><a href='{precipitationRoute}'>{precipitationRoute}</a><br>\
    <a href='{stationsRoute}'>{stationsRoute}</a><br>\
    <a href='{tobsRoute}'>{tobsRoute}</a><br><br>\
    NOTE: Replace '&lt;start&gt;' in the URL with a date of the form YYYY-MM-DD<br>\
    <a href='{tobsStartRoute}'>{tobsStartRouteStr}</a>  <br><br>\
    NOTE: Replace '&lt;start&gt;' and '&lt;end&gt;' in the URL with a date of the form " \
             f"YYYY-MM-DD <br>\
    <a href='{tobsStartEndRoute}'>{tobsStartEndRouteStr}</a>"

    return "<h1>Home</h1>" + routes


@app.route(precipitationRoute)
def precipitationPage():
    # Perform a query to retrieve the data and precipitation scores
    recent12Months = session.query(
        measurement.date, measurement.prcp).\
        filter(measurement.date >= '2016-08-23').\
        order_by(measurement.date).\
        filter(measurement.prcp != None).\
        order_by(measurement.date).all()

    precipDictionary = {}
    for row in recent12Months:
        if row[0] not in precipDictionary:
            precipDictionary[row[0]] = []
        precipDictionary[row[0]].append(row[1])

    return jsonify(precipDictionary)


@app.route(stationsRoute)
def stationPage():
    stationsQuery = session.query(station.station, station.name).all()

    stationsDictionary = {}
    for row in stationsQuery:
        if row[0] not in stationsDictionary:
            stationsDictionary[row[0]] = row[1]

    return jsonify(stationsDictionary)


@app.route(tobsRoute)
def tobsPage():
    mostActiveStations = session.query(
        measurement.station,
        func.count(measurement.date)).\
        group_by(measurement.station).\
        order_by(func.count(measurement.date).desc()).all()

    temperaturesMostActiveStation = session.query(
        measurement.date, measurement.tobs).\
        filter(measurement.station == mostActiveStations[0][0]).\
        filter(measurement.date > '2016-08-23').all()


    tempDictionary = {}
    for row in temperaturesMostActiveStation:
        tempDictionary[row[0]] = row[1]

    return jsonify(tempDictionary)


@app.route(tobsStartRoute)
def tobsStartPage(start, end=None):
    tobsMinMaxAvg = session.query(
        func.min(measurement.tobs),
        func.max(measurement.tobs),
        func.avg(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.tobs != None).all()

    print(tobsMinMaxAvg)
    TMIN = tobsMinMaxAvg[0][0]
    TMAX = tobsMinMaxAvg[0][1]
    TAVG = tobsMinMaxAvg[0][2]
    tempDict = {"TMIN": TMIN, "TMAX": TMAX, "TAVG": TAVG}

    return jsonify(tempDict)


@app.route(tobsStartEndRoute)
def tobsStartEndPage(start, end):
    tobsMinMaxAvg = session.query(
        func.min(measurement.tobs),
        func.max(measurement.tobs),
        func.avg(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).\
        filter(measurement.tobs != None).all()

    print(tobsMinMaxAvg)
    TMIN = tobsMinMaxAvg[0][0]
    TMAX = tobsMinMaxAvg[0][1]
    TAVG = tobsMinMaxAvg[0][2]
    tempDict = {"TMIN": TMIN, "TMAX": TMAX, "TAVG": TAVG}

    return jsonify(tempDict)


if __name__ == "__main__":
    app.run(debug=True)