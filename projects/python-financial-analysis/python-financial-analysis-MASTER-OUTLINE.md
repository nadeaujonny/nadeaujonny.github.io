# Master Outline & Study Guide
## Python Financial Analysis — Portfolio Performance & Risk (2015–2024)

> **Purpose of this document:** A complete, self-contained reference for studying this
> portfolio project. Use it to prepare for interviews — to explain what was built, how it
> works, why each decision was made, and to answer probing technical questions. When
> studying with Claude, this is the file Claude reads to teach and quiz you.
>
> **One sentence to anchor everything:** This project pulls 10 years of daily market data
> for six diversified assets via the yfinance API and runs it through a five-notebook
> Python pipeline — EDA → returns & risk → correlation & diversification → time-series
> decomposition → ARIMA forecasting — to evaluate portfolio performance, quantify risk,
> and demonstrate the value of diversification.
>
> **Important — read §13 before an interview.** The portfolio write-up (`index.md`)
> describes a few techniques (an ADF stationarity test, ARIMA confidence intervals,
> covariance-matrix diversification math, VaR, SARIMA, ML regression) that are **not in
> the committed notebooks**. This guide is written from what the *notebooks actually do*,
> and §13 lays out the gaps so nothing surprises you.

---

## Table of Contents

1. [The 30-Second Pitch](#1-the-30-second-pitch)
2. [Why This Project Exists (Context)](#2-why-this-project-exists-context)
3. [The Tech Stack](#3-the-tech-stack)
4. [The Dataset — 6 Assets via yfinance](#4-the-dataset--6-assets-via-yfinance)
5. [The 5-Notebook Pipeline (Architecture)](#5-the-5-notebook-pipeline-architecture)
6. [Notebook 1 — Data Acquisition & EDA](#6-notebook-1--data-acquisition--eda)
7. [Notebook 2 — Returns & Risk Analysis](#7-notebook-2--returns--risk-analysis)
8. [Notebook 3 — Correlation & Diversification](#8-notebook-3--correlation--diversification)
9. [Notebook 4 — Time Series Decomposition & Trends](#9-notebook-4--time-series-decomposition--trends)
10. [Notebook 5 — ARIMA Forecasting](#10-notebook-5--arima-forecasting)
11. [Key Results & Numbers](#11-key-results--numbers)
12. [Finance & Stats Concepts to Know Cold](#12-finance--stats-concepts-to-know-cold)
13. [Limitations & Honest Caveats (incl. write-up vs. notebooks)](#13-limitations--honest-caveats-incl-write-up-vs-notebooks)
14. [Design Decisions & Trade-offs (the "Why")](#14-design-decisions--trade-offs-the-why)
15. [Interview Q&A](#15-interview-qa)
16. [How to Walk Through This Project Live](#16-how-to-walk-through-this-project-live)
17. [Glossary](#17-glossary)

---

## 1. The 30-Second Pitch

This project is an **end-to-end Python financial analysis** of a six-asset diversified
portfolio over **10 years of daily data (2015–2024)**. It retrieves the data
programmatically via the **yfinance API**, then works through **five Jupyter notebooks**:
(1) data acquisition and exploratory analysis, (2) returns and risk metrics, (3)
correlation and diversification, (4) time-series decomposition and trends, and (5) an
**ARIMA forecasting baseline**.

The six assets span asset classes deliberately — a market benchmark (SPY), a growth stock
(AAPL), an energy-sector ETF (XLE), long-term bonds (TLT), gold (GLD), and international
equities (EFA) — so the analysis can study real cross-asset relationships. The pipeline
computes risk-adjusted performance (Sharpe ratio, maximum drawdown, annualized volatility),
maps correlations, demonstrates that a diversified allocation cuts volatility, decomposes
the S&P 500 into trend/seasonal/residual components, and fits an ARIMA model to forecast
SPY prices.

The headline findings: enormous performance dispersion (AAPL +936%, TLT −11% over the
decade), diversification meaningfully reduced volatility, equity assets are too correlated
to diversify each other, and **forecasting price levels is genuinely hard** — the ARIMA
baseline captured trend direction but missed regime shifts.

**One-line version:** "I built a five-notebook Python pipeline that pulls 10 years of
market data via an API and runs the full quant-analyst workflow — risk metrics,
correlation and diversification analysis, time-series decomposition, and ARIMA forecasting
— on a six-asset diversified portfolio."

---

## 2. Why This Project Exists (Context)

**The premise.** Investment decisions are too often driven by intuition — "stocks go up,
bonds are safe." This project's job is to replace intuition with **evidence**: take real
market data and quantify performance, risk, and the actual benefit of diversification.

**The simulated role.** The project plays a **data analyst supporting portfolio management
and investment decision-making** — turning raw price data into the risk and return
diagnostics a portfolio manager needs.

**Why these six assets.** They were chosen to be a *genuinely diversified* portfolio across
asset classes, so the analysis exercises real cross-asset behavior — equities vs. bonds vs.
gold vs. international — rather than six tech stocks that all move together. That choice is
what makes the correlation and diversification analysis (Notebook 3) meaningful.

**Why it's a strong portfolio project.** It demonstrates the full quantitative-analysis
loop on real financial data: **API data engineering** (programmatic retrieval, validation),
**risk analytics** (Sharpe, drawdown, volatility), **statistical analysis** (correlation,
time-series decomposition), and **predictive modeling** (ARIMA) — all in Python, all
reproducible. It's a finance-flavored data-science project that shows breadth across data
engineering, statistics, and modeling.

**The honest framing.** The project is deliberately structured as a *learning pipeline* —
five notebooks that build on each other, each ending in a completion summary. It's
exploratory and descriptive analysis, not a production trading system, and the forecasting
notebook is explicit about that ("Forecasting is HARD! Don't use for real trading!").

---

## 3. The Tech Stack

| Tool | Role |
|---|---|
| **Python 3.10+** | The language for the whole pipeline. |
| **Jupyter Notebook** | Five notebooks, one per analysis phase. |
| **yfinance** | The Yahoo Finance API wrapper — programmatic retrieval of 10 years of daily price data. |
| **pandas** | All data manipulation — `pct_change`, `cumprod`, `rolling`, `corr`, resampling. |
| **NumPy** | Numerical computing — the `√252` annualization, array math. |
| **matplotlib / seaborn** | Every chart — line charts, scatter plots, heatmaps, the decomposition panels. |
| **statsmodels** | Time-series tools — `seasonal_decompose` and the `ARIMA` model. |
| **scikit-learn** | Forecast evaluation metrics (`mean_absolute_error`, `mean_squared_error`). |
| **SciPy** | Listed as a dependency for scientific/statistical functions. |

**The mental model.** yfinance is the *data source*, pandas/NumPy are the *analysis
engine*, matplotlib/seaborn are the *presentation layer*, and statsmodels/scikit-learn are
the *modeling layer*. Everything runs on a laptop in seconds; no GPU, no cloud.

**One architectural fact to know.** The notebooks **hand off through CSV files**. Notebook
1 saves `cleaned_prices_2015_2024.csv`; Notebooks 2–5 load it (and Notebook 2 saves
`daily_returns` and `cumulative_returns` CSVs for Notebook 3). So the pipeline is a chain:
each notebook reads the previous notebook's saved output. *(The data files committed in
`data/processed/` carry an `.xls` extension but are actually plain CSVs — a minor
mislabeling.)*

---

## 4. The Dataset — 6 Assets via yfinance

**No static data file ships with the project** — all price data is **retrieved
programmatically via the yfinance API** (Yahoo Finance), for January 2015 through December
2024.

**The six assets — and *why* each one:**

| Ticker | Name | Asset class | Role in the portfolio |
|---|---|---|---|
| **SPY** | S&P 500 ETF | US large-cap stocks | The market **benchmark** |
| **AAPL** | Apple Inc. | Technology stock | A high-**growth** individual stock |
| **XLE** | Energy Select Sector ETF | Energy sector | **Cyclical** sector exposure |
| **TLT** | 20+ Year Treasury Bond ETF | Long-term bonds | The **safe-haven** asset |
| **GLD** | SPDR Gold Trust | Commodities / gold | An **inflation hedge** |
| **EFA** | MSCI EAFE ETF | International developed stocks | Geographic **diversification** |

**The data.** Daily price data, **`auto_adjust=True`** (so prices are adjusted for splits
and dividends — important for accurate return math). The analysis uses the **Close**
column. The result: **2,515 trading days per asset** — roughly 15,000 daily price points
across the six assets, with **zero missing values** (a 100%-complete dataset, validated in
Notebook 1).

**Why `auto_adjust=True` matters** (a likely interview question): adjusted close prices
back out the artificial price drops caused by stock splits and dividend payouts, so a
computed return reflects an investor's *actual* total return rather than a cosmetic price
change. Using unadjusted prices would understate returns for dividend-paying assets.

**The committed processed files** (`data/processed/`): `cleaned_prices_2015_2024`
(2,515 rows — the daily close prices), `daily_returns_2015_2024` (2,514 rows — one fewer,
because `pct_change` drops the first day), and `cumulative_returns_2015_2024` (2,514 rows —
the growth-of-$1 series).

---

## 5. The 5-Notebook Pipeline (Architecture)

```
  yfinance API  (Yahoo Finance — 6 tickers, 2015–2024 daily)
        │
        ▼
  NOTEBOOK 1 — Data Acquisition & EDA
  download (retry logic) · validate · price history chart · summary stats · correlation
        │  saves → cleaned_prices_2015_2024.csv
        ▼
  NOTEBOOK 2 — Returns & Risk Analysis
  daily & cumulative returns · volatility · Sharpe · max drawdown · risk-return scatter
        │  saves → daily_returns.csv, cumulative_returns.csv
        ▼
  NOTEBOOK 3 — Correlation & Diversification
  correlation matrix · rolling 252-day correlations · 100% SPY vs 60/30/10 portfolio
        │
        ▼
  NOTEBOOK 4 — Time Series Decomposition & Trends
  50/200-day moving averages · multiplicative seasonal decomposition
        │
        ▼
  NOTEBOOK 5 — ARIMA Forecasting
  80/20 chronological train/test split · ARIMA(1,1,1) · MAE / RMSE / MAPE
        │
        ▼
  12 saved chart PNGs in outputs/figures/
```

**The key architectural idea — sequential, file-chained notebooks.** Each notebook is one
analysis *phase*, and they pass data forward through saved CSV files: Notebook 1 produces
the clean prices, Notebook 2 produces the returns, and Notebooks 3–5 load whichever they
need. The chain means each notebook is independently runnable (given the upstream CSVs
exist) and the analysis builds in layers — raw data → returns → relationships → structure →
forecast.

**A style note.** The notebooks are **all code cells** (no markdown cells) — narration is
done through `print()` statements and section-header comments. Each notebook ends with a
printed "completion summary" listing what it did and what it found. It's a tutorial-style
structure: clear and linear.

---

## 6. Notebook 1 — Data Acquisition & EDA

**File:** `01_data_acquisition_eda.ipynb` · **Output:** `cleaned_prices_2015_2024.csv`,
2 charts

**Business question.** What are the fundamental characteristics of each asset's 10-year
price history, and what preliminary relationships exist between them?

**What the notebook actually does, step by step:**

1. **Download with retry logic.** `yf.download()` for the six tickers, 2015–2024,
   `auto_adjust=True`, wrapped in a **3-attempt retry loop** with a 2-second wait between
   tries — defensive coding against a flaky API.
2. **Extract Close prices and validate quality.** Pulls `data['Close']`, checks shape and
   date range, and runs a **missing-data check** — confirmed **zero missing values** across
   all 2,515 days × 6 assets.
3. **10-year price history chart** — all six assets' raw prices on one plot.
4. **Summary statistics** — `describe()`, plus three computed performance metrics:
   - **Total return** = `(last price / first price − 1) × 100`.
   - **Annualized return (CAGR)** = `(last/first)^(1/years) − 1` — the constant yearly
     growth rate that would produce the observed total return.
   - **Annualized volatility** = `daily_returns.std() × √252 × 100`.
5. **Correlation matrix + heatmap** — an initial `prices.corr()` heatmap, and it
   programmatically finds the highest and lowest correlations.
6. **Save** `cleaned_prices_2015_2024.csv` for the downstream notebooks.

**Key findings.**
- **Massive performance dispersion** — **AAPL +935.85%** total return over the decade,
  **SPY +240.81%**, and **TLT −11.29%** (long bonds *lost* money in a rising-rate decade).
- **100% data completeness** — zero missing values; the yfinance API delivered a clean,
  reliable dataset.
- **Highest volatility: XLE (29.81%)**; **lowest: GLD (14.12%)**.

**The teachable point.** This notebook's job is *foundation*: get the data, prove it's
clean, and establish the basic shape (who grew, who's volatile, who's correlated). A core
discipline shown here: **validate data quality before any downstream analysis** — a missing
value undetected at this stage would corrupt every return and risk calculation that
follows.

---

## 7. Notebook 2 — Returns & Risk Analysis

**File:** `02_returns_risk_analysis.ipynb` · **Output:** `daily_returns` + `cumulative_returns` CSVs, 3 charts

**Business question.** Which assets delivered the best *risk-adjusted* returns, and where
were the largest downside episodes?

**What the notebook does:**

1. **Daily returns** — `prices.pct_change().dropna()` — the day-over-day percentage change.
2. **Cumulative returns** — `(1 + daily_returns).cumprod()` — the "growth of $1": what one
   dollar invested in 2015 became.
3. **Annualized volatility** — `daily_returns.std() × √252`. *(The √252 converts a daily
   standard deviation to an annual one — 252 is the standard trading-days-per-year.)*
4. **Annualized return (CAGR)** and the **Sharpe ratio** — `(annual return − risk-free
   rate) / annualized volatility`, using a **2% risk-free rate**.
5. **Risk-return scatter plot** — each asset plotted as volatility (x) vs. return (y), with
   diagonal lines marking Sharpe-ratio levels; the upper-left quadrant is best.
6. **Maximum drawdown** — the worst peak-to-trough decline, computed by tracking the
   running maximum (`cummax`) of the cumulative-return path and measuring the largest drop
   below it.
7. **Save** the daily and cumulative returns CSVs.

**Key findings** (approximate annualized figures over 2015–2024, Sharpe at rf = 2%):

| Asset | ~Annual Return | ~Volatility | ~Sharpe | ~Max Drawdown |
|---|---|---|---|---|
| AAPL | 26% | 30% | 0.80 | −39% |
| SPY | 13% | 18% | 0.61 | −34% |
| GLD | 8% | 15% | 0.40 | −21% |
| EFA | 6% | 17% | 0.24 | −35% |
| XLE | 4% | 30% | 0.07 | −62% |
| TLT | −1% | 16% | −0.19 | −48% |

The headline reads: **AAPL** had the best return *and* the best Sharpe; **XLE** had AAPL-
level volatility but tiny return and a brutal **−62% drawdown** (worst risk-adjusted
performer); **TLT lost money** and still drew down ~48%; **GLD** had the smallest drawdown
(~21%) — the steadiest diversifier.

**The teachable point — risk has two faces.** Volatility and drawdown tell *different*
stories: TLT's volatility (~16%) looked moderate, but its drawdown (~48%) was severe.
Volatility measures day-to-day wobble; drawdown measures the worst sustained loss an
investor would actually have to *live through*. The lesson the notebook draws: evaluate
**Sharpe and drawdown together** — neither alone is enough.

---

## 8. Notebook 3 — Correlation & Diversification

**File:** `03_correlation_diversification.ipynb` · **Output:** 3 charts

**Business question.** How stable are cross-asset correlations over time, and how much risk
can diversification actually remove?

**What the notebook does:**

1. **Full-period correlation matrix** on daily returns + an enhanced heatmap; it
   programmatically identifies the strongest and weakest pairs.
2. **Rolling 252-day correlations** — for four key pairs (SPY-TLT, SPY-GLD, AAPL-SPY,
   XLE-TLT), a one-trading-year rolling window tracks how each relationship *shifts* across
   calm and crisis periods, with the COVID window shaded.
3. **The diversification benefit** — it builds two portfolios as weighted daily-return
   series and compares them: a **concentrated portfolio (100% SPY)** vs. a **diversified
   portfolio (60% SPY / 30% TLT / 10% GLD)**, computing each one's annualized return,
   volatility, Sharpe, and drawdown.

**Key findings.**
- **The strongest correlation is EFA–SPY at ≈ 0.855** — international and US large-cap
  equities move almost in lockstep. *(Note: the portfolio write-up's approximate table
  shows SPY-AAPL as the top pair at ~0.80; the notebook's actual computed output says
  EFA-SPY 0.855 is the strongest — cite the notebook's number.)*
- **Equity assets cluster** — SPY, AAPL, EFA, XLE all correlate moderately-to-strongly, so
  adding *another* equity barely diversifies anything.
- **TLT (bonds) is negatively correlated with stocks** (~−0.35 vs. SPY) — a genuine
  diversifier; **GLD (gold) is near-zero correlated** with both stocks and bonds — an
  independent return driver.
- **Diversification worked** — the 60/30/10 portfolio had **lower volatility** than 100%
  SPY (the notebook reports a volatility reduction of ~6.67 percentage points; the write-up
  frames the same result as roughly a 35% *relative* reduction). The diversified portfolio
  had a **better Sharpe ratio despite a lower raw return** — the project's clearest
  demonstration of diversification as a "free lunch."
- **Correlations are regime-dependent** — the rolling windows showed the SPY-TLT negative
  correlation weakening (even flipping positive) during the 2022 rate-hike period, and
  equity correlations spiking together during the March 2020 crash — diversification
  weakens exactly when you need it most.

**The teachable point.** This is the project's core finance lesson: **diversification means
combining assets with *low correlation*, not just holding *more* assets.** Six equity ETFs
that all correlate at 0.8 are not a diversified portfolio. And because correlations *move*,
diversification has to be monitored, not set once.

---

## 9. Notebook 4 — Time Series Decomposition & Trends

**File:** `04_time_series_trends.ipynb` · **Output:** 2 charts

**Business question.** What components drive SPY's price movement, and can trend,
seasonality, and noise be separated?

**What the notebook does:**

1. **Moving averages** — computes SPY's **50-day** and **200-day** moving averages and
   overlays them on the price. These are the classic technical-analysis regime indicators:
   when the 50-day crosses *above* the 200-day it's a "**golden cross**" (bullish); crossing
   *below* is a "**death cross**" (bearish).
2. **Seasonal decomposition** — `statsmodels`' `seasonal_decompose` with a
   **multiplicative model** and a **252-day period** (one trading year), splitting SPY into
   three components:
   - **Trend** — the long-run direction.
   - **Seasonal** — the repeating annual pattern.
   - **Residual** — what's left: random noise and shocks.

**Why a *multiplicative* model** (a likely interview question): financial prices grow
roughly *exponentially* (a percentage each year), so the components combine by
multiplication (trend × seasonal × residual), not addition. An additive model fits series
that grow by a fixed *amount* each period; a multiplicative model fits series that grow by
a fixed *rate* — which is how markets behave.

**Key findings.**
- **Trend dominates.** The notebook's own estimate: SPY's behavior is roughly **80% trend,
  15% seasonal, 5% random** — a persistent long-run uptrend (from ~$180 to ~$520+) broken
  by sharp structural breaks (the March 2020 COVID crash, the 2022 rate selloff).
- **Seasonality is weak** — calendar patterns contribute far less than trend; they're not a
  reliable forecasting signal for equities.
- **The residual concentrates the shocks** — crisis events show up as large residual
  spikes, which the trend view hides.
- **Moving-average crossovers** confirmed regime changes (multiple golden crosses, a brief
  COVID death cross) but **lag** actual reversals.

**The teachable point.** Decomposition is a *diagnostic* — it tells you the series is
trend-driven, which is useful context before forecasting. *(Note: the portfolio write-up
describes an Augmented Dickey-Fuller stationarity test in this notebook; the committed
`04_time_series_trends.ipynb` does **not** include one — see §13. The standard finance fact
to know anyway: raw **prices are non-stationary** but daily **returns are stationary**,
which is why return-based inputs are the right choice for modeling.)*

---

## 10. Notebook 5 — ARIMA Forecasting

**File:** `05_forecasting.ipynb` · **Output:** 2 charts

**Business question.** Can a classical ARIMA model produce useful out-of-sample SPY price
forecasts?

**What the notebook does:**

1. **Chronological 80/20 train/test split** — the first **2,012 days** (≈2015–2022) train
   the model; the last **503 days** (≈2022–2024) are the holdout test. **Chronological** is
   essential: you must never train on future data and test on the past — that's lookahead
   leakage. The split is visualized.
2. **Fit `ARIMA(1,1,1)`** on the training SPY price series. The `(p,d,q)` order means:
   **p=1** autoregressive term (today depends on yesterday), **d=1** differencing (difference
   the series once to make it stationary), **q=1** moving-average term (today depends on
   yesterday's forecast error).
3. **Forecast** the full ~503-day test horizon with `fitted_model.forecast()` and plot
   predictions vs. actuals.
4. **Evaluate** with three error metrics: **MAE** (mean absolute error — average dollar
   error), **RMSE** (root mean squared error — penalizes large errors more heavily), and
   **MAPE** (mean absolute percentage error).

**Key findings.**
- ARIMA(1,1,1) **captured the general upward trend direction** but **could not anticipate
  the magnitude or timing** of the 2023–2024 rally — the model struggled where it mattered.
- **RMSE exceeded MAE** — that gap means a few large errors (during volatile windows)
  drove a disproportionate share of total error.
- The honest conclusion, stated in the notebook itself: *"Stock prices are inherently
  difficult to forecast — past performance ≠ future results,"* and *"don't use for real
  trading."* ARIMA(1,1,1) is a **transparent baseline**, not a production model.

**The teachable point — and the maturity signal.** The most valuable thing in this notebook
is that it **doesn't oversell the model.** A naive project would report the error metric
and call the forecast a success. This one frames ARIMA as a *baseline benchmark* — the
simple, interpretable model that any fancier approach must beat — and is candid that
univariate linear models can't predict nonlinear market regime shifts. Being able to say
"my forecast was a deliberately simple baseline, and here's why it has limits" is stronger
than claiming a stock predictor that works.

---

## 11. Key Results & Numbers

Memorize the headline figures (these are from the notebooks' actual computed output).

| Metric | Value |
|---|---|
| Assets | 6 — SPY, AAPL, XLE, TLT, GLD, EFA |
| Period | Jan 2015 – Dec 2024 |
| Trading days | **2,515** per asset (~15,000 total observations) |
| Missing values | **0** (100% complete) |
| Best total return | **AAPL +935.85%** |
| Market (SPY) total return | **+240.81%** |
| Worst total return | **TLT −11.29%** (bonds lost money) |
| Highest volatility | **XLE — 29.81%** annualized |
| Lowest volatility | **GLD — 14.12%** annualized |
| Best Sharpe ratio | **AAPL** (~0.80, rf = 2%) |
| Worst max drawdown | **XLE ≈ −62%** |
| Strongest correlation | **EFA–SPY ≈ 0.855** |
| Best diversifier | **TLT** (negative correlation with equities); **GLD** (near-zero) |
| Diversification benefit | 60/30/10 SPY/TLT/GLD portfolio cut volatility (~6.7 pts absolute / ~35% relative) and improved Sharpe |
| Forecast model | **ARIMA(1,1,1)** — 80/20 split (2,012 train / 503 test days) |
| Charts produced | 12 PNGs in `outputs/figures/` |

**The five takeaways (the story the project tells):**

1. **Performance dispersion is enormous** — over the *same* decade, AAPL grew ~10× and TLT
   lost money. Asset class is destiny.
2. **Return and risk are linked** — the biggest growers (AAPL) carried the biggest interim
   risk; the steady assets (GLD) grew modestly.
3. **Path risk matters as much as endpoint return** — XLE and TLT had drawdowns
   (~62%, ~48%) that real investors would struggle to hold through.
4. **Diversification works — but only across *low-correlated* assets.** Mixing equities,
   bonds, and gold cut volatility; mixing equities with more equities would not.
5. **Forecasting price levels is hard** — the ARIMA baseline got direction but missed
   magnitude and timing.

---

## 12. Finance & Stats Concepts to Know Cold

A finance/data interview will probe the fundamentals behind the project.

**Daily return** — `(today's price / yesterday's price) − 1`; in pandas, `pct_change()`.

**Cumulative return** — the compounded growth of $1: `(1 + daily_returns).cumprod()`.

**Total return vs. annualized return (CAGR)** — total return is the whole-period change;
**CAGR** is the constant *yearly* rate that produces it: `(end/start)^(1/years) − 1`. CAGR
makes assets held for different periods comparable.

**Volatility** — the standard deviation of returns; the standard risk measure. **Annualized
volatility = daily std × √252** — the "√time" rule scales a daily figure to a yearly one
(252 = trading days per year).

**Sharpe ratio** — `(return − risk-free rate) / volatility` — *risk-adjusted* return, i.e.,
how much excess return you earn per unit of risk. Higher is better. This project uses a 2%
risk-free rate. A negative Sharpe (like TLT's) means the asset underperformed cash.

**Maximum drawdown** — the largest peak-to-trough percentage decline over the period;
measures the worst loss an investor would have lived through. Computed by comparing the
cumulative-return path to its running maximum (`cummax`).

**Correlation** — how two assets move together, from −1 (perfect opposite) to +1 (perfect
together); 0 = independent. The basis of diversification.

**Diversification** — combining **low-correlated** assets so the portfolio's volatility is
*less than* the weighted average of its parts. Called a "free lunch" because it cuts risk
without proportionally cutting return.

**Risk-free rate** — the return on a "riskless" asset (a Treasury bill); the baseline the
Sharpe ratio measures excess return *above*.

**Stationarity** — a series whose statistical properties (mean, variance) don't change over
time. **Prices are non-stationary** (they trend); **returns are stationary**. Stationarity
is a prerequisite for ARIMA — handled by the differencing step.

**Time-series decomposition** — splitting a series into **trend** (long-run direction),
**seasonal** (repeating cycle), and **residual** (noise). **Multiplicative** model for
exponentially-growing series (markets); **additive** for linearly-growing ones.

**Moving average** — the rolling mean over a window (50-day, 200-day); a smoothed trend
line. The **golden cross** (50 crosses above 200) and **death cross** (below) are regime
signals.

**ARIMA(p,d,q)** — AutoRegressive Integrated Moving Average — a classic univariate
forecasting model. **p** = autoregressive lags, **d** = differencing order (to reach
stationarity), **q** = moving-average lags. This project uses ARIMA(1,1,1).

**Train/test split (chronological)** — for time series, the test set must be the *latest*
data and the train set the *earliest* — never random — to avoid training on the future.

**MAE / RMSE / MAPE** — forecast error metrics. MAE = average absolute error; RMSE =
root-mean-squared error (penalizes large misses more); MAPE = average absolute *percentage*
error. RMSE > MAE signals a few big errors.

---

## 13. Limitations & Honest Caveats (incl. write-up vs. notebooks)

Volunteer these — and especially know the first one, because it's about your own materials.

**13.1 — The portfolio write-up describes more than the committed notebooks contain.**
This is the most important caveat for an interview. The project's `index.md` page and
`README.md` are polished and, in several places, describe a *more sophisticated* version of
the analysis than the five notebooks actually implement. Specifically:

- **ADF stationarity test** — `index.md` (Analysis 4) shows `adfuller()` code and an "ADF
  Statistic < −20, p-value < 0.001" result. **Notebook 4 does not import or run `adfuller`**
  — it has moving averages and `seasonal_decompose` only.
- **ARIMA confidence intervals** — `index.md` (Analysis 5) shows `get_forecast()` /
  `conf_int()` and says "confidence intervals were included." **Notebook 5 uses plain
  `.forecast()`** and computes/plots **no confidence intervals**.
- **Covariance-matrix diversification math** — `index.md` (Analysis 3) shows
  `w.T @ cov @ w` portfolio-variance code. **Notebook 3 builds the weighted-return series
  directly** and never uses a covariance matrix.
- **Value at Risk (VaR)** — listed in `index.md`'s "Skills" and the README's features.
  **No VaR calculation appears in any notebook.**
- **SARIMA and machine-learning regression** — the README mentions "ARIMA/SARIMA" and a
  "Machine Learning" notebook with "regression and classification." **Notebook 5 fits only
  ARIMA(1,1,1)** — no SARIMA, no ML model.

**How to handle this in an interview:** describe what the notebooks *actually do* — they're
solid and real. If asked about VaR, SARIMA, ADF, or confidence intervals, be honest: "the
write-up frames those as part of the analysis, but in the committed notebooks I implemented
[the actual thing]; those are natural extensions I'd add next." Never claim a technique the
notebooks don't contain. (The cleanest fix, if you want the materials to align, is to
actually add those pieces to the notebooks — but as it stands, *cite the notebooks*.)

**13.2 — Other genuine limitations:**
- **Backward-looking, single 10-year window.** All conclusions describe 2015–2024 — a
  decade of mostly-rising stocks and (until 2022) low rates. A strong Sharpe here doesn't
  predict the next decade.
- **It's descriptive, not a strategy.** The project analyzes performance and risk; it
  doesn't build or backtest a trading strategy, and the diversified 60/30/10 weights are
  illustrative, not optimized (no efficient-frontier / mean-variance optimization).
- **ARIMA is a weak forecaster for prices** — by the project's own admission. A univariate
  linear model can't capture market regime shifts.
- **Survivorship and asset-selection bias** — AAPL was chosen *knowing* it was a huge
  winner; picking a single growth stock in hindsight isn't a neutral test.
- **The notebooks have no markdown cells** — narration is via `print()` statements. They
  read more like scripts than documented analysis notebooks.
- **The processed data files are mislabeled `.xls`** but are actually CSVs.

---

## 14. Design Decisions & Trade-offs (the "Why")

Interviewers reward "why" answers. The deliberate choices and their rationale:

**Why retrieve data via an API instead of a static CSV?**
Reproducibility and freshness — anyone can re-run the pipeline and get current data, and
there's no large data file to commit. The trade-off is a dependency on the API being up,
which is why Notebook 1 wraps the download in retry logic.

**Why `auto_adjust=True`?**
So prices are adjusted for splits and dividends. Returns computed from *unadjusted* prices
would show a fake drop on every dividend date and split — adjusted prices give the
investor's true total return.

**Why six assets across asset classes, not six stocks?**
The whole point is to study cross-asset relationships and diversification. Six tech stocks
would all correlate near 1.0 and there'd be nothing to learn about diversification — the
deliberate spread (equity, bond, gold, international) is what makes Notebook 3 meaningful.

**Why annualize with √252?**
252 is the standard number of US trading days per year. Volatility scales with the square
root of time, so a daily standard deviation becomes annual by multiplying by √252 — this
puts every asset on a comparable yearly scale.

**Why compute both Sharpe *and* drawdown?**
They measure different risks. Sharpe rewards smooth return-per-unit-of-wobble; drawdown
measures the worst sustained loss. TLT proved why you need both — moderate volatility but a
severe drawdown.

**Why a chronological train/test split for the ARIMA model?**
Time-series forecasting must respect time. A random split would let the model train on
2024 data and "predict" 2018 — lookahead leakage that makes the forecast look far better
than it is. The chronological 80/20 split simulates genuine real-world forecasting.

**Why ARIMA(1,1,1) specifically?**
It's the simplest non-trivial ARIMA — one AR term, one differencing, one MA term. The point
wasn't to find the best forecaster; it was to establish a **transparent, interpretable
baseline** that any more complex model should be benchmarked against.

**Why a five-notebook pipeline instead of one big notebook?**
Each notebook is one phase with a clear input and output, chained through saved CSVs. It
keeps each stage focused, independently runnable, and easy to follow — the analysis builds
in layers.

---

## 15. Interview Q&A

Practice these out loud. Answers are written the way you'd actually speak.

**Q1. Give me the overview of this project.**
"It's an end-to-end Python financial analysis of a six-asset diversified portfolio over ten
years of daily data, 2015 to 2024. I pull the data via the yfinance API, then work through
five notebooks: data acquisition and EDA, returns and risk metrics, correlation and
diversification, time-series decomposition, and an ARIMA forecasting baseline. The assets
span asset classes on purpose — S&P 500, Apple, energy, long bonds, gold, international —
so I can study real cross-asset behavior. The big themes are quantifying risk-adjusted
return and showing what diversification actually buys you."

**Q2. How did you get the data, and how did you make sure it was clean?**
"Programmatically, through the yfinance API — no static file. I wrapped the download in a
three-attempt retry loop in case the API hiccuped. I used auto_adjust so prices account for
splits and dividends. Then before any analysis I ran a data-quality check — the dataset was
100% complete, zero missing values across 2,515 trading days for all six assets. Validating
completeness first matters, because a missing value undetected there corrupts every return
and risk number downstream."

**Q3. What's the Sharpe ratio and why does it matter?**
"It's risk-adjusted return — excess return over the risk-free rate, divided by volatility.
It answers 'how much return am I getting per unit of risk I'm taking?' I used a 2%
risk-free rate. It matters because raw return is misleading — XLE and AAPL both had about
30% volatility, but AAPL turned that risk into roughly a 0.80 Sharpe while XLE was near
zero. Same risk, completely different reward. TLT actually had a negative Sharpe — it
underperformed cash."

**Q4. What's the difference between volatility and maximum drawdown?**
"Volatility is the standard deviation of returns — day-to-day wobble. Maximum drawdown is
the worst peak-to-trough decline — the deepest sustained loss an investor would actually
have to sit through. They can disagree: TLT had only moderate volatility, around 16%, but a
roughly 48% drawdown. Volatility says 'bumpy,' drawdown says 'how bad does it get and stay.'
You need both — I'd never screen a portfolio on volatility alone."

**Q5. How did you demonstrate the value of diversification?**
"In notebook three I compared two portfolios as weighted return series — a concentrated one,
100% SPY, and a diversified one, 60% SPY, 30% TLT, 10% gold. The diversified portfolio had
clearly lower volatility — and a better Sharpe ratio even though its raw return was lower.
That's the 'free lunch' of diversification: combining low-correlated assets reduces risk
more than it reduces return. The key is *low-correlated* — bonds and gold, because they
don't move with stocks."

**Q6. Why doesn't holding more stocks diversify a portfolio?**
"Because equities share the same underlying risk factors. In my data, SPY, Apple,
international stocks, and energy all correlated moderately to strongly — the strongest pair,
EFA and SPY, was about 0.855. When assets correlate near one, they fall together, so adding
another one barely reduces risk. Real diversification needs assets that move differently —
that's why I added bonds and gold, not a seventh stock."

**Q7. You found correlations change over time — why does that matter?**
"I computed rolling 252-day correlations, and the relationships weren't stable. The
stock-bond correlation, normally negative, weakened and even turned positive during the
2022 rate-hike period — so the bond hedge wasn't working when stocks fell. And in the March
2020 crash, equity correlations spiked together. The lesson: diversification tends to break
down exactly during a crisis, when you need it most. So correlation has to be monitored as
a live risk metric, not assumed."

**Q8. Walk me through the time-series decomposition.**
"I decomposed SPY with a multiplicative seasonal model and a 252-day period, splitting it
into trend, seasonal, and residual components. Multiplicative because markets grow roughly
exponentially — by a percentage, not a fixed dollar amount — so the components multiply.
The takeaway was that SPY is overwhelmingly trend-driven, roughly 80% trend, with weak
seasonality and the residual concentrating the crisis shocks. That told me a forecasting
model should focus on trend, and that seasonality isn't a reliable equity signal."

**Q9. Explain your ARIMA forecasting setup.**
"I forecasted SPY prices with ARIMA(1,1,1) — one autoregressive term, one differencing
step, one moving-average term. I used a chronological 80/20 train/test split — about 2,000
days to train, 500 to test — chronological so the model never trains on the future. Then I
evaluated with MAE, RMSE, and MAPE. The honest result: the model captured the general
upward direction but missed the magnitude and timing of the 2023–24 rally. RMSE exceeded
MAE, meaning a few big errors during volatile periods dominated. I treated ARIMA as a
transparent baseline, not a real predictor."

**Q10. Why is forecasting stock prices so hard, and is your model useful?**
"Stock prices are close to a random walk with nonlinear regime shifts, and a univariate
linear model like ARIMA can't anticipate a regime change — a rate shock, a crisis. So no, I
wouldn't trade on it, and the notebook says so explicitly. But it's still useful as a
baseline: it's simple and interpretable, and any more sophisticated model — multivariate,
regime-switching, machine learning — should have to beat this benchmark to justify its
complexity. Knowing the limits of your model is part of the analysis."

**Q11. Why a chronological split instead of a random train/test split?**
"Because it's time-series data. A random split would let the model see 2024 data during
training and then 'predict' 2018 — that's lookahead leakage, and it makes the forecast look
artificially good. A chronological split — earliest data to train, latest to test —
simulates the real situation: you only ever have the past to predict the future."

**Q12. What would you do to improve this project?**
"A few things. I'd make the materials fully consistent — the write-up mentions a
stationarity test, ARIMA confidence intervals, and VaR that I'd actually implement in the
notebooks. I'd add proper mean-variance portfolio optimization to find efficient weights
rather than using illustrative 60/30/10. I'd benchmark ARIMA against richer models. And I'd
add walk-forward validation — retraining on a rolling window — since a single static split
doesn't reflect how forecasting works in practice."

**Q13. What's the single most important finding?**
"That diversification across low-correlated asset classes genuinely reduces risk — my
60/30/10 portfolio cut volatility meaningfully and improved the Sharpe ratio versus
all-stocks — but that it's conditional: correlations rise in a crisis, so the benefit
shrinks exactly when it's most needed. The practical conclusion is that diversification
works, but it has to be monitored, not assumed."

---

## 16. How to Walk Through This Project Live

If asked to screen-share the notebooks, use this order:

1. **State the structure first** — "it's a five-notebook pipeline, each phase chained
   through saved CSVs: data → returns → correlation → decomposition → forecast."
2. **Notebook 1** — show the **yfinance download with retry logic** and the data-quality
   check (zero missing values). Make the point: validate before you analyze.
3. **Notebook 2** — walk the risk metrics. Explain Sharpe and the volatility-vs-drawdown
   distinction with the TLT example (moderate volatility, severe drawdown).
4. **Notebook 3 — spend the most time here.** It's the strongest part. Show the correlation
   heatmap, the rolling correlations (equity clustering, the regime-dependent stock-bond
   relationship), and the 100%-SPY-vs-60/30/10 diversification comparison.
5. **Notebook 4** — the decomposition; explain why *multiplicative* (exponential growth)
   and that SPY is trend-dominated.
6. **Notebook 5** — the ARIMA baseline. **Lead with the honesty**: chronological split, a
   deliberately simple baseline, captured direction but not regime shifts.
7. **Close on the diversification finding** — it's the most defensible, business-relevant
   conclusion. End on the insight, not the code.

**Pacing tip:** spend the most time on Notebooks 2 and 3 — risk metrics and diversification
are the substantive finance content and the most defensible findings. Treat Notebook 5 as a
*baseline* and be candid about its limits — that candor reads as maturity. And if the
interviewer has read the portfolio page, be ready for §13: describe what the notebooks
actually contain.

---

## 17. Glossary

- **yfinance** — an open-source Python library that pulls market data from Yahoo Finance;
  the project's data source.
- **OHLCV** — Open, High, Low, Close, Volume — the standard daily price fields; this
  project uses **Close**.
- **`auto_adjust`** — a yfinance option that adjusts prices for stock splits and dividends.
- **Ticker** — a market symbol for an asset (SPY, AAPL, etc.).
- **ETF** — Exchange-Traded Fund — a basket of securities that trades like a stock (SPY,
  XLE, TLT, GLD, EFA are ETFs).
- **Daily return** — the day-over-day percentage price change; pandas `pct_change()`.
- **Cumulative return** — the compounded growth of an initial $1; `(1+r).cumprod()`.
- **Total return** — the whole-period percentage change, start to end.
- **CAGR (annualized return)** — Compound Annual Growth Rate; the constant yearly rate that
  yields the observed total return.
- **Volatility** — standard deviation of returns; the standard risk measure.
- **Annualization (√252)** — scaling a daily statistic to a yearly one using 252 trading
  days and the square-root-of-time rule.
- **Sharpe ratio** — risk-adjusted return: `(return − risk-free rate) / volatility`.
- **Risk-free rate** — the return on a "riskless" asset (a T-bill); this project uses 2%.
- **Maximum drawdown** — the worst peak-to-trough percentage decline over a period.
- **Running maximum (`cummax`)** — the highest value seen so far; used to compute drawdown.
- **Correlation** — how two assets co-move, from −1 to +1.
- **Diversification** — combining low-correlated assets to lower portfolio risk; a "free
  lunch."
- **Rolling correlation** — correlation computed over a moving window (here, 252 days) to
  track how a relationship changes over time.
- **Regime** — a distinct market environment (bull, bear, crisis); relationships differ by
  regime.
- **Stationarity** — a series whose statistical properties are constant over time; returns
  are stationary, prices are not.
- **Time-series decomposition** — splitting a series into trend, seasonal, and residual
  components.
- **Multiplicative vs. additive model** — multiplicative for exponentially-growing series
  (markets); additive for linearly-growing ones.
- **Moving average (50-day / 200-day)** — a rolling-mean trend line.
- **Golden cross / death cross** — the 50-day MA crossing above / below the 200-day MA — a
  bullish / bearish regime signal.
- **ARIMA(p,d,q)** — AutoRegressive Integrated Moving Average; a classic univariate
  forecasting model. p = AR lags, d = differencing, q = MA lags.
- **Differencing** — subtracting consecutive values to make a series stationary (the "I" in
  ARIMA).
- **Train/test split (chronological)** — for time series, training on the earliest data and
  testing on the latest, never random.
- **MAE / RMSE / MAPE** — forecast error metrics: mean absolute error, root-mean-squared
  error, mean absolute percentage error.
- **ADF (Augmented Dickey-Fuller) test** — a statistical test for stationarity. *(Described
  in the project write-up; not implemented in the committed notebooks — see §13.)*
- **VaR (Value at Risk)** — an estimate of the worst expected loss at a given confidence
  level. *(Listed as a project skill; not implemented in the committed notebooks — see §13.)*

---

*This study guide documents the project as built. The authoritative references are the five
notebooks in `notebooks/` (the actual code), the processed CSVs in `data/processed/`, and
the portfolio page `index.md`. Where the portfolio page describes techniques not present in
the committed notebooks, §13 documents the gap. When this guide and the notebooks disagree,
the notebooks win.*