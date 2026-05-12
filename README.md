# Dividend Stock Portfolio

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

`Payout ratio = dividend_paid / free_cash_flow`

### 3. Total return metrics

Optimizing for total returns: dividend + stock price appreciation.

- Total Return: Price return + dividends
- Dividend-Adjusted Return: More accurate than price-only return
- CAGR: Annualized performance
- Sharpe Ratio: Return per unit of volatility
- Max Drawdown: Worst peak-to-trough loss
- Beta: Market sensitivity
- Volatility: Risk profile

`Total Return = price_return + dividend_return`

### 4. Valuation metrics

These help avoid overpaying for dividend stocks.

- P/E Ratio: Earnings valuation
- Forward P/E: Expected valuation
- Price-to-Free-Cash-Flow: Strong for dividend stocks
- EV/EBITDA: Better cross-company comparison
- Dividend Yield vs 5-Year Average Yield: Detects undervaluation/overvaluation
- Price vs 52-Week High/Low: Momentum/context

Useful dividend-specific signal:

  `current_yield / five_year_average_yield`

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

  `portfolio_yield = sum(position_weight * dividend_yield)`

  `portfolio_dividend_growth = sum(position_weight * dividend_growth_rate)`

  `portfolio_beta = sum(position_weight * beta)`

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
