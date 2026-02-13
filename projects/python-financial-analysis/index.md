---
layout: default
title: Python Financial Analysis
description: "Portfolio performance and risk analysis of six diversified assets (2015-2024) using Python — time series analysis, risk metrics, correlation studies, and predictive modeling."
breadcrumbs:
  - title: Projects
    url: /projects/
  - title: Python Financial Analysis
---

<a href="/projects/" class="back-to-projects btn">&larr; Back to Projects</a>

# Python Financial Analysis: Portfolio Performance &amp; Risk (2015&ndash;2024)

> Time series analysis, risk metrics, and predictive modeling across six diversified assets using 10 years of daily market data retrieved via the yfinance API.

**Tools:** Python &middot; pandas &middot; NumPy &middot; matplotlib &middot; seaborn &middot; statsmodels &middot; scikit-learn &middot; yfinance &middot; Jupyter Notebook

<!-- TODO: Update GitHub repo link below -->
<p>
  <a href="https://github.com/nadeaujonny/nadeaujonny.github.io/tree/main/projects/python-financial-analysis" target="_blank" rel="noopener">View on GitHub &rarr;</a>
</p>

<!-- TODO: Update date completed -->
**Date Completed:** [TBD]

---

<details>
  <summary><strong>Overview</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Project Goal</h3>
  <!-- TODO: Replace placeholder text with actual project goal -->
  <p>
    This project analyzes 10 years of daily financial market data (2015&ndash;2024) for a diversified portfolio of six assets
    to evaluate historical performance, quantify risk, identify diversification opportunities, and generate short-term
    forecasts. The analysis simulates the role of a data analyst supporting portfolio management and investment
    decision-making with data-driven insights.
  </p>

  <h3>Why Financial Analysis Matters</h3>
  <!-- TODO: Replace placeholder text with actual context -->
  <p>
    Understanding portfolio risk and return characteristics is essential for informed investment decisions. This project
    demonstrates how Python and statistical methods can be applied to real market data to move beyond intuition and
    toward evidence-based portfolio evaluation &mdash; covering volatility measurement, drawdown analysis, correlation
    dynamics, and predictive modeling.
  </p>

  <h3>Skills Demonstrated</h3>
  <!-- TODO: Update list with actual skills demonstrated -->
  <ul>
    <li><strong>Data Engineering:</strong> API integration, data cleaning, feature engineering with pandas</li>
    <li><strong>Exploratory Data Analysis:</strong> Descriptive statistics, distribution analysis, trend identification</li>
    <li><strong>Risk Analytics:</strong> Volatility, Sharpe ratio, maximum drawdown, Value at Risk (VaR), correlation analysis</li>
    <li><strong>Time Series Analysis:</strong> Decomposition, stationarity testing, rolling statistics, regime detection</li>
    <li><strong>Predictive Modeling:</strong> ARIMA/SARIMA forecasting, machine learning regression</li>
    <li><strong>Data Visualization:</strong> Publication-quality charts using matplotlib and seaborn</li>
    <li><strong>Statistical Methods:</strong> Hypothesis testing, distribution fitting, statistical significance</li>
  </ul>

</details>

---

<details>
  <summary><strong>Dataset</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Assets Analyzed</h3>
  <table>
    <thead>
      <tr>
        <th>Ticker</th>
        <th>Name</th>
        <th>Asset Class</th>
        <th>Purpose</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>SPY</td><td>S&amp;P 500 ETF</td><td>US Large Cap Stocks</td><td>Market Benchmark</td></tr>
      <tr><td>AAPL</td><td>Apple Inc.</td><td>Technology Stock</td><td>Growth</td></tr>
      <tr><td>XLE</td><td>Energy Select Sector ETF</td><td>Energy Sector</td><td>Cyclical</td></tr>
      <tr><td>TLT</td><td>20+ Year Treasury Bond ETF</td><td>Bonds</td><td>Safe Haven</td></tr>
      <tr><td>GLD</td><td>SPDR Gold Trust</td><td>Commodities</td><td>Inflation Hedge</td></tr>
      <tr><td>EFA</td><td>MSCI EAFE ETF</td><td>International Stocks</td><td>Diversification</td></tr>
    </tbody>
  </table>

  <h3>Data Source</h3>
  <p>
    All price data is retrieved programmatically via the
    <a href="https://github.com/ranaroussi/yfinance" target="_blank" rel="noopener">yfinance</a>
    API &mdash; no static data files are included in this repository. Daily OHLCV (Open, High, Low, Close, Volume)
    data is pulled for the period January 2015 through December 2024.
  </p>

  <h3>Time Period</h3>
  <ul>
    <li><strong>Start:</strong> January 1, 2015</li>
    <li><strong>End:</strong> December 31, 2024</li>
    <li><strong>Granularity:</strong> Daily trading data (~2,500 trading days per asset)</li>
    <li><strong>Total observations:</strong> ~15,000 daily records across 6 assets</li>
  </ul>

  <h3>Rationale for Asset Selection</h3>
  <!-- TODO: Replace placeholder text with actual rationale -->
  <p>
    These six assets were chosen to represent a diversified portfolio spanning domestic equities (SPY), individual
    growth stocks (AAPL), sector exposure (XLE), fixed income (TLT), commodities (GLD), and international markets
    (EFA). This mix enables meaningful analysis of cross-asset correlations, diversification benefits, and
    risk-return tradeoffs across different market environments.
  </p>

</details>

---

<details markdown="1">
  <summary><strong>Analysis 1 &mdash; Data Acquisition &amp; Exploratory Data Analysis</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>
    What are the fundamental characteristics of each asset's price history over the 2015&ndash;2024 period?
    How do the assets compare in terms of price levels, growth trajectories, and basic statistical properties,
    and what preliminary relationships exist between them?
  </p>

  <h3>Methodology</h3>
  <p>
    The first step in any financial analysis is acquiring reliable data and understanding its structure. Using the
    <a href="https://github.com/ranaroussi/yfinance" target="_blank" rel="noopener">yfinance</a> Python library,
    I programmatically downloaded 10 years of daily price data (January 2015 through December 2024) for six
    diversified assets: SPY (S&amp;P 500), AAPL (Apple), XLE (Energy), TLT (Bonds), GLD (Gold), and EFA
    (International Equities). This yielded 2,515 trading days of data per asset.
  </p>
  <p>
    After retrieval, I validated the dataset for completeness and quality. The data contained zero missing values
    across all six tickers &mdash; a 100% complete dataset requiring no imputation or interpolation. I then computed
    descriptive statistics to understand the central tendency, dispersion, and shape of each asset's price
    distribution over the full period.
  </p>
  <p>
    Finally, I generated two key exploratory visualizations: a normalized price history chart to compare growth
    trajectories across assets with different price scales, and a correlation heatmap of daily returns to identify
    preliminary relationships and potential diversification opportunities within the portfolio.
  </p>

  <h3>Code</h3>

```python
# Define portfolio assets
tickers = ['SPY', 'AAPL', 'XLE', 'TLT', 'GLD', 'EFA']

# Download data via Yahoo Finance API
data = yf.download(
    tickers=tickers,
    start='2015-01-01',
    end='2024-12-31',
    auto_adjust=True
)

# Extract closing prices
prices = data['Close']
print(f"Downloaded {len(prices)} days of data")
```

  <h3>Results</h3>

![10-Year Price History](./outputs/figures/python_price_history_10years.png)
*Figure 1: Normalized price history (base = 100) for all six assets over the 2015-2024 period, allowing direct comparison of cumulative growth across assets with different price scales.*

  <h4>Summary Statistics</h4>
  <p>
    Descriptive statistics were computed across all 2,515 trading days for each asset. Key observations from the
    summary table include wide variation in price ranges (AAPL traded from approximately $27 to over $250, while
    TLT ranged from $82 to $138), confirming the need for normalization when comparing growth trajectories. Standard
    deviations also varied significantly across assets, reflecting their different volatility profiles &mdash; a
    characteristic explored further in Analysis&nbsp;2.
  </p>

![Correlation Heatmap](./outputs/figures/python_correlation_heatmap.png)
*Figure 2: Pairwise correlation heatmap of daily returns across all six assets, highlighting diversification opportunities where correlations are low or negative.*


  <h3>Key Insights</h3>
  <ul>
    <li><strong>Massive performance divergence:</strong> AAPL gained approximately 935% over the 10-year period, far outpacing SPY at 240%, while TLT (long-term bonds) lost roughly 11% &mdash; highlighting the enormous spread in outcomes across asset classes.</li>
    <li><strong>100% data completeness:</strong> All 2,515 trading days across all six tickers contained valid price data with zero missing values, confirming the reliability of the yfinance API for historical financial data retrieval.</li>
    <li><strong>Bonds as a diversifier:</strong> TLT (20+ Year Treasury Bonds) showed negative correlation with equity assets, confirming its role as a portfolio diversification tool that tends to move inversely to stocks during market stress.</li>
    <li><strong>Equity clustering:</strong> SPY, AAPL, XLE, and EFA exhibited moderate-to-strong positive correlations with each other, indicating that equity assets across sectors and geographies share common risk factors and tend to move together.</li>
    <li><strong>Gold&rsquo;s independence:</strong> GLD displayed low correlation with both equities and bonds, suggesting it provides a distinct return driver that is relatively uncoupled from traditional asset class movements.</li>
    <li><strong>Foundation for deeper analysis:</strong> The clean, complete dataset and initial correlation patterns established a solid basis for the risk metrics, time series decomposition, and forecasting analyses that follow.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 2 &mdash; Returns &amp; Risk Analysis</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Methodology</h3>
  <p>
    I converted adjusted close prices into daily percentage returns to create a consistent basis for comparing assets with very different price levels. From those daily returns, I built cumulative return series using a buy-and-hold assumption to show how each investment compounded over the full 2015&ndash;2024 window.
  </p>
  <p>
    I then calculated core risk metrics, including annualized volatility and Sharpe ratio. Annualized volatility captures the magnitude of return fluctuations (total risk), while the Sharpe ratio measures return per unit of risk after subtracting a 2% risk-free baseline. This made it possible to compare not only which asset returned more, but which delivered more efficient risk-adjusted performance.
  </p>
  <p>
    Finally, I evaluated maximum drawdown for each asset to quantify investor pain during market stress. Maximum drawdown represents the worst peak-to-trough decline before recovery, which is critical for understanding downside exposure. This drawdown analysis also highlights crisis periods, including the sharp COVID-19 selloff in March 2020.
  </p>

  <h3>Code</h3>

<pre><code class="language-python"># Calculate daily returns
daily_returns = prices.pct_change().dropna()

# Calculate cumulative returns (buy-and-hold performance)
cumulative_returns = (1 + daily_returns).cumprod()

# Calculate annualized volatility
volatility = daily_returns.std() * np.sqrt(252) * 100

# Calculate Sharpe Ratio (risk-adjusted return)
sharpe_ratio = (annual_return - 2.0) / volatility

# Display final values
print(f"$1 in AAPL became: ${cumulative_returns['AAPL'].iloc[-1]:.2f}")</code></pre>

  <h3>Visualizations</h3>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="./outputs/figures/python_cumulative_returns.png"
      alt="Cumulative growth of one dollar invested in each asset from 2015 to 2024"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Cumulative return trajectories for all six assets, showing that $1 invested in AAPL grew to $10.36 versus $3.41 in SPY over the same period.
      <span style="display:block; margin-top:4px;">
        <a href="./outputs/figures/python_cumulative_returns.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="./outputs/figures/python_risk_return_scatter.png"
      alt="Risk-return scatter plot comparing annualized return and volatility across assets"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Risk-return comparison across assets; higher returns generally came with higher volatility, with AAPL leading on risk-adjusted efficiency via the strongest Sharpe ratio.
      <span style="display:block; margin-top:4px;">
        <a href="./outputs/figures/python_risk_return_scatter.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="./outputs/figures/python_maximum_drawdown.png"
      alt="Maximum drawdown plot showing peak-to-trough declines for each asset over time"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Drawdown profiles across the decade, highlighting deep stress episodes such as the March 2020 COVID-19 crash and XLE&rsquo;s worst decline of -66.81%.
      <span style="display:block; margin-top:4px;">
        <a href="./outputs/figures/python_maximum_drawdown.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Key Insights</h3>
  <ul>
    <li>✅ <strong>AAPL delivered the strongest absolute growth:</strong> $1 invested in 2015 compounded to $10.36 by 2024, compared with $3.41 for SPY.</li>
    <li>✅ <strong>AAPL also led on risk-adjusted returns:</strong> its Sharpe ratio of 0.856 indicates the highest return per unit of risk among the assets analyzed.</li>
    <li>✅ <strong>Risk-return tradeoff was clear:</strong> AAPL posted a higher annual return (26.36%) but also materially higher volatility (28.47%) versus SPY&rsquo;s 13.05% return and 17.62% volatility.</li>
    <li>✅ <strong>Maximum drawdown highlighted downside pain:</strong> XLE experienced the deepest peak-to-trough decline at -66.81%, underscoring sector-specific crash risk in energy.</li>
    <li>✅ <strong>Systemic stress appeared across all assets in March 2020:</strong> the COVID-19 shock is visible as a synchronized drawdown event in the portfolio.</li>
    <li>✅ <strong>Return quality matters as much as return level:</strong> Sharpe ratio analysis helped separate assets that merely rose from those that compensated investors more efficiently for risk taken.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 3 &mdash; Correlation &amp; Diversification</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>
    How strongly do the portfolio assets move together, and which combinations actually improve diversification?
    More specifically, this analysis tests whether cross-asset correlations remain stable or shift across market
    regimes &mdash; and what those shifts imply for portfolio risk management.
  </p>

  <h3>Methodology</h3>
  <p>
    To evaluate diversification properly, I used <em>daily returns</em> rather than raw prices. Returns place all
    assets on a comparable scale and capture day-to-day co-movement, which is the relevant input for correlation and
    portfolio risk analysis.
  </p>
  <p>
    I first computed a full-period correlation matrix to provide a static baseline view of how each asset pair behaved
    across 2015&ndash;2024. I then added rolling correlations (60-day and 252-day windows) for key pairs such as SPY-TLT
    and SPY-GLD to show that relationships are dynamic, not fixed, and can change materially across market regimes.
  </p>
  <p>
    Finally, I translated the correlation findings into a simple diversification demonstration by comparing the
    volatility of a concentrated portfolio against a diversified allocation. This illustrates the core portfolio
    principle: combining lower-correlated assets can reduce total risk even when individual assets remain volatile.
  </p>

  <h3>Code</h3>
```python
# Load daily return data used in Notebook 3
daily_returns = pd.read_csv(
    '../data/daily_returns_2015_2024.csv',
    index_col=0,
    parse_dates=True
)

# Static correlation view across the full sample
correlation_matrix = daily_returns.corr()

# Rolling correlations to capture regime shifts
rolling_corr_spy_tlt_60 = daily_returns['SPY'].rolling(60).corr(daily_returns['TLT'])
rolling_corr_spy_tlt_252 = daily_returns['SPY'].rolling(252).corr(daily_returns['TLT'])
rolling_corr_spy_gld_60 = daily_returns['SPY'].rolling(60).corr(daily_returns['GLD'])

# Simple concentrated vs diversified risk comparison
concentrated = daily_returns[['SPY']].mean(axis=1)
diversified = daily_returns[['SPY', 'TLT', 'GLD']].mean(axis=1)
vol_compare = pd.Series({
    'Concentrated': concentrated.std() * np.sqrt(252),
    'Diversified': diversified.std() * np.sqrt(252)
})

# Figure exports from Notebook 3
plt.savefig('../outputs/figures/python_correlation_heatmap_detailed.png', dpi=300)
plt.savefig('../outputs/figures/python_rolling_correlations.png', dpi=300)
plt.savefig('../outputs/figures/python_diversification_benefit.png', dpi=300)
```

  <h3>Visualizations</h3>

![Correlation Heatmap (Detailed)](./outputs/figures/python_correlation_heatmap_detailed.png)
*Figure 1: Full-period correlations of daily returns across all six assets, providing a static view of cross-asset co-movement and diversification potential.*

![Rolling Correlations](./outputs/figures/python_rolling_correlations.png)
*Figure 2: Rolling correlation trends for key asset pairs, showing that correlation changes across market regimes and often spikes during stress periods.*

![Diversification Benefit](./outputs/figures/python_diversification_benefit.png)
*Figure 3: Concentrated vs diversified portfolio risk comparison, illustrating how blending lower-correlated assets can reduce overall volatility.*

  <h3>Key Insights</h3>
  <ul>
    <li><strong>Equity clustering is persistent:</strong> SPY and EFA generally move together, showing that international developed equities are not fully independent from U.S. equity risk.</li>
    <li><strong>Bonds diversify equities:</strong> TLT maintains low to negative correlation with SPY in many periods, supporting its role as a core portfolio stabilizer.</li>
    <li><strong>Gold is a partial diversifier:</strong> GLD typically shows lower and less stable correlation versus equities, adding a distinct return stream rather than equity-like behavior.</li>
    <li><strong>Correlations are regime-dependent:</strong> Rolling windows show that relationships shift over time, which means static assumptions can understate portfolio risk.</li>
    <li><strong>Stress periods weaken diversification:</strong> During market shocks, equity-linked correlations tend to rise, reducing diversification benefits exactly when protection is most needed.</li>
    <li><strong>Diversification lowers volatility:</strong> A blended multi-asset allocation produces smoother return behavior than concentrated equity exposure.</li>
    <li><strong>Risk management requires monitoring:</strong> Correlation should be treated as a dynamic risk input and reviewed continuously, not as a one-time estimate.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li>Use TLT and GLD as intentional diversifiers rather than adding only equity-like exposures.</li>
    <li>Track rolling correlations in portfolio monitoring to detect diversification breakdowns during stressed markets.</li>
    <li>Avoid assuming EFA provides strong downside insulation versus SPY in crisis regimes.</li>
    <li>Rebalance periodically so target diversification weights are maintained as market moves shift exposures.</li>
    <li>In risk planning, stress-test portfolios under higher-correlation scenarios rather than relying on long-run averages.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 4 &mdash; Time Series Trends &amp; Decomposition</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

### Business Question

<p>
  Financial markets are dynamic systems in which asset prices reflect both long-run macroeconomic forces and short-run shifts in investor sentiment. This analysis examines how major ETFs evolve through time to identify persistent directional trends versus temporary dislocations.
</p>

<p>
  Beyond simple price direction, the objective is to test whether recurring patterns and structural breaks can be detected in a systematic way. In particular, moving-average relationships are used to interpret market regimes (risk-on vs. risk-off), while decomposition techniques separate broad trend effects from seasonal behavior and unexplained residual shocks.
</p>

<p>
  From a portfolio-management perspective, this framework helps answer whether observable technical signals align with known market events such as the COVID-19 drawdown and the higher-volatility rate-hike environment. The goal is to produce interpretable evidence that supports timing, risk monitoring, and allocation decisions.
</p>

### Methodology

<p>
  Price series were first normalized to a common starting value so relative performance could be compared across assets with different price levels. This ensures the analysis focuses on trajectory and regime behavior rather than nominal price differences.
</p>

<p>
  Trend-following structure was evaluated using 50-day and 200-day moving averages, with crossover events flagged as potential regime transitions. Golden crosses (50-day above 200-day) were interpreted as strengthening momentum regimes, while death crosses signaled potential deterioration in trend conditions.
</p>

<p>
  A classical time-series decomposition was then applied to isolate trend, seasonal, and residual components. Interpreting these components alongside known event windows made it possible to identify structural breaks, including the COVID crash and the elevated volatility period associated with rapid policy-rate increases.
</p>

### Code

```python
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt

# Normalize for comparability
normalized = prices.div(prices.iloc[0]).mul(100)

# Rolling moving averages for regime interpretation
prices['SPY_50MA'] = prices['SPY'].rolling(window=50, min_periods=50).mean()
prices['SPY_200MA'] = prices['SPY'].rolling(window=200, min_periods=200).mean()

# Golden/death cross flags
prices['Cross_Signal'] = (prices['SPY_50MA'] > prices['SPY_200MA']).astype(int)

# Time series decomposition (trading-day seasonality proxy)
decomposition = seasonal_decompose(prices['SPY'].dropna(), model='multiplicative', period=252)

# Plot references (full styling omitted for brevity)
ax = prices[['SPY', 'SPY_50MA', 'SPY_200MA']].plot(figsize=(12, 6))
ax.set_title('SPY with 50-Day and 200-Day Moving Averages')
plt.savefig('outputs/figures/python_moving_averages.png', dpi=300, bbox_inches='tight')

decomposition.plot()
plt.savefig('outputs/figures/python_time_series_decomposition.png', dpi=300, bbox_inches='tight')
```

### Visualizations

<figure style="margin: 0 0 18px 0;">
  <img
    src="images/python-moving-averages.png"
    alt="SPY price with 50-day and 200-day moving averages for regime detection"
    loading="lazy"
    style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
  >
  <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
    SPY trend profile with 50-day and 200-day moving averages. Crossovers highlight potential transitions between bullish and defensive market regimes.
    <span style="display:block; margin-top:4px;">
      <a href="images/python-moving-averages.png">Open full-size</a>
    </span>
  </figcaption>
</figure>

<figure style="margin: 0 0 18px 0;">
  <img
    src="images/python-decomposition.png"
    alt="Time series decomposition of SPY into trend seasonal and residual components"
    loading="lazy"
    style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
  >
  <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
    Decomposition output separating long-run trend, seasonal effects, and residual noise to isolate underlying market structure.
    <span style="display:block; margin-top:4px;">
      <a href="images/python-decomposition.png">Open full-size</a>
    </span>
  </figcaption>
</figure>

<figure style="margin: 0 0 18px 0;">
  <img
    src="images/python-market-regimes.png"
    alt="Market regime timeline showing bull bear and high-volatility transition periods"
    loading="lazy"
    style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
  >
  <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
    Regime segmentation view used to contextualize trend strength, drawdowns, and transition intervals across the full sample window.
    <span style="display:block; margin-top:4px;">
      <a href="images/python-market-regimes.png">Open full-size</a>
    </span>
  </figcaption>
</figure>

### Key Insights

<ul>
  <li><strong>Trend dominates long horizons:</strong> The decomposition trend component explains most multi-year price direction, while seasonal effects are comparatively weak for broad ETFs.</li>
  <li><strong>Crossover signals are regime-sensitive:</strong> Golden crosses generally align with sustained recovery phases, whereas death crosses tend to cluster around risk-off transitions and prolonged drawdowns.</li>
  <li><strong>Structural breaks are visible in residuals:</strong> Event-driven shocks such as the COVID selloff and policy-tightening volatility appear as large residual deviations from baseline trend behavior.</li>
  <li><strong>Signal confirmation improves interpretation:</strong> Moving-average signals are most useful when evaluated alongside decomposition outputs and macro context rather than as standalone trading triggers.</li>
</ul>

### Business Interpretation

<p>
  For decision-makers, this analysis provides a practical monitoring framework: decomposition clarifies whether market moves are structural or transitory, and moving-average relationships provide a transparent regime dashboard for tactical risk management.
</p>

<p>
  In application, crossover events can trigger deeper portfolio review rather than automatic execution, especially during known high-volatility macro periods. Combining technical and statistical signals supports more disciplined rebalancing, clearer communication of market conditions, and stronger governance around drawdown response.
</p>

</details>

---

<details>
  <summary><strong>Analysis 5 &mdash; Forecasting</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <!-- TODO: Replace placeholder text with actual business question -->
  <p>
    Can statistical time series models and machine learning methods produce useful short-term forecasts
    of asset prices or returns? How do different modeling approaches compare in accuracy and reliability?
  </p>

  <h3>Method</h3>
  <!-- TODO: Replace placeholder text with actual methodology -->
  <ul>
    <li>Split data into training and test sets using time-based train/test split</li>
    <li>Built ARIMA/SARIMA models using ACF/PACF-informed parameter selection</li>
    <li>Implemented machine learning regression models (e.g., Random Forest, Linear Regression) for return prediction</li>
    <li>Evaluated model performance using RMSE, MAE, and directional accuracy metrics</li>
    <li>Generated forward-looking forecasts with confidence intervals</li>
    <li>Compared statistical vs. ML approaches for financial time series prediction</li>
  </ul>

  <h3>Code</h3>
  <!-- TODO: Add actual code snippet from notebook 5 -->

```python
# Placeholder — will be replaced with actual analysis code
from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Train/test split (80/20 time-based)
train_size = int(len(prices) * 0.8)
train, test = prices['SPY'][:train_size], prices['SPY'][train_size:]

# ARIMA model
model = ARIMA(train, order=(1, 1, 1))
fitted = model.fit()
forecast = fitted.forecast(steps=len(test))

# Evaluate
rmse = np.sqrt(mean_squared_error(test, forecast))
print(f'ARIMA RMSE: {rmse:.4f}')
```

  <h3>Results</h3>

  <!-- TODO: Replace placeholder image with actual vs predicted chart -->
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/python-actual-vs-predicted.png"
      alt="Actual vs predicted values chart comparing model forecast to real prices"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Actual vs. predicted values on the test set, comparing model forecasts to realized prices.
      <span style="display:block; margin-top:4px;">
        <a href="images/python-actual-vs-predicted.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <!-- TODO: Replace placeholder image with actual forecast chart -->
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/python-forecast.png"
      alt="Future forecast chart with confidence intervals"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Forward-looking forecast with 95% confidence intervals showing projected price trajectory.
      <span style="display:block; margin-top:4px;">
        <a href="images/python-forecast.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <!-- TODO: Replace placeholder image with actual accuracy metrics visualization -->
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/python-accuracy-metrics.png"
      alt="Model accuracy metrics comparison across different forecasting approaches"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Model accuracy comparison: RMSE, MAE, and directional accuracy across forecasting methods.
      <span style="display:block; margin-top:4px;">
        <a href="images/python-accuracy-metrics.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Key Insights</h3>
  <!-- TODO: Replace placeholder insights with actual findings -->
  <ul>
    <li><strong>[TBD]:</strong> Placeholder insight about forecasting accuracy of ARIMA vs. ML models</li>
    <li><strong>[TBD]:</strong> Placeholder insight about challenges of financial time series prediction</li>
    <li><strong>[TBD]:</strong> Placeholder insight about confidence interval width and forecast uncertainty</li>
    <li><strong>[TBD]:</strong> Placeholder insight about practical applicability of the forecasting results</li>
  </ul>

</details>

---

<details>
  <summary><strong>Key Findings &amp; Recommendations</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Major Insights</h3>
  <!-- TODO: Replace placeholder insights with actual summary findings -->
  <ul>
    <li><strong>[TBD]:</strong> Placeholder summary insight about overall portfolio performance across the 10-year period</li>
    <li><strong>[TBD]:</strong> Placeholder summary insight about risk-return tradeoffs and the most efficient assets</li>
    <li><strong>[TBD]:</strong> Placeholder summary insight about diversification effectiveness and correlation dynamics</li>
    <li><strong>[TBD]:</strong> Placeholder summary insight about time series patterns and regime behavior</li>
    <li><strong>[TBD]:</strong> Placeholder summary insight about forecasting model performance and limitations</li>
  </ul>

  <h3>Portfolio Recommendations</h3>
  <!-- TODO: Replace placeholder recommendations with actual data-driven recommendations -->
  <ul>
    <li><strong>[TBD]:</strong> Placeholder recommendation about optimal asset allocation based on risk-return analysis</li>
    <li><strong>[TBD]:</strong> Placeholder recommendation about diversification strategy using correlation insights</li>
    <li><strong>[TBD]:</strong> Placeholder recommendation about rebalancing approach based on regime analysis</li>
    <li><strong>[TBD]:</strong> Placeholder recommendation about risk management using drawdown and VaR metrics</li>
  </ul>

  <h3>Business Value</h3>
  <!-- TODO: Replace placeholder text with actual business value statement -->
  <p>
    This analysis demonstrates how Python-based quantitative methods can support portfolio evaluation and
    risk management decisions. The combination of exploratory analysis, statistical modeling, and machine
    learning provides a comprehensive toolkit for data-driven investment insights.
  </p>

  <h3>Disclaimer</h3>
  <p>
    <em>This project is for educational and portfolio demonstration purposes only. It does not constitute
    financial advice, investment recommendations, or trading signals. Past performance does not guarantee
    future results. Always consult a qualified financial advisor before making investment decisions.</em>
  </p>

</details>

---

<details>
  <summary><strong>Technical Details</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Libraries Used</h3>
  <!-- TODO: Update versions after project completion -->
  <ul>
    <li><strong>Python 3.10+</strong></li>
    <li><strong>pandas</strong> &mdash; data manipulation and analysis</li>
    <li><strong>NumPy</strong> &mdash; numerical computing</li>
    <li><strong>yfinance</strong> &mdash; Yahoo Finance API for market data retrieval</li>
    <li><strong>matplotlib</strong> &mdash; static data visualization</li>
    <li><strong>seaborn</strong> &mdash; statistical data visualization</li>
    <li><strong>statsmodels</strong> &mdash; time series analysis, decomposition, ARIMA, statistical tests</li>
    <li><strong>SciPy</strong> &mdash; scientific computing and statistical functions</li>
    <li><strong>scikit-learn</strong> &mdash; machine learning models and evaluation metrics</li>
    <li><strong>Jupyter Notebook</strong> &mdash; interactive analysis environment</li>
  </ul>

  <h3>How to Reproduce</h3>
  <!-- TODO: Update reproduction steps after project completion -->
  <ol>
    <li>Clone the repository: <code>git clone https://github.com/nadeaujonny/nadeaujonny.github.io.git</code></li>
    <li>Navigate to the project: <code>cd projects/python-financial-analysis</code></li>
    <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
    <li>Run the notebooks in order (01 through 05) in Jupyter</li>
    <li>Charts and outputs will be saved to the <code>outputs/</code> directory</li>
  </ol>

  <h3>Project Structure</h3>
  <!-- TODO: Update project structure after completion -->
  <pre><code>python-financial-analysis/
├── index.md                  # This project page
├── requirements.txt          # Python dependencies
├── README.md                 # Project README
├── data/                     # Data directory (API-sourced, not committed)
├── notebooks/                # Jupyter notebooks (01-05)
│   ├── 01_data_acquisition_eda.ipynb
│   ├── 02_returns_risk_metrics.ipynb
│   ├── 03_correlation_diversification.ipynb
│   ├── 04_time_series_decomposition.ipynb
│   └── 05_forecasting.ipynb
├── images/                   # Charts and visualizations
└── outputs/                  # Generated outputs and exports
</code></pre>

  <h3>Contact</h3>
  <!-- TODO: Update LinkedIn link -->
  <p>
    <a href="https://www.linkedin.com/in/nadeaujonny/" target="_blank" rel="noopener">Connect on LinkedIn &rarr;</a>
  </p>

</details>
