import json
from pathlib import Path

import pandas as pd


def load_latest_dividend_file(symbol: str) -> list[dict]:
    files = sorted(Path("data/raw/fmp").glob(f"dividends_{symbol}_*.json"))

    if not files:
        raise FileNotFoundError(f"No raw FMP dividend files found for {symbol}")

    latest_file = files[-1]
    print(f"Loading: {latest_file}")

    with open(latest_file, "r") as f:
        return json.load(f)


def build_annual_dividends(data: list[dict]) -> pd.DataFrame:
    if not data:
        raise ValueError("No dividend records found")

    df = pd.DataFrame(data)

    required_columns = ["symbol", "date", "adjDividend"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column from FMP response: {column}")

    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["adjDividend"] = pd.to_numeric(df["adjDividend"], errors="coerce")

    annual = (
        df.groupby(["symbol", "year"], as_index=False)
        .agg(
            annual_dividend_per_share=("adjDividend", "sum"),
            dividend_payment_count=("adjDividend", "count"),
        )
        .sort_values(["symbol", "year"])
    )

    return annual


def get_completed_years(annual: pd.DataFrame) -> pd.DataFrame:
    """
    For quarterly dividend payers like AAPL, a completed year usually has 4 payments.
    This avoids using the current partial year.
    """
    completed = annual[annual["dividend_payment_count"] >= 4].copy()

    if completed.empty:
        raise ValueError("No completed dividend years found")

    return completed


def calculate_5y_dividend_cagr(annual_completed: pd.DataFrame) -> dict:
    symbol = annual_completed["symbol"].iloc[0]

    end_year = annual_completed["year"].max()
    start_year = end_year - 5

    start_row = annual_completed[annual_completed["year"] == start_year]
    end_row = annual_completed[annual_completed["year"] == end_year]

    if start_row.empty:
        raise ValueError(f"No completed dividend data found for start year: {start_year}")

    if end_row.empty:
        raise ValueError(f"No completed dividend data found for end year: {end_year}")

    start_dividend = start_row["annual_dividend_per_share"].iloc[0]
    end_dividend = end_row["annual_dividend_per_share"].iloc[0]

    if start_dividend <= 0:
        raise ValueError("Start dividend must be greater than zero")

    cagr = (end_dividend / start_dividend) ** (1 / 5) - 1

    return {
        "symbol": symbol,
        "start_year": int(start_year),
        "end_year": int(end_year),
        "start_annual_dividend_per_share": round(float(start_dividend), 6),
        "end_annual_dividend_per_share": round(float(end_dividend), 6),
        "dividend_cagr_5y": round(float(cagr), 6),
        "dividend_cagr_5y_pct": round(float(cagr * 100), 2),
    }


def main():
    symbol = "AAPL"

    data = load_latest_dividend_file(symbol)
    annual = build_annual_dividends(data)
    annual_completed = get_completed_years(annual)

    print("\nAnnual dividend history:")
    print(annual.tail(10))

    print("\nCompleted annual dividend history:")
    print(annual_completed.tail(10))

    result = calculate_5y_dividend_cagr(annual_completed)

    print("\n5-year dividend CAGR:")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()