# Python Financial Analysis

Portfolio project analyzing 10 years of financial market data using Python for time series analysis, risk metrics, and forecasting.

## Dataset

This project analyzes daily price data for six diversified ETFs and stocks spanning 2015–2024:

| Ticker | Description |
|--------|-------------|
| SPY | S&P 500 ETF (U.S. large-cap equities) |
| AAPL | Apple Inc. (individual stock) |
| XLE | Energy Select Sector SPDR (energy sector) |
| TLT | iShares 20+ Year Treasury Bond ETF (long-term bonds) |
| GLD | SPDR Gold Shares (gold/commodities) |
| EFA | iShares MSCI EAFE ETF (international developed markets) |

Data is retrieved programmatically via the [yfinance](https://github.com/ranaroussi/yfinance) API — no static data files are included in this repository.

## Key Features

- **API Integration** — Automated data retrieval using yfinance
- **Time Series Analysis** — Trend decomposition, rolling statistics, and stationarity testing
- **Risk Metrics** — Volatility, Sharpe ratio, max drawdown, Value at Risk (VaR), and correlation analysis
- **Forecasting** — ARIMA/SARIMA models and basic machine learning predictions
- **Visualization** — Publication-quality charts and interactive plots

## Technologies Used

- **Python 3.10+**
- **Jupyter Notebook**
- **pandas** — data manipulation and analysis
- **NumPy** — numerical computing
- **yfinance** — financial data API
- **matplotlib** & **seaborn** — data visualization
- **statsmodels** — time series modeling and statistical tests
- **SciPy** — scientific computing and statistical functions
- **scikit-learn** — machine learning models

## Project Structure

```
python-financial-analysis/
├── notebooks/           # Jupyter notebooks for each analysis phase
├── data/
│   ├── raw/             # Raw downloaded data (not committed)
│   └── processed/       # Cleaned and transformed data (not committed)
├── outputs/
│   └── figures/         # Generated charts and visualizations
├── README.md
├── requirements.txt
├── .gitignore
└── .gitattributes
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/nadeaujonny/python-financial-analysis.git
cd python-financial-analysis
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Launch Jupyter Notebook and open any notebook in the `notebooks/` folder:

```bash
jupyter notebook
```

Run the notebooks in order for the full analysis pipeline, or open any individual notebook to explore a specific topic.

## Analysis Overview

| Notebook | Description |
|----------|-------------|
| 01 — Data Collection | Retrieve and clean 10 years of daily price data using yfinance |
| 02 — Exploratory Analysis | Summary statistics, distributions, and trend visualizations |
| 03 — Risk Analysis | Volatility, drawdowns, Sharpe ratios, VaR, and correlation matrices |
| 04 — Time Series Modeling | Stationarity tests, ACF/PACF analysis, ARIMA/SARIMA forecasting |
| 05 — Machine Learning | Regression and classification models for return prediction |

## Key Findings

*To be updated after analysis is complete.*

## Author

**Jonny Nadeau**
[LinkedIn](https://www.linkedin.com/in/nadeaujonny/)

## License

This project is licensed under the [MIT License](LICENSE).
