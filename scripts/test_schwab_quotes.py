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

    symbols = ["AAPL", "MSFT", "JNJ", "KO", "PG", "SCHD", "VYM", "O"]

    print(f"Fetching quotes for: {symbols}")

    response = client.get_quotes(symbols)
    response.raise_for_status()

    data = response.json()

    today = datetime.now().strftime("%Y-%m-%d")
    save_json(data, f"data/raw/schwab/quotes_{today}.json")

    print("\nQuote response top-level keys:")
    print(data.keys())

    print("\nSample output:")
    for symbol in symbols:
        if symbol in data:
            quote_data = data[symbol]
            print(f"\n--- {symbol} ---")
            print(json.dumps(quote_data, indent=2)[:1500])
        else:
            print(f"\n--- {symbol} not found in response ---")


if __name__ == "__main__":
    main()
