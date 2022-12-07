# Import dependencies and applications
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

# Reflecting database and tables
Base = automap_base()
Base.prepare(engine)

# Save table references
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<b> Welcome to to the Hawaiian Climate API.<b><br/>"
        f"</br>"
        f"</br>"
        f"Available Routes:<br/>"
        f"Daily Precipitation Totals <a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation<a><br/>"
        f"Weather Stations <a href=\"/api/v1.0/stations\">/api/v1.0/stations<a><br/>"
        f"Temperature Observations <a href=\"/api/v1.0/tobs\">/api/v1.0/tobs<a><br/>"  
        f"</br>"
        f"Min, Max, Average temperatures by date ranges; please enter date values as the format of YYYY-MM-DD for the start dates and/or stop dates.<br/>"
        f"Start Date Calculations by start date <a href=\"/api/v1.0/start/<start_date>\">/api/v1.0/start/<start_date><a><br/>"
        f"Date Range Calculations by date range as start date then stop date <a href=\"/api/v1.0/<start_date>/<stop_date>\">/api/v1.0/<start_date>/<stop_date><a><br/>"
    )

# Precipitation route
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Retrieve the last 12 months of precipitation data"""
    # Find last date
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Query all dates and precipitation
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_date).all()

    session.close()

    # Create a dictionary and append
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

# Stations route
@app.route('/api/v1.0/stations')

def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the observation stations"""
    # Query all stations
    results = session.query(Station.station,Station.name).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, name in results:
        all_stations_dict = {}
        all_stations_dict["station"] = station
        all_stations_dict["name"] = name
        all_stations.append(all_stations_dict)

    return jsonify(all_stations)

# Tobs route
@app.route('/api/v1.0/tobs')
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #find last date in database from Measurements
    last_day = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = (dt.datetime.strptime(last_day[0], "%Y-%m-%d") - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    #find the most active station in database from Measurements
    active_station = session.query(Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()

    # Query the dates and temperature observations of the most active station for the last year of data 
    results = session.query(Measurement.tobs).filter(Measurement.date >= query_date).\
filter(Measurement.station == active_station[0]).all()

    session.close()

    # Convert list of tuples into normal list
    info_active_station = list(np.ravel(results))

    return jsonify(info_active_station)

#Start route 
@app.route("/api/v1.0/start/<start_date>")
def start(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return of the minimum, maximum, and average temperates for start date to the end of the dataset."""
    # Query of min, max and avg temperature for all dates greater than and equal to the given date.
    start_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date>=start_date).all()
              
    session.close()

    start_query2 = list(np.ravel(start_query))

    return jsonify(start_query2)
   
# Range route
@app.route('/api/v1.0/<start_date>/<stop_date>')
def start_end_date(start_date, stop_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return of the minimum, maximum, and average temperates for range of dates."""
    # Query of min, max and avg temperature for dates between given start and end date.
    range_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date>=start_date).filter(Measurement.date<=stop_date).all()
              
    session.close()

    range_query2 = list(np.ravel(range_query))

    return jsonify(range_query2)

    
if __name__ == '__main__':
    app.run(debug=True)  