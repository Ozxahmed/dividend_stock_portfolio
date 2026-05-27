# Dividend Stock Portfolio

This project answers the question: “Can I build a dividend portfolio that can return a minimum 8% return (dividend + stock appreciation), while beating low-risk alternatives after accounting for volatility and drawdowns?”

## Metrics

Metrics split across **five Buckets**:

### 1. Dividend return metrics

Metrics that measure the actual income engine.

- Dividend Yield: Current income return
- Forward Dividend Yield: Expected next-year income
- Dividend Growth Rate: Shows if income is compounding
- 5-Year Dividend CAGR: Smooths out noisy yearly changes
- Years of Dividend Growth: Helps identify reliable payers
- Dividend Cut History: Huge red flag if cuts happen often

`Dividend Yield = annual_dividend / current_price`

### 2. Dividend safety metrics

These indicate whether the dividend is sustainable.

- Payout Ratio: % of earnings paid as dividends
- Free Cash Flow Payout Ratio: Better than earnings payout for safety
- Debt-to-Equity: High debt can pressure dividends
- Interest Coverage Ratio: Can the company service debt?
- Revenue Growth: Weak revenue can threaten future dividends
- EPS Growth: Supports future dividend increases
- Free Cash Flow Growth: Best sign dividend can grow

earnings_payout_ratio = annual_dividend_per_share / eps

fcf_payout_ratio = total_dividends_paid / free_cash_flow

### 3. Total return metrics

Optimizing for total returns: dividend + stock price appreciation.

- Total Return: Price return + dividends
- Dividend-Adjusted Return: More accurate than price-only return
- CAGR: Annualized performance
- Sharpe Ratio: Return per unit of volatility
- Max Drawdown: Worst peak-to-trough loss
- Beta: Market sensitivity
- Volatility: Risk profile

Total Return = price_return + dividend_return

### 4. Valuation metrics

These help avoid overpaying for dividend stocks.

- P/E Ratio: Earnings valuation
- Forward P/E: Expected valuation
- Price-to-Free-Cash-Flow: Strong for dividend stocks
- EV/EBITDA: Better cross-company comparison
- Dividend Yield vs 5-Year Average Yield: Detects undervaluation/overvaluation
- Price vs 52-Week High/Low: Momentum/context

Useful dividend-specific signal:

  current_yield / five_year_average_yield

If current yield is meaningfully above historical average, the stock may be undervalued — or the market may be pricing in trouble.

### 5. Portfolio construction metrics

- Sector Allocation: Avoid overconcentration
- Weighted Average Yield: Portfolio income rate
- Weighted Dividend Growth Rate: Income growth potential
- Weighted Payout Ratio: Portfolio-level safety
- Correlation Between Holdings: Diversification
- Position Weight: Risk control
- Income Contribution by Stock: Avoid one stock providing too much income
- Total Return Contribution: Which stocks drive performance

Example portfolio-level metrics:

  portfolio_yield = sum(position_weight * dividend_yield)

  portfolio_dividend_growth = sum(position_weight * dividend_growth_rate)

  portfolio_beta = sum(position_weight * beta)

## Scoring Model

Dividend quality score weighting: (Asked ChatGPT for this; **refine later**)

| Category        | Weight |
| --------------- | -----: |
| Dividend Safety |    30% |
| Dividend Growth |    20% |
| Total Return    |    25% |
| Valuation       |    15% |
| Volatility/Risk |    10% |

Final_score =
  safety_score * 0.30 +
  dividend_growth_score * 0.20 +
  total_return_score * 0.25 +
  valuation_score * 0.15 +
  risk_score * 0.10

## T-bills

Ultimately, the portfolio return needs to be compared to T-bills, income from T-bills have the lowest risk.

If this dividend portfolio can't beat T-bills after acounting for volatility and drawdowns, it may not be worth the extra risk.

As of 5/11/26 the annualized return on:
  3-month T-bill is **3.7%**
  10-year Treasure Note is **4.39%**
  30-year Treasury Bond is **4.88%**

Therefore, at a minimum, the dividend portfolio return has to clear 6%. Let's aim for a little higher, **8%** minimum.

*dividend portfolio return = dividend stock TOTAL RETURN (price + dividend)*
**VS**
*treasury yield*

## Stack

### 1. Data warehouse: Snowflake

Possible daabase layout:

```text
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
```

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

```text
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
```

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

```text
s3://dividend-portfolio-raw/
├── schwab/
│   ├── quotes/load_date=2026-05-11/
│   └── price_history/load_date=2026-05-11/
├── finviz/
│   └── screener/load_date=2026-05-11/
└── treasury/
    └── rates/load_date=2026-05-11/
```

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
