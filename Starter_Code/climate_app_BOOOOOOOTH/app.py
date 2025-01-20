import pandas as pd
from flask import Flask, jsonify
from sql_helper import SQLHelper


#################################################
# Flask Setup
#################################################
app = Flask(__name__)
sqlHelper = SQLHelper()


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/precipitation2<br/>"
        f"/api/v1.0/stations<br/>"
        f"<a href='/api/v1.0/temperature' target='_blank'>/api/v1.0/temperature</a><br/>"
        f"<a href='/api/v1.0/2017-01-01' target='_blank'>/api/v1.0/2017-01-01</a><br/>"
        f"<a href='/api/v1.0/2017-01-01/2017-01-31' target='_blank'>/api/v1.0/2017-01-01/2017-01-31</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Execute queries
    df = sqlHelper.queryPrecipitationORM()

    # Turn DataFrame into List of Dictionary
    data = df.to_dict(orient="records")
    return jsonify(data)

@app.route("/api/v1.0/precipitation2")
def precipitation2():
    # Execute Query
    df = sqlHelper.queryPrecipitationSQL()

    # Turn DataFrame into List of Dictionary
    data = df.to_dict(orient="records")
    return jsonify(data)

@app.route("/api/v1.0/stations")
def stations():
    # Execute Query
    df = sqlHelper.queryStationsSQL()

    # Turn DataFrame into List of Dictionary
    data = df.to_dict(orient="records")
    return jsonify(data)

@app.route("/api/v1.0/stations2")
def stations2():
    # Execute Query
    df = sqlHelper.queryStationsORM()

    # Turn DataFrame into List of Dictionary
    data = df.to_dict(orient="records")
    return jsonify(data)

@app.route("/api/v1.0/temperature")
def temperature():
    # Execute Query
    df = sqlHelper.queryTemperatureSQL()

    # Turn DataFrame into List of Dictionary
    data = df.to_dict(orient="records")
    return jsonify(data)

@app.route("/api/v1.0/temperature2")
def temperature2():
    # Execute Query
    df = sqlHelper.queryTemperatureORM()

    # Turn DataFrame into List of Dictionary
    data = df.to_dict(orient="records")
    return jsonify(data)

@app.route("/api/v1.0/<start>")
def tstats1(start):
    # Execute Query
    df = sqlHelper.queryTStatsSQL(start)

    # Turn DataFrame into List of Dictionary
    data = df.to_dict(orient="records")
    return jsonify(data)

@app.route("/api/v1.0/orm/<start>")
def tstats2(start):
    # Execute Query
    df = sqlHelper.queryTStatsORM(start)

    # Turn DataFrame into List of Dictionary
    data = df.to_dict(orient="records")
    return jsonify(data)

@app.route("/api/v1.0/<start>/<end>")
def tstats_startend1(start, end):
    # Execute Query
    df = sqlHelper.queryTStats_StartEndSQL(start, end)

    # Turn DataFrame into List of Dictionary
    data = df.to_dict(orient="records")
    return jsonify(data)

@app.route("/api/v1.0/orm/<start>/<end>")
def tstats_startend2(start, end):
    # Execute Query
    df = sqlHelper.queryTStats_StartEndORM(start, end)

    # Turn DataFrame into List of Dictionary
    data = df.to_dict(orient="records")
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
