import json
import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


def get_required_env_var(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ValueError(f"Missing required environment variable: {name}")

    return value


def save_json(data, filepath: str) -> None:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved: {path}")


def print_safe_response(response, api_key: str) -> None:
    safe_url = response.url.replace(api_key, "REDACTED")

    print("Final URL without key:")
    print(safe_url)

    print("\nStatus code:")
    print(response.status_code)

    print("\nResponse preview:")
    print(response.text[:1500])


def main():
    load_dotenv()

    api_key = get_required_env_var("FMP_API_KEY")
    symbol = "AAPL"

    url = "https://financialmodelingprep.com/stable/dividends"

    params = {
        "symbol": symbol,
        "apikey": api_key,
    }

    print(f"Fetching FMP dividend history for {symbol}...")

    response = requests.get(url, params=params, timeout=30)

    print_safe_response(response, api_key)

    response.raise_for_status()

    data = response.json()

    today = datetime.now().strftime("%Y-%m-%d")
    save_json(data, f"data/raw/fmp/dividends_{symbol}_{today}.json")

    print("\nParsed response type:")
    print(type(data))

    if isinstance(data, list):
        print(f"\nNumber of records: {len(data)}")
        print("\nFirst record:")
        print(json.dumps(data[0], indent=2) if data else "No records returned")


if __name__ == "__main__":
    main()
