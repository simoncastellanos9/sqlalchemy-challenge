import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurements
Station = Base.classes.stations

session=Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

year = '2016-08-23'

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/observations"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prec = session.query(Measurement.date, func.avg(Measurement.prcp)).filter(Measurement.date >= year).group_by(Measurement.date).all()
    return jsonify(prec)

@app.route("/api/v1.0/stations")
def stations():
    stat = session.query(Station.station, Station.name).all()
    return jsonify(stat)

@app.route("/api/v1.0/tobs")
def tobs():
    temps = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= year).all()
    return jsonify(temps)

@app.route("/api/v1.0/<date>")
def startDateOnly(date):
    dtemps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(dtemps)

@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    mdaytemps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(mdaytemps)

if __name__ == "__main__":
    app.run(debug=True)