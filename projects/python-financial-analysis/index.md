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

<details>
  <summary><strong>Analysis 1 &mdash; Data Acquisition &amp; Exploratory Data Analysis</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <!-- TODO: Replace placeholder text with actual business question -->
  <p>
    What are the fundamental characteristics of each asset's price history over the 2015&ndash;2024 period?
    How do the assets compare in terms of price levels, trading volume, and basic statistical properties?
  </p>

  <h3>Method</h3>
  <!-- TODO: Replace placeholder text with actual methodology -->
  <ul>
    <li>Retrieved daily OHLCV data for all six tickers using the yfinance API</li>
    <li>Cleaned and validated data for missing values, stock splits, and corporate actions</li>
    <li>Computed descriptive statistics (mean, median, standard deviation, skewness, kurtosis)</li>
    <li>Visualized price history trends and initial relationships between assets</li>
    <li>Generated correlation heatmap to identify preliminary asset relationships</li>
  </ul>

  <h3>Code</h3>
  <!-- TODO: Add actual code snippet from notebook 1 -->

```python
# Placeholder — will be replaced with actual analysis code
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

# Define tickers and time period
tickers = ['SPY', 'AAPL', 'XLE', 'TLT', 'GLD', 'EFA']
start_date = '2015-01-01'
end_date = '2024-12-31'

# Download data
data = yf.download(tickers, start=start_date, end=end_date)
prices = data['Adj Close']

# Descriptive statistics
print(prices.describe())
```

  <h3>Results</h3>

  <!-- TODO: Replace placeholder image with actual price history chart -->
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/python-price-history.png"
      alt="Price history chart for all six assets from 2015 to 2024"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Adjusted close price history for SPY, AAPL, XLE, TLT, GLD, and EFA (2015&ndash;2024).
      <span style="display:block; margin-top:4px;">
        <a href="images/python-price-history.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <!-- TODO: Replace placeholder image with actual descriptive statistics visualization -->
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/python-descriptive-stats.png"
      alt="Descriptive statistics summary for all six assets"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Descriptive statistics summary across all assets.
      <span style="display:block; margin-top:4px;">
        <a href="images/python-descriptive-stats.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <!-- TODO: Replace placeholder image with actual correlation heatmap -->
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/python-correlation-heatmap.png"
      alt="Initial correlation heatmap showing relationships between the six assets"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Initial correlation heatmap of daily returns across all assets.
      <span style="display:block; margin-top:4px;">
        <a href="images/python-correlation-heatmap.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Key Insights</h3>
  <!-- TODO: Replace placeholder insights with actual findings -->
  <ul>
    <li><strong>[TBD]:</strong> Placeholder insight about overall price trends observed across the 10-year period</li>
    <li><strong>[TBD]:</strong> Placeholder insight about relative performance differences between asset classes</li>
    <li><strong>[TBD]:</strong> Placeholder insight about data quality and any notable observations during EDA</li>
    <li><strong>[TBD]:</strong> Placeholder insight about initial correlation patterns between assets</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 2 &mdash; Returns &amp; Risk Metrics</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <!-- TODO: Replace placeholder text with actual business question -->
  <p>
    How do the six assets compare on a risk-adjusted basis? What are the cumulative return profiles, volatility
    characteristics, drawdown patterns, and risk-return tradeoffs for each asset over the analysis period?
  </p>

  <h3>Method</h3>
  <!-- TODO: Replace placeholder text with actual methodology -->
  <ul>
    <li>Calculated daily and annualized returns for each asset</li>
    <li>Computed risk metrics: annualized volatility, Sharpe ratio, maximum drawdown, Value at Risk (VaR)</li>
    <li>Plotted cumulative return curves to compare long-term growth trajectories</li>
    <li>Analyzed return distributions to assess normality, skewness, and tail risk</li>
    <li>Created risk-return scatter plot to visualize the efficient frontier relationship</li>
    <li>Computed and visualized drawdown profiles for each asset</li>
  </ul>

  <h3>Code</h3>
  <!-- TODO: Add actual code snippet from notebook 2 -->

```python
# Placeholder — will be replaced with actual analysis code
# Calculate daily returns
daily_returns = prices.pct_change().dropna()

# Annualized metrics
ann_return = daily_returns.mean() * 252
ann_volatility = daily_returns.std() * np.sqrt(252)
sharpe_ratio = ann_return / ann_volatility

# Cumulative returns
cumulative_returns = (1 + daily_returns).cumprod()

# Maximum drawdown
rolling_max = cumulative_returns.cummax()
drawdown = (cumulative_returns - rolling_max) / rolling_max
```

  <h3>Results</h3>

  <!-- TODO: Replace placeholder image with actual cumulative returns chart -->
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/python-cumulative-returns.png"
      alt="Cumulative returns chart for all six assets from 2015 to 2024"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Cumulative returns for all six assets over the 2015&ndash;2024 period.
      <span style="display:block; margin-top:4px;">
        <a href="images/python-cumulative-returns.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <!-- TODO: Replace placeholder image with actual return distributions -->
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/python-return-distributions.png"
      alt="Return distribution histograms for all six assets"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Daily return distributions showing the shape, spread, and tail behavior of each asset.
      <span style="display:block; margin-top:4px;">
        <a href="images/python-return-distributions.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <!-- TODO: Replace placeholder image with actual risk-return scatter plot -->
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/python-risk-return-scatter.png"
      alt="Risk-return scatter plot showing annualized return vs volatility for each asset"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Risk-return scatter plot: annualized return vs. annualized volatility for each asset.
      <span style="display:block; margin-top:4px;">
        <a href="images/python-risk-return-scatter.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <!-- TODO: Replace placeholder image with actual drawdown chart -->
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/python-drawdown-chart.png"
      alt="Maximum drawdown chart for all six assets"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Drawdown profiles showing peak-to-trough declines for each asset over time.
      <span style="display:block; margin-top:4px;">
        <a href="images/python-drawdown-chart.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Key Insights</h3>
  <!-- TODO: Replace placeholder insights with actual findings -->
  <ul>
    <li><strong>[TBD]:</strong> Placeholder insight about cumulative return differences across asset classes</li>
    <li><strong>[TBD]:</strong> Placeholder insight about risk-return tradeoffs and Sharpe ratio comparisons</li>
    <li><strong>[TBD]:</strong> Placeholder insight about drawdown severity and recovery patterns</li>
    <li><strong>[TBD]:</strong> Placeholder insight about return distribution characteristics (fat tails, skewness)</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 3 &mdash; Correlation &amp; Diversification</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <!-- TODO: Replace placeholder text with actual business question -->
  <p>
    How are the six assets correlated with each other, and how do those correlations change over time?
    Which asset pairs offer the best diversification benefits, and do correlations increase during market stress?
  </p>

  <h3>Method</h3>
  <!-- TODO: Replace placeholder text with actual methodology -->
  <ul>
    <li>Computed full-period correlation matrix of daily returns</li>
    <li>Calculated rolling correlations (e.g., 60-day and 252-day windows) to track relationship changes over time</li>
    <li>Created scatter plots for key asset pairs to visualize co-movement patterns</li>
    <li>Analyzed correlation stability across different market regimes (bull vs. bear markets)</li>
    <li>Identified diversification opportunities based on low or negative correlations</li>
  </ul>

  <h3>Code</h3>
  <!-- TODO: Add actual code snippet from notebook 3 -->

```python
# Placeholder — will be replaced with actual analysis code
# Full-period correlation matrix
correlation_matrix = daily_returns.corr()

# Rolling 60-day correlation between SPY and TLT
rolling_corr = daily_returns['SPY'].rolling(60).corr(daily_returns['TLT'])

# Visualize correlation heatmap
sns.heatmap(correlation_matrix, annot=True, cmap='RdBu_r', center=0)
plt.title('Asset Return Correlations')
```

  <h3>Results</h3>

  <!-- TODO: Replace placeholder image with actual correlation heatmap -->
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/python-correlation-heatmap-full.png"
      alt="Full-period correlation heatmap of daily returns"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Full-period correlation heatmap of daily returns across all six assets.
      <span style="display:block; margin-top:4px;">
        <a href="images/python-correlation-heatmap-full.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <!-- TODO: Replace placeholder image with actual rolling correlation chart -->
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/python-rolling-correlation.png"
      alt="Rolling correlation chart showing how asset correlations change over time"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Rolling correlations between key asset pairs over time, highlighting regime-dependent relationship changes.
      <span style="display:block; margin-top:4px;">
        <a href="images/python-rolling-correlation.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <!-- TODO: Replace placeholder image with actual scatter plots -->
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/python-pair-scatter-plots.png"
      alt="Scatter plots of daily returns for key asset pairs"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Asset pair scatter plots showing co-movement patterns and diversification relationships.
      <span style="display:block; margin-top:4px;">
        <a href="images/python-pair-scatter-plots.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Key Insights</h3>
  <!-- TODO: Replace placeholder insights with actual findings -->
  <ul>
    <li><strong>[TBD]:</strong> Placeholder insight about which asset pairs show strongest/weakest correlations</li>
    <li><strong>[TBD]:</strong> Placeholder insight about how correlations change during market stress periods</li>
    <li><strong>[TBD]:</strong> Placeholder insight about diversification effectiveness of bonds (TLT) and gold (GLD)</li>
    <li><strong>[TBD]:</strong> Placeholder insight about rolling correlation stability vs. instability</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 4 &mdash; Time Series Decomposition</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <!-- TODO: Replace placeholder text with actual business question -->
  <p>
    What are the underlying trend, seasonal, and residual components of each asset's price series?
    Can moving averages and regime analysis help identify structural shifts in market behavior?
  </p>

  <h3>Method</h3>
  <!-- TODO: Replace placeholder text with actual methodology -->
  <ul>
    <li>Applied classical and STL decomposition to separate trend, seasonal, and residual components</li>
    <li>Computed multiple moving averages (50-day, 200-day) to identify trend direction and crossovers</li>
    <li>Performed stationarity testing (ADF test, KPSS test) on price and return series</li>
    <li>Identified market regimes (bull/bear/sideways) using rolling statistics and volatility thresholds</li>
    <li>Analyzed ACF/PACF plots to understand autocorrelation structure</li>
  </ul>

  <h3>Code</h3>
  <!-- TODO: Add actual code snippet from notebook 4 -->

```python
# Placeholder — will be replaced with actual analysis code
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

# Decompose SPY price series
decomposition = seasonal_decompose(prices['SPY'], model='multiplicative', period=252)
decomposition.plot()

# Moving averages
prices['SPY_MA50'] = prices['SPY'].rolling(50).mean()
prices['SPY_MA200'] = prices['SPY'].rolling(200).mean()

# ADF stationarity test
result = adfuller(daily_returns['SPY'].dropna())
print(f'ADF Statistic: {result[0]}, p-value: {result[1]}')
```

  <h3>Results</h3>

  <!-- TODO: Replace placeholder image with actual decomposition plot -->
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/python-decomposition.png"
      alt="Time series decomposition showing trend, seasonal, and residual components"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Time series decomposition of SPY price data into trend, seasonal, and residual components.
      <span style="display:block; margin-top:4px;">
        <a href="images/python-decomposition.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <!-- TODO: Replace placeholder image with actual moving averages chart -->
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/python-moving-averages.png"
      alt="Price chart with 50-day and 200-day moving averages"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Price series with 50-day and 200-day moving averages highlighting trend direction and crossover signals.
      <span style="display:block; margin-top:4px;">
        <a href="images/python-moving-averages.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <!-- TODO: Replace placeholder image with actual market regimes chart -->
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/python-market-regimes.png"
      alt="Market regime identification showing bull, bear, and sideways periods"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Market regime identification highlighting bull, bear, and sideways periods across the analysis window.
      <span style="display:block; margin-top:4px;">
        <a href="images/python-market-regimes.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Key Insights</h3>
  <!-- TODO: Replace placeholder insights with actual findings -->
  <ul>
    <li><strong>[TBD]:</strong> Placeholder insight about dominant trends identified through decomposition</li>
    <li><strong>[TBD]:</strong> Placeholder insight about seasonal patterns in financial data</li>
    <li><strong>[TBD]:</strong> Placeholder insight about moving average crossover signals and their reliability</li>
    <li><strong>[TBD]:</strong> Placeholder insight about market regime characteristics and transitions</li>
  </ul>

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
