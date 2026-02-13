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

  <h3>Business Question</h3>
  <p>
    Which assets delivered the best return-to-risk profile over 2015&ndash;2024, and where were the largest downside episodes
    that could challenge portfolio durability?
  </p>

  <h3>Methodology</h3>
  <p>
    Daily percentage returns were computed from adjusted close prices so every asset could be compared on a common scale.
    I then annualized return and volatility, applied a 2% risk-free assumption for Sharpe ratio, and ranked assets by
    risk-adjusted efficiency.
  </p>
  <p>
    To measure downside risk, I calculated maximum drawdown from each return stream&rsquo;s cumulative path. This complements
    volatility by showing worst peak-to-trough losses and highlights stress behavior during sharp market shocks.
  </p>

  <h3>Code Highlight (Key Logic)</h3>
  <pre><code class="language-python">import numpy as np
import pandas as pd

# Daily returns
daily_returns = prices.pct_change().dropna()

def max_drawdown(return_series: pd.Series) -> float:
    """Max drawdown from cumulative returns."""
    cum = (1 + return_series).cumprod()
    peak = cum.cummax()
    dd = (cum / peak) - 1
    return dd.min()

def risk_metrics(returns: pd.DataFrame, rf: float = 0.02) -> pd.DataFrame:
    """Annualized return, volatility, Sharpe, max drawdown for each asset."""
    ann_return = (1 + returns.mean())**252 - 1
    ann_vol = returns.std() * np.sqrt(252)
    sharpe = (ann_return - rf) / ann_vol
    mdd = returns.apply(max_drawdown)

    metrics = pd.DataFrame({
        "Annual Return": ann_return,
        "Annual Volatility": ann_vol,
        "Sharpe (rf=2%)": sharpe,
        "Max Drawdown": mdd
    })

    return metrics.sort_values("Sharpe (rf=2%)", ascending=False)

metrics_df = risk_metrics(daily_returns, rf=0.02)
print(metrics_df.round(4))</code></pre>

  <h3>Visualizations</h3>
  <img src="./outputs/figures/python_risk_return_scatter.png" alt="Risk-return scatter plot across portfolio assets" style="max-width:100%; height:auto; display:block; margin: 12px 0;">
  <p><em>Figure 1: Annualized return versus volatility comparison to evaluate risk-adjusted positioning across assets.</em></p>

  <img src="./outputs/figures/python_maximum_drawdown.png" alt="Maximum drawdown paths for each asset" style="max-width:100%; height:auto; display:block; margin: 12px 0;">
  <p><em>Figure 2: Drawdown trajectories showing each asset&rsquo;s worst historical peak-to-trough declines.</em></p>

  <h3>Key Insights</h3>
  <ul>
    <li>Return and volatility moved together, reinforcing the core risk-return tradeoff across the portfolio.</li>
    <li>Sharpe ranking provided a clearer quality signal than raw return alone.</li>
    <li>Maximum drawdown exposed downside severity that volatility by itself can understate.</li>
    <li>Drawdown paths revealed synchronized stress windows during broad market disruptions.</li>
    <li>Some assets showed materially deeper downside tails despite similar long-run growth.</li>
    <li>Risk metrics should be interpreted as a package, not as standalone indicators.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li>Use Sharpe and max drawdown together when screening or rebalancing portfolio weights.</li>
    <li>Set risk limits based on acceptable drawdown tolerance, not only annual volatility.</li>
    <li>Stress-test allocations against crisis-style scenarios before implementing changes.</li>
    <li>Reassess risk metrics periodically as return distributions evolve through market regimes.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 3 &mdash; Correlation &amp; Diversification</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>
    How stable are cross-asset relationships over time, and how much risk reduction can be achieved by combining assets
    with lower co-movement instead of concentrating in a single market exposure?
  </p>

  <h3>Methodology</h3>
  <p>
    I analyzed daily return correlations to quantify co-movement, then layered rolling correlation windows to track
    how relationships shifted across market environments. This helps distinguish long-run averages from regime-specific
    behavior that matters for real-time risk management.
  </p>
  <p>
    I also compared concentrated and diversified portfolio volatility using annualized covariance matrix math. This
    translates correlation into a direct diversification outcome at the portfolio level.
  </p>

  <h3>Code Highlight (Key Logic)</h3>
  <pre><code class="language-python">import numpy as np
import pandas as pd

# Load daily returns
daily_returns = pd.read_csv("./data/daily_returns_2015_2024.csv", index_col=0, parse_dates=True)

# Static correlation (full period)
corr = daily_returns.corr()

# Rolling correlation (regime sensitivity)
rolling_corr_spy_tlt = daily_returns["SPY"].rolling(252).corr(daily_returns["TLT"])

# Diversification math: portfolio volatility via covariance
cov = daily_returns.cov() * 252  # annualized covariance

w_concentrated = np.array([1, 0, 0])                 # SPY only
w_diversified = np.array([0.6, 0.3, 0.1])            # SPY/TLT/GLD example

assets = ["SPY", "TLT", "GLD"]
cov_3 = cov.loc[assets, assets].values

vol_concentrated = np.sqrt(w_concentrated.T @ cov_3 @ w_concentrated)
vol_diversified = np.sqrt(w_diversified.T @ cov_3 @ w_diversified)

print(f"Annualized vol (SPY only): {vol_concentrated:.2%}")
print(f"Annualized vol (diversified): {vol_diversified:.2%}")</code></pre>

  <h3>Visualizations</h3>
  <img src="./outputs/figures/python_correlation_heatmap_detailed.png" alt="Detailed correlation heatmap of portfolio returns" style="max-width:100%; height:auto; display:block; margin: 12px 0;">
  <p><em>Figure 1: Full-period return correlation map for baseline diversification assessment.</em></p>

  <img src="./outputs/figures/python_rolling_correlations.png" alt="Rolling correlation trends across selected asset pairs" style="max-width:100%; height:auto; display:block; margin: 12px 0;">
  <p><em>Figure 2: Rolling correlations showing that cross-asset relationships vary across regimes.</em></p>

  <img src="./outputs/figures/python_diversification_benefit.png" alt="Diversification benefit comparison between concentrated and mixed portfolio" style="max-width:100%; height:auto; display:block; margin: 12px 0;">
  <p><em>Figure 3: Volatility comparison illustrating risk reduction from a diversified allocation.</em></p>

  <h3>Key Insights</h3>
  <ul>
    <li>Static correlations provided useful baseline structure, but they masked major time variation.</li>
    <li>Correlations changed materially across calm and stress periods.</li>
    <li>Negative or low-correlation relationships were not constant through the full sample.</li>
    <li>Diversification benefits were strongest when cross-asset co-movement stayed moderate.</li>
    <li>Diversification can weaken during market stress when correlations converge upward.</li>
    <li>Covariance-based portfolio volatility gave a more practical risk view than pairwise correlation alone.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li>Monitor rolling correlations as an ongoing risk dashboard, not a one-time diagnostic.</li>
    <li>Use scenario-aware allocations that anticipate temporary correlation breakdowns.</li>
    <li>Favor diversification across distinct risk drivers, not just additional tickers.</li>
    <li>Rebalance with covariance-based portfolio volatility targets rather than static weight rules.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 4 &mdash; Time Series Decomposition</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">
  <h3>Business Question</h3>
  <p>
    What components drive SPY price movement over time, and how can trend, seasonality, and residual shocks be
    separated to support clearer regime interpretation for investment decisions?
  </p>

  <h3>Methodology</h3>
  <p>
    I used moving averages (50-day and 200-day) as practical regime indicators, then decomposed the SPY series into
    trend, seasonal, and residual components using a trading-year periodicity. This clarifies whether observed price
    behavior is persistent structure or short-lived noise.
  </p>
  <p>
    I additionally ran an ADF test on returns to assess stationarity assumptions relevant for downstream forecasting.
    This combination links interpretability, market regime monitoring, and model-readiness diagnostics.
  </p>

  <h3>Code Highlight (Key Logic)</h3>
  <pre><code class="language-python">import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

# Moving averages (trend/regime signals)
prices["SPY_MA50"] = prices["SPY"].rolling(50).mean()
prices["SPY_MA200"] = prices["SPY"].rolling(200).mean()

# Decomposition (trend/seasonal/residual) — use trading-year seasonality
spy_series = prices["SPY"].dropna()
decomp = seasonal_decompose(spy_series, model="multiplicative", period=252)

# Stationarity check (returns typically closer to stationary than prices)
adf_stat, p_value, *_ = adfuller(daily_returns["SPY"].dropna())
print(f"ADF Statistic: {adf_stat:.3f}, p-value: {p_value:.4f}")</code></pre>

  <h3>Visualizations</h3>
  <img src="./outputs/figures/python_moving_averages.png" alt="SPY series with 50-day and 200-day moving averages" style="max-width:100%; height:auto; display:block; margin: 12px 0;">
  <p><em>Figure 1: Moving-average overlays used as lagging trend and regime confirmation signals.</em></p>

  <img src="./outputs/figures/python_time_series_decomposition.png" alt="Decomposed SPY time series into trend seasonal and residual components" style="max-width:100%; height:auto; display:block; margin: 12px 0;">
  <p><em>Figure 2: Multiplicative decomposition separating trend, seasonality, and residual shocks.</em></p>

  <h3>Key Insights</h3>
  <ul>
    <li>Trend was the dominant component in long-horizon SPY behavior.</li>
    <li>Seasonality appeared weaker and less explanatory than underlying trend.</li>
    <li>Residuals concentrated shock periods that standard trend views can hide.</li>
    <li>MA50/MA200 crossovers were useful but lagging regime indicators.</li>
    <li>Short-term reversals often emerged before moving-average confirmation.</li>
    <li>Return-series stationarity diagnostics are more appropriate than testing raw price levels alone.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li>Use moving averages as confirmation tools rather than primary entry timing signals.</li>
    <li>Treat large residual spikes as risk events requiring tighter exposure controls.</li>
    <li>Combine trend diagnostics with volatility and macro context for regime decisions.</li>
    <li>Prefer return-based modeling inputs when building predictive pipelines.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 5 &mdash; Forecasting</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">
  <h3>Business Question</h3>
  <p>
    Can a classical ARIMA baseline produce directionally useful out-of-sample SPY forecasts, and how should forecast
    uncertainty be interpreted for practical portfolio decision support?
  </p>

  <h3>Methodology</h3>
  <p>
    I applied an 80/20 chronological train-test split to preserve real forecasting order, then fit ARIMA(1,1,1) on
    the training segment. Predictions were generated for the full test horizon and evaluated with MAE and RMSE.
  </p>
  <p>
    Forecast intervals were included to represent uncertainty explicitly. This is important because market regime
    shifts and volatility clustering can quickly degrade point-forecast reliability.
  </p>

  <h3>Code Highlight (Key Logic)</h3>
  <pre><code class="language-python">import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error

prices = pd.read_csv("cleaned_prices_2015_2024.csv", index_col=0, parse_dates=True)
spy = prices["SPY"]

# Time-based split (80/20)
split = int(len(spy) * 0.8)
train, test = spy.iloc[:split], spy.iloc[split:]

# Fit ARIMA(1,1,1)
model = ARIMA(train, order=(1, 1, 1))
fit = model.fit()

# Forecast with intervals
fc = fit.get_forecast(steps=len(test))
pred = fc.predicted_mean
conf = fc.conf_int()  # lower/upper bounds

mae = mean_absolute_error(test, pred)
rmse = np.sqrt(mean_squared_error(test, pred))
print(f"MAE: ${mae:.2f} | RMSE: ${rmse:.2f}")</code></pre>

  <h3>Visualizations</h3>
  <img src="./outputs/figures/python_train_test_split.png" alt="SPY time-based train and test split" style="max-width:100%; height:auto; display:block; margin: 12px 0;">
  <p><em>Figure 1: Chronological train-test split used to evaluate realistic out-of-sample forecast performance.</em></p>

  <img src="./outputs/figures/python_arima_predictions.png" alt="ARIMA forecast compared with actual SPY prices" style="max-width:100%; height:auto; display:block; margin: 12px 0;">
  <p><em>Figure 2: ARIMA baseline predictions versus actual prices on the holdout window.</em></p>

  <h3>Key Insights</h3>
  <ul>
    <li>Forecasting price levels remained difficult despite a structured model setup.</li>
    <li>ARIMA served as a transparent baseline, not a final production model.</li>
    <li>Predictive accuracy degraded during sharp regime transitions.</li>
    <li>Point forecasts were most useful when interpreted with prediction intervals.</li>
    <li>Model error increased in high-volatility windows relative to calmer periods.</li>
    <li>Return and volatility forecasting are often more stable than direct price-level forecasting.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li>Keep ARIMA as a baseline benchmark in model comparison workflows.</li>
    <li>Add rolling retraining to adapt faster to evolving market structure.</li>
    <li>Prioritize interval-aware reporting over single-point forecast narratives.</li>
    <li>Evaluate return/volatility targets and exogenous features for improved robustness.</li>
  </ul>

</details>

---

## Key Findings & Recommendations

### Key Findings

- Over the 2015-2024 window, normalized price paths showed large dispersion in outcomes across assets, reinforcing that raw price levels are not comparable and that base-normalized views are essential for cross-asset performance interpretation.
- Return and risk were not aligned: the strongest cumulative growth came from higher-volatility equity exposure, while lower-volatility assets produced smoother but more modest outcomes, highlighting the core return-versus-stability trade-off in portfolio design.
- Risk-adjusted results and drawdown analysis showed that assets can post strong long-run returns while still experiencing severe interim losses, meaning investor experience is driven by path risk, not just endpoint performance.
- Correlation structure confirmed equity clustering (broad market, international equity, and sector equity moving together), which limits diversification if portfolios are built only from equity sleeves.
- Defensive assets behaved differently: long-duration Treasuries and gold provided lower or negative co-movement versus equities in parts of the sample, supporting their role as diversifiers rather than primary growth engines.
- Rolling-correlation analysis showed relationships are regime-dependent, with correlation spikes during stress periods; diversification remains valuable but can partially weaken when it is needed most.
- The diversified comparison portfolio demonstrated a practical diversification effect: materially lower volatility and shallower drawdowns with comparable risk-adjusted efficiency versus an all-equity benchmark.
- Trend diagnostics (moving averages and decomposition) indicated a persistent long-run upward regime in the benchmark series, interrupted by short-lived structural breaks (e.g., COVID shock), with trend dominating seasonal and residual components.
- Forecasting results showed a classical ARIMA baseline struggled to track the late-sample rally, illustrating that univariate linear models have limited ability to anticipate regime shifts and nonlinear market dynamics.

### Business Recommendations

- Build portfolios with intentional cross-regime diversification (equities + rates + real assets) rather than relying on multiple equity proxies that share the same latent risk factors.
- Pair return metrics with downside diagnostics (drawdown, volatility, and rolling correlations) in recurring risk reviews so allocation decisions reflect both performance and resilience.
- Operationalize correlation monitoring with rolling windows and stress-period overlays; treat correlation as time-varying and adjust risk budgets when co-movement begins to rise.
- Use classical models (like ARIMA) as statistical baselines, then benchmark richer alternatives (multivariate, regime-switching, and machine-learning/hybrid approaches) against that baseline.
- Adopt rolling retraining and walk-forward validation for forecasting workflows so models are repeatedly recalibrated as market regimes evolve.
- Communicate forecasts as ranges and scenarios, not point certainties, and explicitly disclose model limitations during structural breaks.
- Translate analytics into governance: define rebalance triggers, drawdown thresholds, and exception-based risk alerts to make insights actionable in live portfolio processes.


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
