from flask import Flask
from flask import jsonify, render_template, render_template_string
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from statistics import mean

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


app = Flask(__name__)


@app.route('/')
def home():
    route1 = '/api/v1.0/precipitation'
    route2 = '/api/v1.0/stations'
    route3 = '/api/v1.0/temperature_observations'
    route4 = '/api/v1.0/<start>'
    route5 = '/api/v1.0/<start>/<end>'

    return render_template('index.html', route1=route1,
                                        route2=route2,
                                        route3=route3,
                                        route4=route4,
                                        route5=route5)

@app.route('/api/v1.0/precipitation')
def precipitation():
    measurement = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    dicts = [q._asdict() for q in measurement]
    data_dict = []
    for d in dicts:
        if d['prcp'] != 0 and d['prcp'] != None:
            data_dict.append({d['date'] : d['prcp']})

    return jsonify(data_dict)
    
@app.route('/api/v1.0/stations')
def stations():
    stations = session.query(Station.station, 
                                Station.name, 
                                Station.latitude, 
                                Station.longitude, 
                                Station.elevation).all()
    dicts = [q._asdict() for q in stations]
    return jsonify(dicts)

@app.route('/api/v1.0/temperature_observations')
def temperature():
    measurement = session.query(Measurement.date, Measurement.tobs).all()
    session.close()
    dicts = [q._asdict() for q in measurement]


    return jsonify(dicts[-365:])
@app.route('/api/v1.0/<start>')
def weather_check(start):
    measurement = session.query(Measurement.date, Measurement.tobs).all()
    session.close()
    dicts = [q._asdict() for q in measurement]
    index = 0
    for i in range(len(dicts)):
        if dicts[i]['date'] == start:
            index = int(i)
    
    current = dicts[index:]
    tobs_list = []
    for c in current:
        tobs_list.append(c['tobs'])


    summary_dict = {
        "T-MIN" : min(tobs_list),
        "T-MAX" : max(tobs_list),
        "T_AVG" : mean(tobs_list),
    }
    return jsonify(summary_dict)

@app.route('/api/v1.0/<start>/<end>')
def weather_check2(start, end):
    measurement = session.query(Measurement.date, Measurement.tobs).all()
    session.close()
    dicts = [q._asdict() for q in measurement]
    start_index = 0
    end_index = 0

    for i in range(len(dicts)):
        if dicts[i]['date'] == start:
            start_index = int(i)
        if dicts[i]['date'] == end:
            end_index = int(i)
    
    current = dicts[start_index:end_index]
    tobs_list = []
    for c in current:
        tobs_list.append(c['tobs'])


    summary_dict = {
        "T-MIN" : min(tobs_list),
        "T-MAX" : max(tobs_list),
        "T_AVG" : mean(tobs_list),
    }
    return jsonify(summary_dict)

app.run(debug=True)