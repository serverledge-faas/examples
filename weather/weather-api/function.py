import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"

def handler (params, context):
    try:
        latitude = float(params["latitude"])
        longitude = float(params["longitude"])
    except:
        # TODO: error
        return {}


    api_params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["rain_sum", "temperature_2m_max", "temperature_2m_min"],
        "current": "temperature_2m",
        "forecast_days": 3,
        #"bounding_box": "-90,-180,90,180",
    }
    responses = openmeteo.weather_api(url, params=api_params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    print(response)

    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

    # Process current data. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()

    print(f"\nCurrent time: {current.Time()}")
    print(f"Current temperature_2m: {current_temperature_2m}")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_rain_sum = daily.Variables(0).ValuesAsNumpy().tolist()
    daily_max_temp = daily.Variables(1).ValuesAsNumpy().tolist()
    daily_min_temp = daily.Variables(2).ValuesAsNumpy().tolist()

    #daily_data = {"date": pd.date_range(
    #    start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
    #    end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
    #    freq = pd.Timedelta(seconds = daily.Interval()),
    #    inclusive = "left"
    #)}

    #daily_data["weather_code"] = daily_weather_code
    #daily_data["rain_sum"] = daily_rain_sum

    #daily_dataframe = pd.DataFrame(data = daily_data)
    #print("\nDaily data\n", daily_dataframe)

    response = {}
    if "gemini_api_key" in params:
        response["gemini_api_key"] = params["gemini_api_key"]
    response["current_temperature"] = current_temperature_2m
    response["daily_max_temp"] = daily_max_temp
    response["daily_min_temp"] = daily_min_temp
    response["daily_rain_sum"] = daily_rain_sum

    return response
