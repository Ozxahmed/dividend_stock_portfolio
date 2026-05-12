# Dividend Stock Portfolio

I have listed all the **metrics** and **scoring model** in the **README**.

## NOTES

Initially I'm going to focus on only the following metrics to create an MVP (min viable prod):

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

## T-bills

Ultimately, the portfolio return needs to be compared to T-bills, income from T-bills have the lowest risk.

If this dividend portfolio can't beat T-bills after acounting for volatility and drawdowns, it may not be worth the extra risk.

As of 5/11/26 the annualized return on:
  3-month T-bill is **3.7%**
  10-year Treasure Note is **4.39%**
  30-year Treasury Bond is **4.88%**

Therefore, at a minimum, the dividend portfolio return has to clear 6%. Let's aim for a little higher, **8%** minimum.

The *dividend portfolio return = dividend stock TOTAL RETURN (price + dividend)*
**VS**
*treasury yield*

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

## Stack

### 1. Data warehouse: Snowflake

Possible daabase layout:

DIVIDEND_PORTFOLIO_DB
├── RAW
│   ├── raw_schwab_quotes
│   ├── raw_schwab_price_history
│   ├── raw_finviz_screener
│   ├── raw_finviz_fundamentals
│   ├── raw_dividend_history
│   └── raw_treasury_rates
│
├── STAGING
│   ├── stg_tickers
│   ├── stg_prices
│   ├── stg_dividends
│   ├── stg_fundamentals
│   ├── stg_sector_industry
│   └── stg_treasury_rates
│
├── MARTS
│   ├── dim_company
│   ├── fact_prices
│   ├── fact_dividends
│   ├── fact_financial_metrics
│   ├── mart_dividend_scorecard
│   ├── mart_portfolio_candidates
│   └── mart_portfolio_simulation
│
└── ANALYTICS
    ├── portfolio_recommendations
    ├── income_projection
    ├── risk_exposure
    └── rebalance_suggestions

Snowflake also has *dynamic tables, tasks, streams, and Cortex AI functions,* which could be useful later for *automated refreshes, incremental transformations, and **AI-powered explanations*** inside the warehouse.

### 2. Ingestion layer: Python

Recommended libraries:

- **requests** --> API calls
- **pandas** --> light cleaning before load
- **snowflake-connector-python** --> load data into Snowflake
- **snowpark-python** --> optional Snowflake-native transformations
- **python-dotenv** --> manage local credentials
- **pydantic** --> validate API response schemas
- **tenacity** --> retry failed API calls
- **loguru** --> cleaner logging

### 3. Orchestration: Airflow

Use Airflow for:

- daily quote refresh
- weekly fundamentals refresh
- monthly dividend history refresh
- monthly portfolio rebalance simulation
- Treasury/risk-free-rate updates
- data quality checks

Add this later, first check data sources, calculate metrics, and figure out the data models and schemas.

### 4. Transformation layer: dbt

Use dbt for:

- raw → staging
- staging → marts
- data tests
- documentation
- lineage
- metric definitions

dbt will be **valuable** here because this project has a lot of **calculated business logic** (div yield, payout ratio, risk score, div CAGR, etc).

Example dbt model structure:

models/
├── staging/
│   ├── stg_schwab_quotes.sql
│   ├── stg_finviz_fundamentals.sql
│   ├── stg_dividend_history.sql
│   └── stg_treasury_rates.sql
│
├── marts/
│   ├── dim_company.sql
│   ├── fact_prices.sql
│   ├── fact_dividends.sql
│   ├── mart_dividend_scorecard.sql
│   ├── mart_portfolio_candidates.sql
│   └── mart_income_projection.sql
│
└── analytics/
    ├── portfolio_recommendations.sql
    └── risk_summary.sql

### 5. Data quality: dbt tests + [optional] Great Expectations

use dbt tests for:

```yaml
not_null:
  - ticker
  - as_of_date
  - dividend_yield

unique:
  - ticker + as_of_date

accepted_range:
  - dividend_yield between 0 and 25
  - payout_ratio between 0 and 300
```

Later add **Great Expectations** if needed, for more advanced data quality check.

### 6. Storage/archive layer: S3

Use S3 for raw file archival.

Flow: API response → save JSON/CSV to S3 → load into Snowflake RAW schema

This is good for:

- auditability
- replayability
- debugging
- portfolio/resume value
- realistic DE architecture

Example S3 layout:

s3://dividend-portfolio-raw/
├── schwab/
│   ├── quotes/load_date=2026-05-11/
│   └── price_history/load_date=2026-05-11/
├── finviz/
│   └── screener/load_date=2026-05-11/
└── treasury/
    └── rates/load_date=2026-05-11/

### 7. Portfolio analytics layer: Python + SQL

use **SQL/dbt** for **repeatable** metrics:

- dividend yield
- dividend history
- sector exposure
- income by month
- payout ratio bands
- volatility metrics
- drawdown calculations
- ranking candidates

use **Python** for **optimization/simulation**:

- portfolio allocation
- Monte Carlo simulation
- risk-adjusted scoring
- efficient frontier
- constraint solving
- income target simulation

Example **optimizer constraints**:

- target monthly income >= $X
- do not sell principal
- max allocation per stock <= 5%
- max sector allocation <= 20%
- minimum dividend growth CAGR >= Y%
- maximum payout ratio <= Z%
- minimum dividend history length >= N years
- minimum market cap >= threshold
- exclude dividend cutters
- prefer lower volatility
- prefer dividend growth over extreme yield

### 8. App/dashboard layer: Streamlit

Use **Streamlit** for front end. Possible app pages:

1. Portfolio Goal Input
   - target monthly income
   - investment capital available
   - risk tolerance
   - max stock allocation
   - max sector allocation

2. Dividend Stock Screener
   - yield
   - payout ratio
   - dividend growth
   - sector
   - volatility
   - quality score

3. Portfolio Builder
   - recommended tickers
   - allocation
   - projected monthly income
   - estimated annual income
   - sector exposure
   - risk score

4. Income Calendar
   - expected dividend payments by month
   - monthly cash flow gaps

5. Risk Dashboard
   - concentration risk
   - dividend cut risk
   - valuation risk
   - drawdown risk

6. Rebalance Suggestions
   - overweight positions
   - underweight positions
   - stocks failing quality filters

### 9. BI layer: Tableau

Add at end, this can provide portfolio/resume-friendly analytics screenshots.

## MVP

Basic version of project. Use `stocksenv` env.

For MVP, I'm going to calculate the following:

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

### MVP Plan

Phase 1
Python → Snowflake RAW → dbt marts → Streamlit dashboard

Phase 2
Add S3 archival + Airflow

Phase 3
Add optimizer + portfolio simulator

Phase 4
Add Docker, GitHub Actions, documentation, and screenshots

### MVP Stack

- Snowflake
- Python
- dbt
- GitHub
- S3
- Streamlit
- Finvizfinance
- Schwab API

After MVP, can add: Airflow, Docker, Great Expectations, GitHub Actions.

### MVP Architecture

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
