---
layout: default
title: "Python Financial Analysis: Portfolio Performance & Risk (2015-2024)"
description: "Portfolio performance and risk analysis of six diversified assets (2015-2024) using Python — time series analysis, risk metrics, correlation studies, and predictive modeling."
---

<a href="/projects/" class="back-to-projects btn">&larr; Back to Projects</a>

# Python Financial Analysis: Portfolio Performance &amp; Risk (2015&ndash;2024)

> Time series analysis, risk metrics, and predictive modeling across six diversified assets using 10 years of daily market data retrieved via the yfinance API.

**Tools:** Python &middot; pandas &middot; NumPy &middot; matplotlib &middot; seaborn &middot; statsmodels &middot; scikit-learn &middot; yfinance &middot; Jupyter Notebook

---

<details class="dropdown-section">
  <summary><strong>Project Overview</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Overview</h3>
  <p>
    This project analyzes 10 years of daily financial market data (2015&ndash;2024) for a diversified portfolio of six assets
    to evaluate historical performance, quantify risk, identify diversification opportunities, and generate short-term
    forecasts. The analysis simulates the role of a data analyst supporting portfolio management and investment
    decision-making with data-driven insights.
  </p>

  <h3>Business Context</h3>
  <p>
    Understanding portfolio risk and return characteristics is essential for informed investment decisions. This project
    demonstrates how Python and statistical methods can be applied to real market data to move beyond intuition and
    toward evidence-based portfolio evaluation &mdash; covering volatility measurement, drawdown analysis, correlation
    dynamics, and predictive modeling.
  </p>

  <h3>Objectives</h3>
  <ul>
    <li>Retrieve and validate 10 years of daily market data via the yfinance API</li>
    <li>Compute risk-adjusted performance metrics (Sharpe ratio, maximum drawdown, annualized volatility)</li>
    <li>Analyze cross-asset correlations and quantify diversification benefits</li>
    <li>Decompose time series into trend, seasonality, and residual components</li>
    <li>Build and evaluate an ARIMA baseline forecast for the benchmark index</li>
    <li>Produce publication-quality visualizations for each stage of analysis</li>
  </ul>

  <h3>Skills Demonstrated</h3>
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
<details class="dropdown-section">
  <summary><strong>Dataset</strong></summary>

  <div style="margin-top: 12px;"></div>

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
  <table>
    <thead>
      <tr><th>Attribute</th><th>Value</th></tr>
    </thead>
    <tbody>
      <tr><td>Start</td><td>January 1, 2015</td></tr>
      <tr><td>End</td><td>December 31, 2024</td></tr>
      <tr><td>Granularity</td><td>Daily trading data (~2,500 trading days per asset)</td></tr>
      <tr><td>Total Observations</td><td>~15,000 daily records across 6 assets</td></tr>
    </tbody>
  </table>

  <h3>Rationale for Asset Selection</h3>
  <p>
    These six assets were chosen to represent a diversified portfolio spanning domestic equities (SPY), individual
    growth stocks (AAPL), sector exposure (XLE), fixed income (TLT), commodities (GLD), and international markets
    (EFA). This mix enables meaningful analysis of cross-asset correlations, diversification benefits, and
    risk-return tradeoffs across different market environments.
  </p>

</details>
<details class="dropdown-section">
  <summary><strong>Analysis 1 &mdash; Data Acquisition &amp; Exploratory Data Analysis</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Business Question</h3>
  <p>
    What are the fundamental characteristics of each asset's price history over the 2015&ndash;2024 period?
    How do the assets compare in terms of price levels, growth trajectories, and basic statistical properties,
    and what preliminary relationships exist between them?
  </p>

  <h3>Methodology</h3>
  <p>
    Using the <a href="https://github.com/ranaroussi/yfinance" target="_blank" rel="noopener">yfinance</a> Python library,
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

  <h3>Code Highlight</h3>

<pre><code class="language-python"># Define portfolio assets
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

# Normalize to base 100 for cross-asset comparison
normalized = (prices / prices.iloc[0]) * 100</code></pre>

  <h3>Results</h3>

  <figure style="margin: 0 0 18px 0;">
    <img src="./outputs/figures/python_price_history_10years.png" alt="Normalized 10-year price history for all six portfolio assets" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Normalized price history (base = 100) for all six assets, 2015&ndash;2024.
      <span style="display:block; margin-top:4px;"><a href="./outputs/figures/python_price_history_10years.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="./outputs/figures/python_correlation_heatmap.png" alt="Correlation heatmap of daily returns across six assets" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Pairwise correlation heatmap of daily returns, highlighting diversification opportunities.
      <span style="display:block; margin-top:4px;"><a href="./outputs/figures/python_correlation_heatmap.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>Massive performance divergence:</strong> AAPL gained approximately 935% over the 10-year period, far outpacing SPY at 240%, while TLT (long-term bonds) lost roughly 11% &mdash; highlighting the enormous spread in outcomes across asset classes.</li>
    <li><strong>100% data completeness:</strong> All 2,515 trading days across all six tickers contained valid price data with zero missing values, confirming the reliability of the yfinance API for historical financial data retrieval.</li>
    <li><strong>Bonds as a diversifier:</strong> TLT showed negative correlation with equity assets (approximately &minus;0.35 vs. SPY), confirming its role as a portfolio diversification tool that tends to move inversely to stocks during market stress.</li>
    <li><strong>Equity clustering:</strong> SPY, AAPL, XLE, and EFA exhibited moderate-to-strong positive correlations (0.50&ndash;0.80), indicating that equity assets across sectors and geographies share common risk factors.</li>
    <li><strong>Gold&rsquo;s independence:</strong> GLD displayed low correlation with both equities (~0.05) and bonds (~0.10), providing a distinct return driver relatively uncoupled from traditional asset class movements.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Normalize for comparison:</strong> always use base-100 indexing when comparing assets with different price levels to avoid misleading visual interpretation.</li>
    <li><strong>Use correlations as a starting point:</strong> preliminary correlations guide portfolio construction, but should be confirmed with rolling windows (see Analysis 3).</li>
    <li><strong>Validate before analyzing:</strong> confirming data completeness and quality before downstream analysis prevents compounding errors through the pipeline.</li>
  </ul>

</details>
<details class="dropdown-section">
  <summary><strong>Analysis 2 &mdash; Returns &amp; Risk Analysis</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Business Question</h3>
  <p>
    Which assets delivered the best risk-adjusted returns over 2015&ndash;2024, and where were the largest downside
    episodes that could challenge portfolio durability?
  </p>

  <h3>Methodology</h3>
  <p>
    Daily percentage returns were computed from adjusted close prices so every asset could be compared on a common scale.
    I then annualized return and volatility (using the &radic;252 convention), applied a 2% risk-free assumption for Sharpe
    ratio calculation, and ranked assets by risk-adjusted efficiency.
  </p>
  <p>
    To measure downside risk, I calculated maximum drawdown from each asset&rsquo;s cumulative return path. This complements
    volatility by showing the worst peak-to-trough loss and highlights stress behavior during sharp market shocks
    (e.g., the 2020 COVID crash and the 2022 rate-hike selloff).
  </p>

  <h3>Code Highlight</h3>

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
    """Annualized return, volatility, Sharpe, max drawdown."""
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

metrics_df = risk_metrics(daily_returns, rf=0.02)</code></pre>

  <h3>Results</h3>

  <h4>Risk Metrics Summary</h4>
  <table>
    <thead>
      <tr><th>Asset</th><th>Annual Return</th><th>Annual Volatility</th><th>Sharpe Ratio</th><th>Max Drawdown</th></tr>
    </thead>
    <tbody>
      <tr><td>AAPL</td><td>~26%</td><td>~30%</td><td>~0.80</td><td>~&minus;39%</td></tr>
      <tr><td>SPY</td><td>~13%</td><td>~18%</td><td>~0.61</td><td>~&minus;34%</td></tr>
      <tr><td>GLD</td><td>~8%</td><td>~15%</td><td>~0.40</td><td>~&minus;21%</td></tr>
      <tr><td>EFA</td><td>~6%</td><td>~17%</td><td>~0.24</td><td>~&minus;35%</td></tr>
      <tr><td>XLE</td><td>~4%</td><td>~30%</td><td>~0.07</td><td>~&minus;62%</td></tr>
      <tr><td>TLT</td><td>~&minus;1%</td><td>~16%</td><td>~&minus;0.19</td><td>~&minus;48%</td></tr>
    </tbody>
  </table>
  <p style="font-size:0.9em; color:#555;">Values are approximate annualized figures over the full 2015&ndash;2024 period. Sharpe ratio assumes a 2% risk-free rate.</p>

  <figure style="margin: 0 0 18px 0;">
    <img src="./outputs/figures/python_risk_return_scatter.png" alt="Risk-return scatter plot showing annualized return versus volatility" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Annualized return versus volatility for each asset &mdash; assets in the upper-left quadrant offer the best risk-adjusted positioning.
      <span style="display:block; margin-top:4px;"><a href="./outputs/figures/python_risk_return_scatter.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="./outputs/figures/python_cumulative_returns.png" alt="Cumulative returns for all six portfolio assets" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Cumulative return paths showing the growth trajectory and volatility profile of each asset.
      <span style="display:block; margin-top:4px;"><a href="./outputs/figures/python_cumulative_returns.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="./outputs/figures/python_maximum_drawdown.png" alt="Maximum drawdown trajectories for each asset" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Drawdown trajectories showing each asset&rsquo;s worst historical peak-to-trough declines.
      <span style="display:block; margin-top:4px;"><a href="./outputs/figures/python_maximum_drawdown.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>AAPL led on both return and Sharpe:</strong> ~26% annualized return with a Sharpe of ~0.80, but carried ~30% volatility and a ~39% max drawdown &mdash; high reward came with substantial interim risk.</li>
    <li><strong>XLE: high volatility, low reward:</strong> ~30% annualized volatility (matching AAPL) but only ~4% return and a devastating ~62% max drawdown, making it the worst risk-adjusted performer.</li>
    <li><strong>TLT lost money over the decade:</strong> long-duration Treasuries posted a negative annualized return (~&minus;1%) with a ~48% drawdown during the 2022 rate cycle, challenging the traditional "safe haven" narrative.</li>
    <li><strong>GLD was the most stable diversifier:</strong> lowest max drawdown (~21%) among all assets with a positive Sharpe ratio, reinforcing gold&rsquo;s defensive role.</li>
    <li><strong>Synchronized stress windows:</strong> drawdown paths for SPY, EFA, and XLE overlapped sharply during the March 2020 COVID crash, demonstrating correlated equity risk during crises.</li>
    <li><strong>Risk metrics tell different stories:</strong> volatility alone underestimates tail risk &mdash; TLT had moderate volatility (~16%) but a severe drawdown (~48%), showing that Sharpe and drawdown should be evaluated together.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Use Sharpe and drawdown together:</strong> screen and rebalance portfolio weights using risk-adjusted return alongside maximum drawdown tolerance.</li>
    <li><strong>Set drawdown-based risk limits:</strong> define acceptable peak-to-trough loss thresholds, not only annual volatility targets.</li>
    <li><strong>Stress-test allocations:</strong> evaluate how portfolio weights would have performed during the 2020 and 2022 stress episodes before implementing changes.</li>
    <li><strong>Reassess periodically:</strong> risk metrics evolve as market regimes shift &mdash; a strong Sharpe in one decade does not guarantee the next.</li>
  </ul>

</details>
<details class="dropdown-section">
  <summary><strong>Analysis 3 &mdash; Correlation &amp; Diversification</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Business Question</h3>
  <p>
    How stable are cross-asset correlations over time, and how much risk reduction can be achieved by combining assets
    with lower co-movement instead of concentrating in a single market exposure?
  </p>

  <h3>Methodology</h3>
  <p>
    I computed full-period pairwise correlations on daily returns, then layered 252-day (one trading year) rolling
    correlation windows to track how relationships shifted across calm and stress environments. This distinguishes
    long-run averages from regime-specific behavior that matters for real-time risk management.
  </p>
  <p>
    I also quantified the diversification benefit by comparing the annualized volatility of a concentrated SPY-only
    portfolio against a diversified allocation (60% SPY, 30% TLT, 10% GLD) using covariance matrix math.
  </p>

  <h3>Code Highlight</h3>

<pre><code class="language-python">import numpy as np
import pandas as pd

# Static correlation (full period)
corr = daily_returns.corr()

# Rolling 252-day correlation (regime sensitivity)
rolling_corr_spy_tlt = daily_returns["SPY"].rolling(252).corr(daily_returns["TLT"])

# Diversification math: portfolio volatility via covariance
cov = daily_returns.cov() * 252  # annualized covariance

w_concentrated = np.array([1, 0, 0])               # SPY only
w_diversified = np.array([0.6, 0.3, 0.1])           # SPY / TLT / GLD

assets = ["SPY", "TLT", "GLD"]
cov_3 = cov.loc[assets, assets].values

vol_concentrated = np.sqrt(w_concentrated.T @ cov_3 @ w_concentrated)
vol_diversified = np.sqrt(w_diversified.T @ cov_3 @ w_diversified)</code></pre>

  <h3>Results</h3>

  <h4>Key Pairwise Correlations (Full Period)</h4>
  <table>
    <thead>
      <tr><th>Asset Pair</th><th>Correlation</th><th>Interpretation</th></tr>
    </thead>
    <tbody>
      <tr><td>SPY &ndash; AAPL</td><td>~0.80</td><td>Strong positive (equity clustering)</td></tr>
      <tr><td>SPY &ndash; EFA</td><td>~0.75</td><td>Strong positive (global equity co-movement)</td></tr>
      <tr><td>SPY &ndash; XLE</td><td>~0.55</td><td>Moderate positive (sector link)</td></tr>
      <tr><td>SPY &ndash; TLT</td><td>~&minus;0.35</td><td>Negative (stock-bond diversification)</td></tr>
      <tr><td>SPY &ndash; GLD</td><td>~0.05</td><td>Near zero (independent return driver)</td></tr>
      <tr><td>TLT &ndash; GLD</td><td>~0.10</td><td>Near zero (distinct safe-haven profiles)</td></tr>
    </tbody>
  </table>

  <h4>Diversification Benefit</h4>
  <table>
    <thead>
      <tr><th>Portfolio</th><th>Weights</th><th>Annualized Volatility</th></tr>
    </thead>
    <tbody>
      <tr><td>Concentrated</td><td>100% SPY</td><td>~18.5%</td></tr>
      <tr><td>Diversified</td><td>60% SPY / 30% TLT / 10% GLD</td><td>~12.0%</td></tr>
    </tbody>
  </table>
  <p style="font-size:0.9em; color:#555;">Diversification reduced annualized portfolio volatility by approximately 35% relative to SPY-only.</p>

  <figure style="margin: 0 0 18px 0;">
    <img src="./outputs/figures/python_correlation_heatmap_detailed.png" alt="Detailed correlation heatmap of portfolio asset returns" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Full-period return correlation matrix for baseline diversification assessment.
      <span style="display:block; margin-top:4px;"><a href="./outputs/figures/python_correlation_heatmap_detailed.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="./outputs/figures/python_rolling_correlations.png" alt="Rolling 252-day correlations across selected asset pairs" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Rolling 252-day correlations showing regime-dependent shifts in cross-asset relationships.
      <span style="display:block; margin-top:4px;"><a href="./outputs/figures/python_rolling_correlations.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="./outputs/figures/python_diversification_benefit.png" alt="Volatility comparison between concentrated and diversified portfolio" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Annualized volatility comparison illustrating the risk reduction from a diversified allocation.
      <span style="display:block; margin-top:4px;"><a href="./outputs/figures/python_diversification_benefit.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>~35% volatility reduction from diversification:</strong> the three-asset portfolio (SPY/TLT/GLD) achieved ~12% annualized volatility versus ~18.5% for SPY alone, demonstrating the practical benefit of combining low-correlated assets.</li>
    <li><strong>Equity correlations cluster above 0.50:</strong> SPY, AAPL, EFA, and XLE moved together, meaning additional equity-only positions provide limited diversification benefit.</li>
    <li><strong>SPY&ndash;TLT correlation was regime-dependent:</strong> rolling windows showed the negative correlation weakened and occasionally turned positive during the 2022 rate-hike environment, meaning the stock-bond hedge is not guaranteed.</li>
    <li><strong>Gold remained the most independent asset:</strong> GLD correlations stayed near zero across both calm and stress periods, making it the most reliable diversifier in the portfolio.</li>
    <li><strong>Correlations spiked during crises:</strong> the March 2020 selloff saw equity correlations converge upward, partially reducing diversification benefits precisely when they are needed most.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Monitor rolling correlations continuously:</strong> treat correlation as time-varying and adjust risk budgets when co-movement begins to rise.</li>
    <li><strong>Diversify across risk drivers, not just tickers:</strong> adding more equity ETFs provides less benefit than combining equities with bonds and commodities.</li>
    <li><strong>Use covariance-based targets:</strong> rebalance using portfolio volatility targets rather than static weight rules to adapt to changing correlations.</li>
    <li><strong>Plan for correlation breakdown:</strong> build allocations that anticipate temporary loss of the stock-bond hedge during rate-driven environments.</li>
  </ul>

</details>
<details class="dropdown-section">
  <summary><strong>Analysis 4 &mdash; Time Series Decomposition</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Business Question</h3>
  <p>
    What components drive SPY price movement over time, and how can trend, seasonality, and residual shocks be
    separated to support clearer regime interpretation and forecasting readiness?
  </p>

  <h3>Methodology</h3>
  <p>
    I used 50-day and 200-day moving averages as practical regime indicators (the "golden cross" and "death cross"
    framework), then decomposed the SPY series into trend, seasonal, and residual components using multiplicative
    seasonal decomposition with a 252-day (one trading year) periodicity.
  </p>
  <p>
    An Augmented Dickey-Fuller (ADF) test was run on SPY daily returns to confirm stationarity &mdash; a prerequisite
    for the ARIMA modeling in Analysis 5. This combination links visual regime interpretation, structural decomposition,
    and statistical model-readiness diagnostics.
  </p>

  <h3>Code Highlight</h3>

<pre><code class="language-python">import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

# Moving averages (trend/regime signals)
prices["SPY_MA50"] = prices["SPY"].rolling(50).mean()
prices["SPY_MA200"] = prices["SPY"].rolling(200).mean()

# Multiplicative decomposition (trend/seasonal/residual)
spy_series = prices["SPY"].dropna()
decomp = seasonal_decompose(spy_series, model="multiplicative", period=252)

# Stationarity check on returns (not prices)
adf_stat, p_value, *_ = adfuller(daily_returns["SPY"].dropna())
print(f"ADF Statistic: {adf_stat:.3f}, p-value: {p_value:.4f}")</code></pre>

  <h3>Results</h3>

  <h4>Stationarity Test</h4>
  <table>
    <thead>
      <tr><th>Series</th><th>ADF Statistic</th><th>p-value</th><th>Conclusion</th></tr>
    </thead>
    <tbody>
      <tr><td>SPY daily returns</td><td>&lt; &minus;20</td><td>&lt; 0.001</td><td>Stationary (reject unit root)</td></tr>
    </tbody>
  </table>
  <p style="font-size:0.9em; color:#555;">Daily returns are stationary; raw price levels are not. This confirms return-based inputs are appropriate for ARIMA modeling.</p>

  <figure style="margin: 0 0 18px 0;">
    <img src="./outputs/figures/python_moving_averages.png" alt="SPY price with 50-day and 200-day moving averages overlaid" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      SPY with 50-day and 200-day moving averages. Crossovers indicate regime transitions (golden cross / death cross).
      <span style="display:block; margin-top:4px;"><a href="./outputs/figures/python_moving_averages.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="./outputs/figures/python_time_series_decomposition.png" alt="Multiplicative decomposition of SPY into trend, seasonal, and residual components" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Multiplicative decomposition separating SPY into trend, seasonal, and residual components (252-day periodicity).
      <span style="display:block; margin-top:4px;"><a href="./outputs/figures/python_time_series_decomposition.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>Trend dominated long-horizon behavior:</strong> the trend component showed a persistent upward trajectory interrupted by sharp structural breaks (COVID crash in March 2020, rate-driven selloff in 2022).</li>
    <li><strong>Seasonality was weak and inconsistent:</strong> the seasonal component contributed far less explanatory power than trend, suggesting that calendar-based patterns are not reliable signals for equity forecasting.</li>
    <li><strong>Residuals concentrated shock events:</strong> the residual component captured crisis-period spikes that standard trend views hide &mdash; useful for identifying stress regimes.</li>
    <li><strong>MA crossovers lagged regime shifts:</strong> the 50/200-day moving average crossovers confirmed trend changes but typically lagged actual price reversals by several weeks.</li>
    <li><strong>Returns were strongly stationary:</strong> ADF test p-value &lt; 0.001, confirming that return-based modeling inputs (not raw prices) are appropriate for downstream ARIMA forecasting.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Use moving averages as confirmation, not prediction:</strong> MA crossovers are useful for validating regime changes but should not be used as primary timing signals.</li>
    <li><strong>Monitor residual spikes as risk alerts:</strong> large residual deviations can serve as early-warning signals for tighter exposure controls.</li>
    <li><strong>Combine trend with macro context:</strong> trend diagnostics are most valuable when paired with volatility analysis and economic indicators.</li>
    <li><strong>Model returns, not prices:</strong> stationarity testing confirms that return-based inputs produce more reliable forecasting pipelines.</li>
  </ul>

</details>
<details class="dropdown-section">
  <summary><strong>Analysis 5 &mdash; Forecasting (ARIMA Baseline)</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Business Question</h3>
  <p>
    Can a classical ARIMA model produce directionally useful out-of-sample SPY price forecasts, and how should
    forecast uncertainty be interpreted for practical portfolio decision support?
  </p>

  <h3>Methodology</h3>
  <p>
    I applied a chronological 80/20 train-test split to preserve realistic forecasting order (no future data leakage),
    then fit an ARIMA(1,1,1) model on the training segment. Predictions were generated for the full test horizon
    (~500 trading days) and evaluated with MAE and RMSE.
  </p>
  <p>
    Confidence intervals were included to represent uncertainty explicitly. This is critical because market regime
    shifts and volatility clustering can quickly degrade point-forecast reliability &mdash; forecasts should always
    be communicated as ranges, not certainties.
  </p>

  <h3>Code Highlight</h3>

<pre><code class="language-python">import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error

spy = prices["SPY"]

# Chronological train-test split (80/20)
split = int(len(spy) * 0.8)
train, test = spy.iloc[:split], spy.iloc[split:]

# Fit ARIMA(1,1,1)
model = ARIMA(train, order=(1, 1, 1))
fit = model.fit()

# Forecast with confidence intervals
fc = fit.get_forecast(steps=len(test))
pred = fc.predicted_mean
conf = fc.conf_int()  # lower/upper bounds

mae = mean_absolute_error(test, pred)
rmse = np.sqrt(mean_squared_error(test, pred))
print(f"MAE: ${mae:.2f} | RMSE: ${rmse:.2f}")</code></pre>

  <h3>Results</h3>

  <h4>Forecast Error Metrics</h4>
  <table>
    <thead>
      <tr><th>Metric</th><th>Value</th><th>Interpretation</th></tr>
    </thead>
    <tbody>
      <tr><td>MAE</td><td>Moderate</td><td>Average absolute prediction error across the test window</td></tr>
      <tr><td>RMSE</td><td>Higher than MAE</td><td>Penalizes large errors &mdash; confirms forecast degradation during volatile periods</td></tr>
      <tr><td>Train/Test Split</td><td>80% / 20%</td><td>~2,012 train days / ~503 test days</td></tr>
      <tr><td>Model Order</td><td>ARIMA(1,1,1)</td><td>First-order autoregressive + differencing + moving average</td></tr>
    </tbody>
  </table>

  <figure style="margin: 0 0 18px 0;">
    <img src="./outputs/figures/python_train_test_split.png" alt="SPY chronological train-test split visualization" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Chronological 80/20 train-test split used to evaluate out-of-sample forecast performance.
      <span style="display:block; margin-top:4px;"><a href="./outputs/figures/python_train_test_split.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="./outputs/figures/python_arima_predictions.png" alt="ARIMA forecast versus actual SPY prices on the test set" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      ARIMA(1,1,1) predictions versus actual SPY prices on the holdout window, with confidence intervals.
      <span style="display:block; margin-top:4px;"><a href="./outputs/figures/python_arima_predictions.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>ARIMA captured the general trend direction:</strong> the model correctly identified the upward drift in SPY over the test period, but could not anticipate the magnitude or timing of the late-sample rally.</li>
    <li><strong>Point forecasts degraded during regime shifts:</strong> prediction error increased substantially during high-volatility windows, confirming that univariate linear models struggle with nonlinear market dynamics.</li>
    <li><strong>Confidence intervals widened rapidly:</strong> forecast uncertainty grew quickly over longer horizons, meaning ARIMA is most useful for short-term directional guidance, not multi-month point predictions.</li>
    <li><strong>RMSE exceeded MAE meaningfully:</strong> the gap indicates that a small number of large errors (during volatile periods) disproportionately drove total forecast error.</li>
    <li><strong>Baseline benchmark, not production model:</strong> ARIMA(1,1,1) serves as a transparent, interpretable baseline against which richer models (multivariate, regime-switching, machine learning) should be benchmarked.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Keep ARIMA as a baseline:</strong> use it as a reference point in model comparison workflows &mdash; any production model should demonstrably outperform this benchmark.</li>
    <li><strong>Add rolling retraining:</strong> retrain the model on a rolling window to adapt faster to evolving market structure and reduce drift in predictions.</li>
    <li><strong>Communicate forecasts as ranges:</strong> always report prediction intervals alongside point estimates &mdash; single-number forecasts create false confidence.</li>
    <li><strong>Explore richer alternatives:</strong> test multivariate models (VAR), regime-switching models, and machine learning approaches against this ARIMA baseline to quantify incremental improvement.</li>
  </ul>

</details>
<details class="dropdown-section">
  <summary><strong>Key Findings &amp; Recommendations</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Key Findings</h3>
  <ul>
    <li><strong>Massive performance dispersion:</strong> over 2015&ndash;2024, AAPL returned ~935% while TLT lost ~11%, reinforcing that raw price levels are not comparable and base-normalized views are essential for cross-asset interpretation.</li>
    <li><strong>Return and risk are fundamentally linked:</strong> the strongest cumulative growth (AAPL, SPY) came from higher-volatility equity exposure, while lower-volatility assets (GLD) produced smoother but more modest outcomes.</li>
    <li><strong>Path risk matters as much as endpoint return:</strong> XLE and TLT posted severe interim drawdowns (~62% and ~48%) that would challenge real investor behavior, even where long-run returns appeared acceptable.</li>
    <li><strong>Equity correlations limit within-class diversification:</strong> SPY, AAPL, EFA, and XLE correlated between 0.50&ndash;0.80, meaning equity-only portfolios carry concentrated risk.</li>
    <li><strong>Cross-asset diversification worked:</strong> a 60/30/10 SPY/TLT/GLD portfolio achieved ~35% lower volatility than SPY alone, demonstrating practical diversification benefit.</li>
    <li><strong>Correlations are regime-dependent:</strong> rolling analysis showed the SPY&ndash;TLT negative correlation weakened during the 2022 rate-hike environment and equity correlations spiked during the 2020 crisis.</li>
    <li><strong>Trend dominated SPY structure:</strong> time series decomposition confirmed a persistent long-run upward trend interrupted by short-lived structural breaks, with seasonality contributing minimal explanatory power.</li>
    <li><strong>Forecasting price levels remains difficult:</strong> the ARIMA baseline captured directional trend but could not anticipate regime shifts, confirming that univariate models have limited predictive power for multi-month horizons.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Build cross-regime portfolios:</strong> combine equities, rates, and real assets rather than relying on multiple equity proxies that share the same latent risk factors.</li>
    <li><strong>Pair return metrics with downside diagnostics:</strong> include drawdown, rolling correlation, and volatility in recurring risk reviews &mdash; not just return and Sharpe.</li>
    <li><strong>Operationalize correlation monitoring:</strong> use rolling windows and stress-period overlays as an ongoing risk dashboard, not a one-time diagnostic.</li>
    <li><strong>Use classical models as baselines:</strong> benchmark richer alternatives (multivariate, regime-switching, machine learning) against transparent ARIMA baselines.</li>
    <li><strong>Adopt rolling retraining for forecasting:</strong> walk-forward validation ensures models are recalibrated as market regimes evolve.</li>
    <li><strong>Communicate forecasts as ranges:</strong> report prediction intervals and disclose model limitations during structural breaks &mdash; never present single-point forecasts as certainties.</li>
    <li><strong>Translate analytics into governance:</strong> define rebalance triggers, drawdown thresholds, and exception-based risk alerts to make insights actionable in live portfolio processes.</li>
  </ul>

</details>
<details class="dropdown-section">
  <summary><strong>Technical Details</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Libraries Used</h3>
  <table>
    <thead>
      <tr><th>Library</th><th>Purpose</th></tr>
    </thead>
    <tbody>
      <tr><td>Python 3.10+</td><td>Runtime environment</td></tr>
      <tr><td>pandas</td><td>Data manipulation and analysis</td></tr>
      <tr><td>NumPy</td><td>Numerical computing</td></tr>
      <tr><td>yfinance</td><td>Yahoo Finance API for market data retrieval</td></tr>
      <tr><td>matplotlib</td><td>Static data visualization</td></tr>
      <tr><td>seaborn</td><td>Statistical data visualization</td></tr>
      <tr><td>statsmodels</td><td>Time series analysis, decomposition, ARIMA, statistical tests</td></tr>
      <tr><td>SciPy</td><td>Scientific computing and statistical functions</td></tr>
      <tr><td>scikit-learn</td><td>Machine learning models and evaluation metrics</td></tr>
      <tr><td>Jupyter Notebook</td><td>Interactive analysis environment</td></tr>
    </tbody>
  </table>

  <h3>How to Reproduce</h3>
  <ol>
    <li>Clone the repository: <code>git clone https://github.com/nadeaujonny/nadeaujonny.github.io.git</code></li>
    <li>Navigate to the project: <code>cd projects/python-financial-analysis</code></li>
    <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
    <li>Run the notebooks in order (01 through 05) in Jupyter</li>
    <li>Charts and outputs will be saved to the <code>outputs/</code> directory</li>
  </ol>

  <h3>Project Structure</h3>
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
├── outputs/                  # Generated outputs and exports
│   └── figures/              # Charts and visualizations
└── .gitignore                # Excludes data files
</code></pre>

</details>
