# Import the dependencies.
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from datetime import datetime, timedelta

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)



#################################################
# Flask Setup
#################################################
app = Flask(__name__)




#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a JSON list of precipitation data for the last 12 months."""
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_date_obj = datetime.strptime(last_date, "%Y-%m-%d")
    one_year_ago = last_date_obj - timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    precip_dict = {date: prcp for date, prcp in results}

    return jsonify(precip_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    results = session.query(Station.station, Station.name).all()
    station_list = [{"station": station, "name": name} for station, name in results]
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the most active station for the previous year."""
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_date_obj = datetime.strptime(last_date, "%Y-%m-%d")
    one_year_ago = last_date_obj - timedelta(days=365)

    most_active_station = session.query(Measurement.station)\
        .group_by(Measurement.station)\
        .order_by(func.count().desc()).first()[0]

    tobs_data = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active_station)\
        .filter(Measurement.date >= one_year_ago)\
        .order_by(Measurement.date).all()

    tobs_list = [{"date": date, "tobs": tobs} for date, tobs in tobs_data]
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def calc_temps(start):
    """Calculate TMIN, TAVG, and TMAX for dates greater than or equal to the start date."""
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start_date).all()

        temp_data = results[0]
        temp_dict = {
            "TMIN": temp_data[0],
            "TAVG": temp_data[1],
            "TMAX": temp_data[2]
        }
        return jsonify(temp_dict)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/api/v1.0/<start>/<end>")
def calc_temps2(start, end):
    """Calculate TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date.between(start_date, end_date)).all()

        temp_data = results[0]
        temp_dict = {
            "TMIN": temp_data[0],
            "TAVG": temp_data[1],
            "TMAX": temp_data[2]
        }
        return jsonify(temp_dict)
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=False)