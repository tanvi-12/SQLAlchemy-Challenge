#Imports
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def Home_page():
    """List all available api routes."""
    return (
        f"Welcome to the Climate Analysis page for Hawaii<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"Precipitation data by date: /api/v1.0/precipitation<br/>"
        f"List of all stations: /api/v1.0/stations<br/>"
        f"Temperatures at most active station in the last year: /api/v1.0/tobs<br/>"
        f"Temperature analysis provides MIN,MAX and AVG Tem "
        f"Temperature analysis from the start date(yyyy-mm-dd): /api/v1.0/<start><br/>"
        f"Temperatures analysis from start to end date(yyyy-mm-dd): /api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query all prcp
    results = session.query(measurement.date, measurement.prcp).\
                order_by(measurement.date).all()
    session.close()

    # Create a dictionary from the row data and append to a list of prcp data
    precipitation = []
    
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def all_stations():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station names"""
    # Query all stations
    all_stations = session.query(station.station, station.name).all()

    session.close()
    
    # Convert this data into a list 
    stationlist = list(np.ravel(all_stations))

    return jsonify(stationlist)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all tobs
    tempdata = session.query(measurement.station,measurement.date,measurement.tobs).\
                filter(measurement.station == "USC00519281").\
                filter(measurement.date >= "2016-08-23").all()
    session.close()

    # Convert this data into a list 
    templist = list(np.ravel(tempdata))

    return jsonify(templist)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #convert format
    startdt = dt.datetime.strptime(start,"%Y-%m-%d").date()

    # Query all data
    start_data = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
                filter(measurement.date >= startdt).all()
    session.close()

    # Convert this data into a list 
    start_list = list(np.ravel(start_data))

    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #convert format
    startdt = dt.datetime.strptime(start, "%Y-%m-%d").date()

    enddt = dt.datetime.strptime(end, "%Y-%m-%d").date()

    # Query all data
    start_end_data = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
                filter(measurement.date >= startdt).\
                filter(measurement.date <= enddt).all()
    session.close()

    # Convert this data into a list  
    start_end_list = list(np.ravel(start_end_data))

    return jsonify(start_end_list)
   

if __name__ == '__main__':
    app.run(debug=True)
