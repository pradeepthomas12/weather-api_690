from fastapi.testclient import TestClient
from run_app import app

client = TestClient(app)

def test_get_weather_records_no_filter():
    """Test that the API returns all weather records when no filters are applied"""
    # Arrange

    # Act
    response = client.get("/api/weather/")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_get_weather_records_filter_by_date():
    """Test that the API returns weather records filtered by date"""
    # Arrange

    # Act
    response = client.get("/api/weather/?date=19860101")

    # Assert
    assert response.status_code == 200
    assert response.json()[0]["date"] == 19860101


def test_get_weather_records_filter_by_station_id():
    """Test that the API returns weather records filtered by station ID"""
    # Arrange

    # Act
    response = client.get("/api/weather/?id_of_station=USC00110187")

    # Assert
    assert response.status_code == 200
    assert all(data["id_of_station"] == "USC00110187" for data in response.json())


def test_get_weather_stats_no_filter():
    """Test that the API returns weather stats for all records when no filters are applied"""
    # Arrange

    # Act
    response = client.get("/api/weather/stats")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_get_weather_stats_filter_by_year():
    """Test that the API returns weather stats filtered by year"""
    # Arrange

    # Act
    response = client.get("/api/weather/stats?year_of_date=1986")

    # Assert
    assert response.status_code == 200
    assert all(data["date"].startswith("1986") for data in response.json())


def test_get_weather_stats_filter_by_station_id():
    """Test that the API returns weather stats filtered by station ID"""
    # Arrange

    # Act
    response = client.get("/api/weather/stats?id_of_station=USC00110187")

    # Assert
    assert response.status_code == 200
    assert response.json()[0]["id_of_station"] == "USC00110187"
