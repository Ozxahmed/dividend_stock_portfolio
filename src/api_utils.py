import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_fmp_api_data(fmp_endpoint_url: str, ticker: str, api_key: str | None = None):
    # if api_key is not passed in, get it from .env
    if api_key is None:
        api_key = os.getenv("FMP_API_KEY")

    # validate api_key
    if not api_key:
        raise ValueError("Missing FMP_API_KEY. Check your .env file or pass api_key manually.")

    # set api request params
    params = {
        "symbol": ticker,
        "apikey": api_key,
    }

    # make api request using params; timeout after 30s
    r = requests.get(fmp_endpoint_url, params=params, timeout=30)

    # create safe_url
    safe_url = r.url.replace(api_key, "REDACTED")

    # print request info
    print(f"Request URL: {safe_url}")
    print(f"Status code: {r.status_code}")

    # if status code != 200 -> print message and quit function
    if r.status_code != 200:
        print(f"Error fetching data. Status code: {r.status_code}")
        return None

    # convert to json
    data = r.json()

    # print dtype
    print(f"Data type: {type(data)}")
    print(f"Number of records fetched: {len(data)}")

    # preview depends on whether data is list or dict
    if isinstance(data, list):
        print(f"Limited data preview: {data[:1]}")

    elif isinstance(data, dict):
        print(f"Limited keys preview: {list(data.keys())[:5]}")
        print(f"Limited data preview: {dict(list(data.items())[:5])}")

    return data