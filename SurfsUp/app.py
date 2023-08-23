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
# Flask _routes
#################################################
precipitation_route = '/api/v1.0/precipitation'
stations_route = '/api/v1.0/stations'
tobs_route = '/api/v1.0/tobs'
tobs_start_route = '/api/v1.0/<start>'

tobs_start_route_str = '/api/v1.0/&lt;start&gt;'
tobs_start_end_route = '/api/v1.0/<start>/<end>'
tobs_start_end_route_str = '/api/v1.0/&lt;start&gt;/&lt;end&gt;'


@app.route('/')
def home():
    routes = f"<br><a href='{precipitation_route}'>{precipitation_route}</a><br>\
    <a href='{stations_route}'>{stations_route}</a><br>\
    <a href='{tobs_route}'>{tobs_route}</a><br><br>\
    NOTE: Replace '&lt;start&gt;' in the URL with a date of the form YYYY-MM-DD<br>\
    <a href='{tobs_start_route}'>{tobs_start_route_str}</a>  <br><br>\
    NOTE: Replace '&lt;start&gt;' and '&lt;end&gt;' in the URL with a date of the form " \
             f"YYYY-MM-DD <br>\
    <a href='{tobs_start_end_route}'>{tobs_start_end_route_str}</a>"

    return "<h1>Home</h1>" + routes


@app.route(precipitation_route)
def precipitation_page():
    # Perform a query to retrieve the data and precipitation scores
    recent12_months = session.query(
        measurement.date, measurement.prcp).\
        filter(measurement.date >= '2016-08-23').\
        order_by(measurement.date).\
        filter(measurement.prcp != None).\
        order_by(measurement.date).all()

    precip_dictionary = {}
    for row in recent12_months:
        if row[0] not in precip_dictionary:
            precip_dictionary[row[0]] = []
        precip_dictionary[row[0]].append(row[1])

    return jsonify(precip_dictionary)


@app.route(stations_route)
def station_page():
    stations_query = session.query(station.station, station.name).all()

    stations_dictionary = {}
    for row in stations_query:
        if row[0] not in stations_dictionary:
            stations_dictionary[row[0]] = row[1]

    return jsonify(stations_dictionary)


@app.route(tobs_route)
def tobs_page():
    most_active_stations = session.query(
        measurement.station,
        func.count(measurement.date)).\
        group_by(measurement.station).\
        order_by(func.count(measurement.date).desc()).all()

    temperatures_most_active_station = session.query(
        measurement.date, measurement.tobs).\
        filter(measurement.station == most_active_stations[0][0]).\
        filter(measurement.date > '2016-08-23').all()


    temp_dictionary = {}
    for row in temperatures_most_active_station:
        temp_dictionary[row[0]] = row[1]

    return jsonify(temp_dictionary)


@app.route(tobs_start_route)
def tobs_start_page(start, end=None):
    tobs_min_max_avg = session.query(
        func.min(measurement.tobs),
        func.max(measurement.tobs),
        func.avg(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.tobs != None).all()

    print(tobs_min_max_avg)
    t_min = tobs_min_max_avg[0][0]
    t_max = tobs_min_max_avg[0][1]
    t_avg = tobs_min_max_avg[0][2]
    temp_dict = {"TMIN": t_min, "TMAX": t_max, "TAVG": t_avg}

    return jsonify(temp_dict)


@app.route(tobs_start_end_route)
def tobs_start_end_page(start, end):
    tobs_min_max_avg = session.query(
        func.min(measurement.tobs),
        func.max(measurement.tobs),
        func.avg(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).\
        filter(measurement.tobs != None).all()

    print(tobs_min_max_avg)
    t_min = tobs_min_max_avg[0][0]
    t_max = tobs_min_max_avg[0][1]
    t_avg = tobs_min_max_avg[0][2]
    temp_dict = {"TMIN": t_min, "TMAX": t_max, "TAVG": t_avg}

    return jsonify(temp_dict)


if __name__ == "__main__":
    app.run(debug=True)