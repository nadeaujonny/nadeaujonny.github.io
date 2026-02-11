---
layout: default
title: Python Financial Analysis
description: "Portfolio project analyzing 10 years of financial market data using Python for time series analysis, risk metrics, and forecasting."
breadcrumbs:
  - title: Projects
    url: /projects/
  - title: Python Financial Analysis
---

<a href="/projects/" class="back-to-projects btn">&larr; Back to Projects</a>

# Python Financial Analysis

> Analyzing 10 years of financial market data (2015&ndash;2024) using Python for time series analysis, risk metrics, and forecasting across six diversified ETFs and stocks.

---

<details>
  <summary><strong>Project Overview</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Overview</h3>
  <p>
    This project demonstrates practical Python skills applied to financial market analysis. Using daily price data
    retrieved via the <strong>yfinance</strong> API for six diversified assets (SPY, AAPL, XLE, TLT, GLD, EFA),
    I perform exploratory analysis, risk assessment, time series modeling, and machine learning forecasting.
  </p>

  <h3>Dataset</h3>
  <table>
    <thead>
      <tr><th>Ticker</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td>SPY</td><td>S&amp;P 500 ETF (U.S. large-cap equities)</td></tr>
      <tr><td>AAPL</td><td>Apple Inc. (individual stock)</td></tr>
      <tr><td>XLE</td><td>Energy Select Sector SPDR (energy sector)</td></tr>
      <tr><td>TLT</td><td>iShares 20+ Year Treasury Bond ETF (long-term bonds)</td></tr>
      <tr><td>GLD</td><td>SPDR Gold Shares (gold/commodities)</td></tr>
      <tr><td>EFA</td><td>iShares MSCI EAFE ETF (international developed markets)</td></tr>
    </tbody>
  </table>
  <p>Data is retrieved programmatically via the <a href="https://github.com/ranaroussi/yfinance">yfinance</a> API &mdash; no static data files are included in this repository.</p>

</details>

<details>
  <summary><strong>Key Features</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <ul>
    <li><strong>API Integration</strong> &mdash; Automated data retrieval using yfinance</li>
    <li><strong>Time Series Analysis</strong> &mdash; Trend decomposition, rolling statistics, and stationarity testing</li>
    <li><strong>Risk Metrics</strong> &mdash; Volatility, Sharpe ratio, max drawdown, Value at Risk (VaR), and correlation analysis</li>
    <li><strong>Forecasting</strong> &mdash; ARIMA/SARIMA models and basic machine learning predictions</li>
    <li><strong>Visualization</strong> &mdash; Publication-quality charts and interactive plots</li>
  </ul>

</details>

<details>
  <summary><strong>Technologies Used</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <ul>
    <li><strong>Python 3.10+</strong></li>
    <li><strong>Jupyter Notebook</strong></li>
    <li><strong>pandas</strong> &mdash; data manipulation and analysis</li>
    <li><strong>NumPy</strong> &mdash; numerical computing</li>
    <li><strong>yfinance</strong> &mdash; financial data API</li>
    <li><strong>matplotlib</strong> &amp; <strong>seaborn</strong> &mdash; data visualization</li>
    <li><strong>statsmodels</strong> &mdash; time series modeling and statistical tests</li>
    <li><strong>SciPy</strong> &mdash; scientific computing and statistical functions</li>
    <li><strong>scikit-learn</strong> &mdash; machine learning models</li>
  </ul>

</details>

<details>
  <summary><strong>Analysis Pipeline</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <table>
    <thead>
      <tr><th>Phase</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td>01 &mdash; Data Collection</td><td>Retrieve and clean 10 years of daily price data using yfinance</td></tr>
      <tr><td>02 &mdash; Exploratory Analysis</td><td>Summary statistics, distributions, and trend visualizations</td></tr>
      <tr><td>03 &mdash; Risk Analysis</td><td>Volatility, drawdowns, Sharpe ratios, VaR, and correlation matrices</td></tr>
      <tr><td>04 &mdash; Time Series Modeling</td><td>Stationarity tests, ACF/PACF analysis, ARIMA/SARIMA forecasting</td></tr>
      <tr><td>05 &mdash; Machine Learning</td><td>Regression and classification models for return prediction</td></tr>
    </tbody>
  </table>

</details>

---

### Key Findings

*To be updated after analysis is complete.*
