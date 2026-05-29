import json
from pathlib import Path

import pandas as pd


def load_latest_quotes_file() -> dict:
    files = sorted(Path("data/raw/schwab").glob("quotes_*.json"))

    if not files:
        raise FileNotFoundError("No Schwab quote files found in data/raw/schwab")

    latest_file = files[-1]
    print(f"Loading: {latest_file}")

    with open(latest_file, "r") as f:
        return json.load(f)


def calculate_payout_ratios(quotes: dict) -> pd.DataFrame:
    rows = []

    for symbol, quote_data in quotes.items():
        fundamental = quote_data.get("fundamental", {})

        annual_dividend = fundamental.get("divAmount")
        eps = fundamental.get("eps")

        if annual_dividend is None or eps is None:
            payout_ratio = None
            payout_ratio_pct = None
        elif eps <= 0:
            payout_ratio = None
            payout_ratio_pct = None
        else:
            payout_ratio = annual_dividend / eps
            payout_ratio_pct = payout_ratio * 100

        rows.append(
            {
                "symbol": symbol,
                "annual_dividend_per_share": annual_dividend,
                "eps": eps,
                "payout_ratio": payout_ratio,
                "payout_ratio_pct": payout_ratio_pct,
            }
        )

    return pd.DataFrame(rows)


def main():
    quotes = load_latest_quotes_file()
    payout_df = calculate_payout_ratios(quotes)

    print("\nPayout ratios:")
    print(payout_df)


if __name__ == "__main__":
    main()