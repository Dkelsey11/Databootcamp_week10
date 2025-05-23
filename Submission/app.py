# Import the dependencies.
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import pandas as pd
from flask import Flask, jsonify
import datetime as dt
import numpy as np
import os 


#################################################
# Database Setup
#################################################
os.chdir(os.path.dirname(os.path.realpath(__file__)))
# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)
# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station


#session = Session(engine)
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
        "Welcome to the Hawaii Climate Analysis API!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/temp/&lt;start&gt<br/>"
        "/api/v1.0/temp/&lt;start&gt/&lt;end&gt<br/>"
        "<p>'start' and 'end' date should be in the format MMDDYYYY.</p>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year"""
    # Calculate the date 1 year ago from last date in database
    year_ago_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query for the date and precipitation for the last year
    precipitation = Session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago_date).all()

    Session.close()
    # Dict with date as the key and prcp as the value
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    results = Session.query(Station.station).all()

    Session.close()

    # Unravel results into a 1D array and convert to a list
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
    
@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return the temperature observations (tobs) for previous year."""
    # Calculate the date 1 year ago from last date in database
    year_ago_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the primary station for all tobs from the last year
    tobs_data = Session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= year_ago_date).all()

@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return the temperature observations (tobs) for previous year."""
    # Calculate the date 1 year ago from last date in database
    year_ago_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the primary station for all tobs from the last year
    tobs_data = Session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= year_ago_date).all()
        
Session.close()
    # Unravel results into a 1D array and convert to a list
temps = list(np.ravel(tobs_data))

    # Return the results
        return jsonify(temps=temps)


@app.route("/api/v1.0/temp/&lt;start&gt")
@app.route("/api/v1.0/temp/&lt;start&gt/&lt;end&gt")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        # start = dt.datetime.strptime(start, "%m/%d/%Y")
        # # calculate TMIN, TAVG, TMAX for dates greater than start
        # results = session.query(*sel).\
        #     filter(Measurement.date >= start).all()
        # # Unravel results into a 1D array and convert to a list
        # temps = list(np.ravel(results))
        # return jsonify(temps)

        start = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()

        session.close()

temps = list(np.ravel(results))
        return jsonify(temps)

    # calculate TMIN, TAVG, TMAX with start and stop
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


if __name__ == '__main__':
    app.run()
        


