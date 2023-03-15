from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base

D_Base = declarative_base()
db_engine = create_engine('sqlite:///weather.db', echo=True)
D_Base.metadata.create_all(bind=db_engine)

app = FastAPI()




@app.get("/api/weather/stats")
def read_weather_stats(
    year_of_date: str = Query(None),
    id_of_station: str = Query(None),
    pagination: int = Query(1),
    size_of_query: int = Query(10),
):
    offset_value = (pagination - 1) * size_of_query
    db_query = "SELECT * FROM weather_stats"
    filter_params = []
    if year_of_date:
        filter_params.append(f"Date == '{year_of_date}'")
    if id_of_station:
        filter_params.append(f"Station_ID== '{id_of_station}'")
    if filter_params:
        db_query += " WHERE " + " AND ".join(filter_params)
    db_query += f" LIMIT {size_of_query} OFFSET {offset_value}"
    with db_engine.connect() as conn:
        result = conn.execute(text(db_query))
        rows = result.fetchall()
        if not rows:
            raise HTTPException(
                status_code=404, detail="No data found for the specified dates"
            )
        weather_data = []
        for row in rows:
            weather_data.append(
                {
                    "id_of_station": row[1],
                    "date": row[2],
                    "avg_max_temp": row[3],
                    "avg_min_temp": row[4],
                    "total_acc_precipitation": row[5],
                }
            )
        return weather_data


@app.get("/api/weather/")
def read_weather_records(
    date: str = Query(None),
    id_of_station: str = Query(None),
    pagination: int = Query(1),
    size_of_query: int = Query(10),
):
    offset_value = (pagination - 1) * size_of_query
    db_query = "SELECT * FROM weather_records"
    filter_params = []
    if date:
        filter_params.append(f"Date == '{date}'")
    if id_of_station:
        filter_params.append(f"Station_ID== '{id_of_station}'")
    if filter_params:
        db_query += " WHERE " + " AND ".join(filter_params)
    db_query += f" LIMIT {size_of_query} OFFSET {offset_value}"
    with db_engine.connect() as conn:
        result = conn.execute(text(db_query))
        rows = result.fetchall()
        if not rows:
            raise HTTPException(
                status_code=404, detail="No data found for the specified dates"
            )
        weather_data = []
        for row in rows:
            weather_data.append(
                {
                    "id_of_station": row[5],
                    "date": row[1],
                    "max_temp": row[2],
                    "min_temp": row[3],
                    "precipitaion": row[4],
                }
            )
        return weather_data



