import requests
import pandas as pd
from src.common.config import (
    SOURCE_B_RAW_PATH,
    MARKET_COORDINATES,
    RAINFALL_START_DATE,
    RAINFALL_END_DATE,
    RAINFALL_URL
)
def get_market_rainfall(market_name, latitude, longitude, start_date=RAINFALL_START_DATE, end_date=RAINFALL_END_DATE):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "timezone" : "auto",
        "daily": "precipitation_sum", 
    }
    response = requests.get(RAINFALL_URL, params=params, timeout = 10)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to get rainfall data for {market_name}. Status code: {response.status_code}")
    daily = response.json()["daily"]
    return pd.DataFrame({
        "date": daily["time"],
        "rainfall": daily["precipitation_sum"],
        "market":market_name,
    }) 
    return df

def ingest_source_b():
    all_frames = []

    for market_name,(lat, lon) in MARKET_COORDINATES.items():
        print(f"Fetching rainfall for {market_name}...")
        df = get_market_rainfall(market_name,lat,lon)
        all_frames.append(df)

    result = pd.concat(all_frames, ignore_index = True)
    return result 


if __name__ =="__main__":
    df = ingest_source_b()
    print("\nShape:", df.shape)
    print(df.head(10))
    print("\nMarkets:")
    print(df["market"].value_counts()) 


##get the details for the other markets
