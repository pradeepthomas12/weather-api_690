import os
import dask.dataframe as daskDataFrame
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

def create_engine_and_tables(database_name):
    engine = create_engine(f'sqlite:///{database_name}', echo=True)
    Base.metadata.create_all(bind=engine)
    return engine

def read_data(filepath):
    data = daskDataFrame.read_csv(filepath, sep="\t", header=None,
                                  names=["date", "max_temp", "min_temp", "precipitation"])
    data["Station_ID"] = os.path.basename(filepath)[:11]
    return data

def clean_data(data):
    # Remove any rows with missing temperature or precipitation data
    result = data[(data['max_temp'] != -9999) |
                  (data['min_temp'] != -9999) | (data['precipitation'] != -9999)]

    # Group the data by station ID and year, and compute the mean maximum and minimum temperatures
    # and the total accumulated precipitation for each group
    result = result.groupby(['Station_ID', data['date'].map(str).str[:4]]).agg({
        'max_temp': 'mean',
        'min_temp': 'mean',
        'precipitation': 'sum'
    }).reset_index()

    # Rename the columns to more descriptive names
    heading = {'max_temp': 'AvgMaxtemp', 'min_temp': 'AvgMintemp',
               'precipitation': 'TotalAccPrecipitation'}
    result.rename(columns=heading, inplace=True)
    return result

def write_to_database(engine, data, result):
    session = engine.raw_connection()
    # Write the weather data to a table in the database
    data.to_sql("weather_records", session, if_exists="replace",
                    index=True, index_label='id')
    result.to_sql("weather_stats", session, if_exists="replace",
                      index=True, index_label='id')
    session.commit()

def data_ingestion(database_name, directory):
    engine = create_engine_and_tables(database_name)
    dataframes = []
    for file_data in os.listdir(directory):
        if file_data.endswith(".txt"):
            filepath = os.path.join(directory, file_data)
            data = read_data(filepath)
            dataframes.append(data)
    data = daskDataFrame.concat(dataframes).compute().reset_index(drop=True)
    result = clean_data(data)
    write_to_database(engine, data, result)
    
# Call the data_ingestion function with the specified directory and database name
data_ingestion('weather.db', '../wx_data')