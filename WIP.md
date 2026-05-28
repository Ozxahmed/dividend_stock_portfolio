# MVP (minimum viable product)

The following can be found in the README:

- Metrics
- Scoring Model
- Stack

The above will change as the project progresses. I'll update the README as changes are confirmed.

## MVP Metrics

For the MVP, I'm only going to focus on the following metrics:

| y/n | Metric                          | Bucket                              | Source                  | Status     | Notes                                                                                                  |
| --- | ------------------------------- | ----------------------------------- | ----------------------- | ---------- | ------------------------------------------------------------------------------------------------------ |
| [x] | **Dividend yield**              | *1. Dividend return metrics*        | Schwab quotes API       | Confirmed  | Use `fundamental.divYield`; also store `divAmount`, `divPayAmount`, `divFreq`, and current price.      |
| [x] | **5-year dividend growth CAGR** | *1. Dividend return metrics*        | FMP dividends endpoint  | Confirmed  | Use completed years only; for AAPL: 2020 → 2025 = `4.99%`.                                             |
| [ ] | **Payout ratio**                | *2. Dividend safety metrics*        | TBD                     | Not tested | Earnings payout ratio: `annual_dividend_per_share / eps`.                                              |
| [ ] | **Free cash flow payout ratio** | *2. Dividend safety metrics*        | TBD                     | Not tested | Better sustainability check than earnings payout ratio.                                                |
| [ ] | **Revenue growth**              | *2. Dividend safety metrics*        | TBD                     | Not tested | Helps evaluate whether the business can support future dividends.                                      |
| [ ] | **EPS growth**                  | *2. Dividend safety metrics*        | TBD                     | Not tested | Supports future dividend increases.                                                                    |
| [ ] | **Total return CAGR**           | *3. Total return metrics*           | TBD                     | Not tested | Annualized total return, ideally including dividends plus price appreciation.                          |
| [ ] | **Volatility**                  | *3. Total return metrics*           | TBD                     | Not tested | Risk profile / price movement variability.                                                             |
| [ ] | **Max drawdown**                | *3. Total return metrics*           | TBD                     | Not tested | Worst peak-to-trough loss.                                                                             |
| [ ] | **Sector allocation**           | *5. Portfolio construction metrics* | TBD                     | Not tested | Concentration/diversification control.                                                                 |
| [ ] | **Weighted portfolio yield**    | *5. Portfolio construction metrics* | TBD                     | Not tested | Portfolio-level income rate. Same idea as weighted average yield.                                      |
| [ ] | **Weighted total return**       | *5. Portfolio construction metrics* | TBD                     | Not tested | Portfolio-level total return contribution across holdings.                                             |

## Data Sources

- Schwab API
- Python `finvizfinance` library (unofficial finviz api)
- [] *Need to find a source for historical dividend data*

Other possible sources to evaluate:

- Nasdaq dividend history pages
- Alpha Vantage
- Financial Modeling Prep
- Polygon.io
- Tiingo
- IEX Cloud alternatives
- Kaggle/static dividend aristocrat lists
- yfinance as a fallback

## MVP Stack

- Snowflake
- Python
- dbt
- GitHub
- S3
- Streamlit
- Finvizfinance
- Schwab API

After MVP, can add: Airflow, Docker, Great Expectations, GitHub Actions.

## MVP Architecture

```md

                 ┌────────────────────┐
                 │   Schwab API        │
                 │   Finviz Library    │
                 │   Div Historical data │
                 │   Treasury Data     │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │ Python Ingestion    │
                 │ API clients         │
                 │ validation/logging  │
                 └─────────┬──────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
      ┌──────────────┐          ┌────────────────┐
      │ S3 Raw Files │          │ Snowflake RAW  │
      └──────────────┘          └───────┬────────┘
                                        │
                                        ▼
                              ┌────────────────┐
                              │ dbt STAGING    │
                              └───────┬────────┘
                                      │
                                      ▼
                              ┌────────────────┐
                              │ dbt MARTS      │
                              │ Scorecards     │
                              │ Metrics        │
                              └───────┬────────┘
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                ┌────────────────┐        ┌─────────────────┐
                │ Python Optimizer│        │ Streamlit App   │
                │ Portfolio Logic │        │ Dashboard/Input │
                └────────────────┘        └─────────────────┘
```

## MVP Plan

Phase 1
Python → Snowflake RAW → dbt marts → Streamlit dashboard

Phase 2
Add S3 archival + Airflow

Phase 3
Add optimizer + portfolio simulator

Phase 4
Add Docker, GitHub Actions, documentation, and screenshots

### **PHASE 1**

#### Schwab API

- App created on Schwab developer portal
- created .env file with schwab creds
- pip installed schwab-py
- created `data/raw/` and `scripts/` folder, along with python scripts for *auth*, *price_history*, *quotes*.
- schwab-py is python library used to access the schwab api -> it accesses the app created on the Schwab dev portal
- Can collect *market data + quote snapshot + some dividend dates* using the schwab-py
- [] There could be other end points that the api can access, depending on what I'm allowed within the schwab dev portal access.
- schwab-py can give us the following:
  - quote/fundamental snapshot --> ticker open/close $, dividend $, 52 wk high/low $, etc.
  - price history

#### Dividend Yield

Available from Quotes call. In addition to dividend yield, collect following data:

- ticker
- quote_date
- current_price
- annual_dividend_per_share
- **dividend_yield**
- dividend_frequency
- dividend_pay_amount

#### 5-year dividend growth CAGR

Need historical dividends.

- [x] test Financial Modeling Prep (FMP) free tier plan

FMP free tier works!
