import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from schwab import auth  # type: ignore


def get_client():
    load_dotenv()

    app_key = os.getenv("SCHWAB_APP_KEY")
    app_secret = os.getenv("SCHWAB_APP_SECRET")
    callback_url = os.getenv("SCHWAB_CALLBACK_URL")
    token_path = os.getenv("SCHWAB_TOKEN_PATH", ".secrets/schwab_token.json")

    return auth.easy_client(
        api_key=app_key,
        app_secret=app_secret,
        callback_url=callback_url,
        token_path=token_path,
    )


def save_json(data, filepath):
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved: {filepath}")


def main():
    client = get_client()

    symbol = "AAPL"

    print(f"Fetching daily price history for {symbol}...")

    response = client.get_price_history_every_day(symbol)
    response.raise_for_status()

    data = response.json()

    today = datetime.now().strftime("%Y-%m-%d")
    save_json(data, f"data/raw/schwab/price_history_{symbol}_{today}.json")

    print("\nTop-level keys:")
    print(data.keys())

    candles = data.get("candles", [])

    print(f"\nNumber of candles returned: {len(candles)}")

    print("\nFirst 3 candles:")
    for candle in candles[:3]:
        print(candle)

    print("\nLast 3 candles:")
    for candle in candles[-3:]:
        print(candle)


if __name__ == "__main__":
    main()
