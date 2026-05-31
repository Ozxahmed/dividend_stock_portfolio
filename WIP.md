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
    - [Financial Modeling Prep (FMP)](#financial-modeling-prep-fmp)
  - [MVP Stack](#mvp-stack)
  - [MVP Architecture](#mvp-architecture)
  - [MVP Plan](#mvp-plan)
  - [**PHASE 1**](#phase-1)
    - [Metrics](#metrics)
      - [Dividend Yield](#dividend-yield)
      - [5-year dividend growth CAGR](#5-year-dividend-growth-cagr)
      - [Payout Ratio](#payout-ratio)
      - [Free cash flow payout ratio](#free-cash-flow-payout-ratio)
      - [5-Year Revenue growth CAGR](#5-year-revenue-growth-cagr)

## MVP Metrics

For the MVP, I'm only going to focus on the following metrics:

| y/n | Metric                          | Bucket                              | Source                  | Status     | Notes                                                                                             |
| --- | ------------------------------- | ----------------------------------- | ----------------------- | ---------- | ------------------------------------------------------------------------------------------------- |
| [x] | **Dividend yield**              | *1. Dividend return metrics*        | Schwab quotes API       | Confirmed  | Use `fundamental.divYield`; also store `divAmount`, `divPayAmount`, `divFreq`, and current price. |
| [x] | **5-year dividend growth CAGR** | *1. Dividend return metrics*        | FMP dividends endpoint  | Confirmed  | Use completed years only; for AAPL: 2020 → 2025 = `4.99%`.                                        |
| [x] | **Payout ratio**                | *2. Dividend safety metrics*        | Schwab quotes API       | Confirmed  | Use `fundamental.divAmount / fundamental.eps`; for AAPL: `1.08 / 7.46 = 14.48%`.                  |
| [x] | **Free cash flow payout ratio** | *2. Dividend safety metrics*        | FMP cash flow statement | Confirmed  | Use `abs(netDividendsPaid) / freeCashFlow`; for AAPL FY2025: `15.61%`.                            |
| [*] | **5-year Revenue growth CAGR**  | *2. Dividend safety metrics*        | TBD                     | Not tested | Helps evaluate whether the business can support future dividends.                                 |
| [ ] | **EPS growth**                  | *2. Dividend safety metrics*        | TBD                     | Not tested | Supports future dividend increases.                                                               |
| [ ] | **Total return CAGR**           | *3. Total return metrics*           | TBD                     | Not tested | Annualized total return, ideally including dividends plus price appreciation.                     |
| [ ] | **Volatility**                  | *3. Total return metrics*           | TBD                     | Not tested | Risk profile / price movement variability.                                                        |
| [ ] | **Max drawdown**                | *3. Total return metrics*           | TBD                     | Not tested | Worst peak-to-trough loss.                                                                        |
| [ ] | **Sector allocation**           | *5. Portfolio construction metrics* | TBD                     | Not tested | Concentration/diversification control.                                                            |
| [ ] | **Weighted portfolio yield**    | *5. Portfolio construction metrics* | TBD                     | Not tested | Portfolio-level income rate. Same idea as weighted average yield.                                 |
| [ ] | **Weighted total return**       | *5. Portfolio construction metrics* | TBD                     | Not tested | Portfolio-level total return contribution across holdings.                                        |

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

## **PHASE 1**

- App created on Schwab Developer Portal
- .env file created with schwab creds
- pip installed schwab-py
- created `data/raw/` and `scripts/` folder, along with python scripts for *auth*, *price_history*, *quotes*.
- schwab-py is python library used to access the schwab api -> it accesses the app created on the Schwab dev portal
- Can collect *market data + quote snapshot + some dividend dates* using the schwab-py
- schwab-py can give us the following:
  - quote/fundamental snapshot --> ticker open/close $, dividend $, 52 wk high/low $, etc.
  - price history
- To calculate `5-year dividend growth CAGR`, need historical dividends
  - Signed up for Financial Modeling Prep (FMP) free tier plan
  - Can fetch historical data, up to 5 years.

### Metrics

#### Dividend Yield

Available from Schwab APO Quotes call. In addition to dividend yield, collect following data:

- `ticker`
- `quote_date`
- `current_price`
- `annual_dividend_per_share`
- **`dividend_yield`**
- `dividend_frequency`
- `dividend_pay_amount`

#### 5-year dividend growth CAGR

|             |                                                                                                                                                                      |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bucket      | 1 - Dividend return metrics                                                                                                                                          |
| Formula     | $\left( \frac{D_{\text{current}}}{D_{\text{5 years ago}}} \right)^{\frac{1}{5}} - 1$                                                                                 |
| Purpose     | Measures how fast dividend income has compounded over the last 5 years. It answers the question: “Has the company been growing its dividend meaningfully over time?” |
| Data Needed | historical annual dividend per share                                                                                                                                 |
| Main Source | FMP API                                                                                                                                                              |

Where:

- $D_{\text{current}}$ = annual dividend per share for the current completed year
- $D_{\text{5 years ago}}$ = annual dividend per share from 5 years ago

#### Payout Ratio

| Item        | Answer                                                        |
| ----------- | ------------------------------------------------------------- |
| Bucket      | 2 - Dividend safety metrics                                   |
| Formula     | $\frac{D_{\text{annual}}}{EPS}$                               |
| Data Needed | `fundamental.divAmount` and `fundamental.eps`                 |
| Main Source | Schwab quotes API                                             |

Where:

- $D_{\text{annual}}$ = annual dividend per share
- $EPS$ = earnings per share

#### Free cash flow payout ratio

|             |                                                                                                                                                                                                                            |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bucket      | 2 - Dividend safety metrics                                                                                                                                                                                                |
| Formula     | $\frac{D_{\text{paid}}}{FCF}$                                                                                                                                                                                              |
| Purpose     | Measures whether the company’s dividend is supported by actual cash generation. This is usually a stronger dividend safety check than earnings payout ratio because dividends are paid with cash, not accounting earnings. |
| Data Needed | Total dividends paid and free cash flow                                                                                                                                                                                    |
| Main Source | FMP API                                                                                                                                                                                                                    |

Where:

- $D_{\text{paid}}$ = total dividends paid
- $FCF$ = free cash flow

#### 5-Year Revenue growth CAGR

| Item             | Answer                                                                                                                                                                                                             |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Bucket           | Dividend safety metrics                                                                                                                                                                                            |
| Formula          | $\left( \frac{\text{revenue_current_year}}{\text{revenue_5_years_ago}} \right)^{\frac{1}{5}} - 1$                                                                                                                  |
| Purpose          | Measures whether the company’s top-line business is growing enough to support future earnings, cash flow, and dividend growth. Weak or declining revenue can be an early warning sign for dividend sustainability. |
| Data Needed      | Historical annual revenue for at least 5 completed fiscal years                                                                                                                                                    |
| Main Source      | FMP API                                                                                                                                                                                                            |
| Endpoint to Test | `https://financialmodelingprep.com/stable/income-statement?symbol=AAPL`                                                                                                                                            |
| Expected Fields  | `symbol`, `date`, `fiscalYear`, `period`, `revenue`                                                                                                                                                                |
| Status           | Not tested yet                                                                                                                                                                                                     |
