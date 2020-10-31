#Imports
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Temperatures from the start date(yyyy-mm-dd): /api/v1.0/<start><br/>"
        f"Temperatures from start to end date(yyyy-mm-dd): /api/v1.0/<start><end><br/>"
    )

##### fix below
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
    results = session.query(station.station, station.name).all()

    session.close()

   # Create a dictionary from the row data and append to a list of station data
    
    all_stations = []
    
    for station,name in results:
        station_dict = {}
        station_dict[station] = name
        all_stations.append(station_dict)

    return jsonify(all_stations)

    

if __name__ == '__main__':
    app.run(debug=True)
