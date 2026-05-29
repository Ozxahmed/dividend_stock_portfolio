# MVP (minimum viable product)

The following can be found in the [README](README.md):

- All Metrics that will be calculated
- Scoring Model
- Stack

The above will change as the project progresses. The README will be updated as needed.

## TOC

- [MVP (minimum viable product)](#mvp-minimum-viable-product)
  - [TOC](#toc)
  - [MVP Metrics](#mvp-metrics)
  - [Data Sources](#data-sources)
    - [Schwab API](#schwab-api)
  - [MVP Stack](#mvp-stack)
  - [MVP Architecture](#mvp-architecture)
  - [MVP Plan](#mvp-plan)
    - [**PHASE 1**](#phase-1)
      - [Dividend Yield](#dividend-yield)
      - [5-year dividend growth CAGR](#5-year-dividend-growth-cagr)

## MVP Metrics

For the MVP, I'm only going to focus on the following metrics:

| y/n | Metric                          | Bucket                              | Source                 | Status     | Notes                                                                                             |
| --- | ------------------------------- | ----------------------------------- | ---------------------- | ---------- | ------------------------------------------------------------------------------------------------- |
| [x] | **Dividend yield**              | *1. Dividend return metrics*        | Schwab quotes API      | Confirmed  | Use `fundamental.divYield`; also store `divAmount`, `divPayAmount`, `divFreq`, and current price. |
| [x] | **5-year dividend growth CAGR** | *1. Dividend return metrics*        | FMP dividends endpoint | Confirmed  | Use completed years only; for AAPL: 2020 → 2025 = `4.99%`.                                        |
| [x] | **Payout ratio**                | *2. Dividend safety metrics*        | Schwab quotes API      | Not tested | Earnings payout ratio: `annual_dividend_per_share / eps`.                                         |
| [ ] | **Free cash flow payout ratio** | *2. Dividend safety metrics*        | TBD                    | Not tested | Better sustainability check than earnings payout ratio.                                           |
| [ ] | **Revenue growth**              | *2. Dividend safety metrics*        | TBD                    | Not tested | Helps evaluate whether the business can support future dividends.                                 |
| [ ] | **EPS growth**                  | *2. Dividend safety metrics*        | TBD                    | Not tested | Supports future dividend increases.                                                               |
| [ ] | **Total return CAGR**           | *3. Total return metrics*           | TBD                    | Not tested | Annualized total return, ideally including dividends plus price appreciation.                     |
| [ ] | **Volatility**                  | *3. Total return metrics*           | TBD                    | Not tested | Risk profile / price movement variability.                                                        |
| [ ] | **Max drawdown**                | *3. Total return metrics*           | TBD                    | Not tested | Worst peak-to-trough loss.                                                                        |
| [ ] | **Sector allocation**           | *5. Portfolio construction metrics* | TBD                    | Not tested | Concentration/diversification control.                                                            |
| [ ] | **Weighted portfolio yield**    | *5. Portfolio construction metrics* | TBD                    | Not tested | Portfolio-level income rate. Same idea as weighted average yield.                                 |
| [ ] | **Weighted total return**       | *5. Portfolio construction metrics* | TBD                    | Not tested | Portfolio-level total return contribution across holdings.                                        |

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

### Schwab API

- schwab-py (python wrapper for Schwab API) can give us the following:
  - quote/fundamental snapshot --> ticker open/close $, dividend $, 52 wk high/low $, etc.
  - price history

### Financial Modeling Prep (FMP)

- Free Tier
- 5 year history of dividend payments

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

- App created on Schwab Developer Portal
- .env file created with schwab creds
- pip installed schwab-py
- created `data/raw/` and `scripts/` folder, along with python scripts for *auth*, *price_history*, *quotes*.
- schwab-py is python library used to access the schwab api -> it accesses the app created on the Schwab dev portal
- Can collect *market data + quote snapshot + some dividend dates* using the schwab-py
- schwab-py can give us the following:
  - quote/fundamental snapshot --> ticker open/close $, dividend $, 52 wk high/low $, etc.
  - price history
- To calculate `5-year dividend growth CAGR`, need historical dividends:
  - Signed up for Financial Modeling Prep (FMP) free tier plan

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

| Item        | Answer                                                                                                                                                               |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bucket      | Dividend return metrics                                                                                                                                              |
| Formula     | $\left( \frac{\text{dividend\_per\_share\_current\_year}}{\text{dividend\_per\_share\_5\_years\_ago}} \right)^{\frac{1}{5}} - 1$                                     |
| Purpose     | Measures how fast dividend income has compounded over the last 5 years. It answers the question: “Has the company been growing its dividend meaningfully over time?” |
| Data Needed | historical annual dividend per share                                                                                                                                 |
| Main Source | FMP API                                                                                                                                                              |

#### Payout Ratio

| Item        | Answer                                        |
| ----------- | --------------------------------------------- |
| Bucket      | 2. Dividend safety metrics                    |
| Formula     | annual_dividend_per_share / eps               |
| Data needed | `fundamental.divAmount` and `fundamental.eps` |
| Main source | Schwab quotes API                             |
