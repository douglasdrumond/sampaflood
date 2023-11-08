import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"


def get_weather_data(latitude=(-23.6314278), longitude=(-46.6207165), append_data=None):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": "2013-01-01",
        "end_date": "2022-12-31",
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "temperature_2m_mean",
            "precipitation_sum",
            "precipitation_hours"
        ],
        "timezone": "America/Sao_Paulo"
    }

    responses = openmeteo.weather_api(url, params=params)

    accumulated_df = pd.DataFrame(data=None)

    # Process first location. Add a for-loop for multiple locations or weather models
    for i, response in enumerate(responses):
        print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
        daily_temperature_2m_mean = daily.Variables(2).ValuesAsNumpy()
        daily_precipitation_sum = daily.Variables(3).ValuesAsNumpy()
        daily_precipitation_hours = daily.Variables(4).ValuesAsNumpy()

        daily_data = {
            "date": pd.date_range(
                start=pd.to_datetime(daily.Time(), unit="s").date(),
                end=pd.to_datetime(daily.TimeEnd(), unit="s").date(),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left"
            ),
            "temperature_2m_max": daily_temperature_2m_max,
            "temperature_2m_min": daily_temperature_2m_min,
            "temperature_2m_mean": daily_temperature_2m_mean,
            "precipitation_sum": daily_precipitation_sum,
            "precipitation_hours": daily_precipitation_hours
        }

        daily_dataframe = pd.DataFrame(data=daily_data)
        daily_dataframe["latitude"] = latitude[i]
        daily_dataframe["longitude"] = longitude[i]
        if append_data:
            abbreviation = append_data["abbreviation"][i]
            district_name = append_data["district_name"][i]
            daily_dataframe["sigla"] = abbreviation
            daily_dataframe["ds_name"] = district_name

        accumulated_df = pd.concat([accumulated_df, daily_dataframe])
    return accumulated_df


if __name__ == "__main__":
    df = get_weather_data()
    print(df)
