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

# stop script if insufficient data
if len(data) == 1:
    raise ValueError("Insufficient data to calculate revenue growth CAGR")

# convert list of records to df
df = pd.DataFrame(data)

# display df
df.head()

# keep cols needed to calculate rev growth CAGR
revenue_df = df[["symbol", "date", "fiscalYear", "period", "revenue"]].copy()

# confirm fiscalYear and revenue are numeric
revenue_df['fiscalYear'] = pd.to_numeric(revenue_df['fiscalYear'], errors="coerce")
revenue_df['revenue'] = pd.to_numeric(revenue_df['revenue'], errors="coerce")

# sort oldest to newest
revenue_df = revenue_df.sort_values('fiscalYear')

# calc rev growth CAGR
start_row = revenue_df.iloc[0]
end_row = revenue_df.iloc[-1]

start_year = start_row['fiscalYear']
end_year = end_row['fiscalYear']

start_revenue = start_row['revenue']
end_revenue = end_row['revenue']

number_of_years = end_year - start_year

rev_growth_cagr = (end_revenue / start_revenue) ** (1 / number_of_years) - 1
rev_growth_cagr_percent = round(rev_growth_cagr * 100, 2)

print(f"Start year: {start_year}")
print(f"End year: {end_year}")
print(f"Start revenue: {start_revenue}")
print(f"End revenue: {end_revenue}")
print(f"Number of years: {number_of_years}")
print(f"Revenue CAGR: {rev_growth_cagr:.4f}")
print(f"Revenue CAGR %: {rev_growth_cagr_percent:.2f}%")