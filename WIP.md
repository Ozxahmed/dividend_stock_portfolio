# MVP

The following can be found in the README:

- Metrics
- Scoring Model
- Stack

These will change as the project progresses.

## MVP Metrics

For the MVP, I'm only going to focus on the following metrics:

- Dividend yield
- 5-year dividend growth CAGR
- Payout ratio
- Free cash flow payout ratio
- Revenue growth
- EPS growth
- Total return CAGR
- Volatility
- Max drawdown
- Sector allocation
- Weighted portfolio yield
- Weighted total return

This will give an idea of how the project will look like.

## Data Sources

- Schwab API
- Python `finvizfinance` library (unofficial finviz api)
- *Need to find a source for historical dividend data*

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
- created data/raw/ and scripts/ folder, along with python scripts for auth, price_history, quotes.
