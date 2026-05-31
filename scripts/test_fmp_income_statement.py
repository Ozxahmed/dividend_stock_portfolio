from src.config import load_env_variable
import requests
import pandas as pd

# load fmp api key
api_key = load_env_variable("FMP_API_KEY")

# set ticker
symbol = "AAPL"

# api endpoint url
endpoint_url = "https://financialmodelingprep.com/stable/income-statement"

# api params
params = {
    "symbol": symbol,
    "apikey": api_key,
}

# api call
response = requests.get(url=endpoint_url, params=params, timeout=30)

# mask api key
safe_url = response.url.replace(api_key, "REDACTED")

# view api request
print(safe_url)
print(response.status_code)
print(response.text[:1000])

# stop script if API call fails
response.raise_for_status()

# convert response to python json object
data = response.json()

print(type(data))
print(len(data))
print(data[0])