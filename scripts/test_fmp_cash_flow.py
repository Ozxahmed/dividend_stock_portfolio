import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# load env
env_path = Path("/Users/oz/Documents/personal/education/dividend_stock_portfolio/.env")

print(env_path.exists())

load_dotenv(dotenv_path=env_path)

# validate API key
api_key = os.getenv("FMP_API_KEY")

if not api_key:
    raise ValueError("Missing FMP_API_KEY in .env file")

print("FMP API key loaded successfully")

# set ticker
symbol = "AAPL"

# build fmp url
url = "https://financialmodelingprep.com/stable/cash-flow-statement"

params = {
    "symbol": symbol,
    "apikey": api_key,
}

# api request
response = requests.get(url, params=params, timeout=30)

# hide api key
safe_url = (
    response.url.replace(api_key, "REDACTED") if response.url else "URL not available"
)

# view api request
print("Final URL:")
print(safe_url)

print("\nStatus code:")
print(response.status_code)

print("\nResponse Preview:")
print(response.text[:1000])

response.raise_for_status()

# convert response to python json object
data = response.json()

if not data:
    raise ValueError("No cash flow data returned from FMP")

# calculate fcf payout ratio
latest_record = data[0]

dividends_paid = latest_record["netDividendsPaid"]
free_cash_flow = latest_record["freeCashFlow"]

if free_cash_flow <= 0:
    raise ValueError(
        "Free cash flow is zero or negative; FCF payout ratio is not meaningful"
    )

fcf_payout_ratio = abs(dividends_paid) / free_cash_flow
fcf_payout_ratio_pct = fcf_payout_ratio * 100

print("\nFCF payout ratio:")
print(f"{fcf_payout_ratio_pct:.2f}%")
