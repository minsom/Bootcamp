import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite",
        connect_args={'check_same_thread':False},
                    poolclass=StaticPool)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Calculate the date 1 year ago from the last data point in the database
recent_record=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
print(recent_record)
print(type(recent_record))

# Change the last_date's datatype to string and extract only the date to convert it into
recent_record_str=str(recent_record).split("'")[1]
print(recent_record_str)
print(type(recent_record_str))

# Determine the date point one year from the most recent date
recent_date=dt.datetime.strptime(recent_record_str,"%Y-%m-%d")
last=recent_date-dt.timedelta(days=364)
print(last)
print(type(last))
last_date=last.strftime("%Y-%m-%d")#back to string
print(last_date)





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
        f"<hr>"
        f"* Dates and Precipation from a Year from the Last Data Point<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<hr>"

        f"* List of Hawaiian Weather Stations<br/>"
        f"/api/v1.0/stations<br/>"
        f"<hr>"

        f"* List of Temperature Observations from a Year from the Last Data Point (by Stations and Dates)<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<hr>"

        f"* Minimum, Average and Maximum Temperatues for a Given Date<br/>"
        f"Date should be entered as YYYY-MM-DD<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"   
        f"<hr>"

        f"* Minimum, Average and Maximum Temperatues over for a Start Date and End Date Range<br/>"
        f"Date Range should be entered as YYYY-MM-DD/YYYY-MM-DD (Start/End dates respectively)<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD<br/>"
        f"<hr>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= last_date).\
    order_by(Measurement.date).all()

    precipitation = []

    for p in prcp:
        precipitation_dict = {}
        precipitation_dict["Date"] = p.date
        precipitation_dict["Precipitation"] = p.prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name).all()

    stations = list(np.ravel(results))

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():

    tobs = session.query(Station.name, Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= last_date).\
    order_by(Station.name, Measurement.date).all()

    temps = []
    for t in tobs:
        temps_dict = {}
        temps_dict["Name"] = t.name
        temps_dict["Date"] = t.date
        temps_dict["Temperature"] = t.tobs
        temps.append(temps_dict)

    return jsonify(temps)


@app.route("/api/v1.0/<start_date>")
def calc_temps(start_date):

    start = dt.datetime.strptime(start_date, '%Y-%m-%d')

    start_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all() 

    temps_start = list(np.ravel(start_temp)) 

    return jsonify(temps_start)
    
    
 
@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps_end(start_date, end_date):

    start = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end = dt.datetime.strptime(end_date, '%Y-%m-%d')    
    
    start_end_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()

    temps_end = list(np.ravel(start_end_temp)) 

    return jsonify(temps_end)


if __name__ == "__main__":
    app.run(debug=True)