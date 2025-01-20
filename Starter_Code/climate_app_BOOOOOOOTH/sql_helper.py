from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, func

import pandas as pd

# Define the SQLHelper Class
# PURPOSE: Deal with all of the database logic

class SQLHelper():

    # Initialize PARAMETERS/VARIABLES

    #################################################
    # Database Setup
    #################################################
    def __init__(self):
        self.engine = create_engine("sqlite:///hawaii.sqlite")
        self.Station = self.createStation()
        self.Measurement = self.createMeasurement()

    # Used for ORM
    def createStation(self):
        # Reflect an existing database into a new model
        Base = automap_base()

        # reflect the tables
        Base.prepare(autoload_with=self.engine)

        # Save reference to the table
        Station = Base.classes.station
        return(Station)

    def createMeasurement(self):
        # Reflect an existing database into a new model
        Base = automap_base()

        # reflect the tables
        Base.prepare(autoload_with=self.engine)

        # Save reference to the table
        Measurement = Base.classes.measurement
        return(Measurement)

    #################################################################

    def queryPrecipitationORM(self):
        # Create our session (link) from Python to the DB
        session = Session(self.engine)

        # Query all precipitation
        rows = session.query(self.Measurement.id, self.Measurement.station, self.Measurement.date, self.Measurement.prcp).filter(self.Measurement.date >= '2016-08-23').order_by(self.Measurement.date).all()

        # Create the dataframe
        df = pd.DataFrame(rows)

        # Close the Session
        session.close()
        return(df)

    def queryPrecipitationSQL(self):
        # Create our session (link) from Python to the DB
        conn = self.engine.connect() # Raw SQL/Pandas

        # Define Query
        query = text("""SELECT
                    id,
                    station,
                    date,
                    prcp
                FROM
                    measurement
                WHERE
                    date >= '2016-08-23'
                ORDER BY
                    date;""")
        df = pd.read_sql(query, con=conn)

        # Close the connection
        conn.close()
        return(df)

    def queryStationsSQL(self):
        # Create our session (link) from Python to the DB
        conn = self.engine.connect() # Raw SQL/Pandas

        # Define Query
        query = text("""SELECT
                    station,
                    name,
                    latitude,
                     longitude,
                     elevation
                FROM
                    station
                ORDER BY
                    station;""")
        df = pd.read_sql(query, con=conn)

        # Close the connection
        conn.close()
        return(df)

    def queryStationsORM(self):
        # Create our session (link) from Python to the DB
        session = Session(self.engine)

        # Query all precipitation
        rows = session.query(self.Station.station, self.Station.name, self.Station.latitude, self.Station.longitude, self.Station.elevation).order_by(self.Station.station).all()

        # Create the dataframe
        df = pd.DataFrame(rows)

        # Close the Session
        session.close()
        return(df)

    def queryTemperatureSQL(self):
        # Create our session (link) from Python to the DB
        conn = self.engine.connect() # Raw SQL/Pandas

        # Define Query
        query = text("""SELECT
                    id,
                    station,
                    date,
                    tobs
                FROM
                    measurement
                WHERE
                    station = 'USC00519281'
                    and date >= '2016-08-23'
                ORDER BY
                    date;""")
        df = pd.read_sql(query, con=conn)

        # Close the connection
        conn.close()
        return(df)

    def queryTemperatureORM(self):
        # Create our session (link) from Python to the DB
        session = Session(self.engine)

        # Query all precipitation
        rows = session.query(self.Measurement.id, self.Measurement.station, self.Measurement.date, self.Measurement.tobs).filter(self.Measurement.station == 'USC00519281').filter(self.Measurement.date >= '2016-08-23').order_by(self.Measurement.date).all()

        # Create the dataframe
        df = pd.DataFrame(rows)

        # Close the Session
        session.close()
        return(df)

    def queryTStatsSQL(self, start):
        # Create our session (link) from Python to the DB
        conn = self.engine.connect() # Raw SQL/Pandas

        # Define Query
        query = text(f"""SELECT
                    min(tobs) as min_tobs,
                    max(tobs) as max_tobs,
                    avg(tobs) as avg_tobs
                FROM
                    measurement
                WHERE
                    date >= '{start}';""")
        print(query)
        df = pd.read_sql(query, con=conn)

        # Close the connection
        conn.close()
        return(df)

    def queryTStatsORM(self, start):
        # Create our session (link) from Python to the DB
        session = Session(self.engine)

        # Query all precipitation
        rows = session.query(func.min(self.Measurement.tobs).label('min_tobs'), func.max(self.Measurement.tobs).label('max_tobs'), func.avg(self.Measurement.tobs).label('avg_tobs')).filter(self.Measurement.date >= start).all()

        # Create the dataframe
        df = pd.DataFrame(rows)

        # Close the Session
        session.close()
        return(df)

    def queryTStats_StartEndSQL(self, start, end):
        # Create our session (link) from Python to the DB
        conn = self.engine.connect() # Raw SQL/Pandas

        # Define Query
        query = text(f"""SELECT
                    min(tobs) as min_tobs,
                    max(tobs) as max_tobs,
                    avg(tobs) as avg_tobs
                FROM
                    measurement
                WHERE
                    date >= '{start}'
                    AND date <= '{end}';""")
        print(query)
        df = pd.read_sql(query, con=conn)

        # Close the connection
        conn.close()
        return(df)


    def queryTStats_StartEndORM(self, start, end):
        # Create our session (link) from Python to the DB
        session = Session(self.engine)

        # Query all precipitation
        rows =  session.query(func.min(self.Measurement.tobs).label('min_tobs'), func.max(self.Measurement.tobs).label('max_tobs'), func.avg(self.Measurement.tobs).label('avg_tobs')).filter(self.Measurement.date >= start).filter(self.Measurement.date <= end).all()

        # Create the dataframe
        df = pd.DataFrame(rows)

        # Close the Session
        session.close()
        return(df)
