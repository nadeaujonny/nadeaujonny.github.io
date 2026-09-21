---
layout: default
title: Bot Bought – Automated Paper-Trading System (Python, SQL, FinBERT)
description: "A statistics-first experiment testing whether a dip-buying rule can beat the S&P 500, using a Monte Carlo null baseline, Sharpe-ratio benchmarking, an A/B test of a news-sentiment filter, and a power analysis. Paper trading only."
stack:
  - Python
  - pandas
  - SQL (SQLite)
  - FinBERT
  - Alpaca API
  - yfinance
  - FRED
  - Ubuntu Server
  - systemd
  - Git
  - Claude Code
pipeline:
  - label: "Data fetch"
    detail: "Pulls daily bars for 16 stocks + SPY benchmark"
  - label: "Signal"
    detail: "Flags a dip: drop ≥ 1.5× the stock's 20-day ATR AND below its 20-day moving average; skips stocks within 3 days of earnings"
  - label: "Sentiment"
    detail: "FinBERT scores recent headlines; negative-news dips are vetoed (shadow mode: scored and logged, not enforced)"
  - label: "Risk"
    detail: "$500 fixed position, max 6 open positions, $400 max daily loss, kill switch, cash only"
  - label: "Execute"
    detail: "Paper orders via Alpaca; exits at +6% target, −6% stop, or 10 trading days"
  - label: "Log"
    detail: "Every signal, gate decision, veto (with the headlines behind it), order, fill, and reconciliation stored in SQLite"
  - label: "Report"
    detail: "Nightly text digest, weekly review package, automated backups"
---

<a href="/projects/" class="back-to-projects btn" aria-label="Back to projects page">&larr; Back to Projects</a>

<h1>Bot Bought – Automated Paper-Trading System (Python, SQL, FinBERT)</h1>

<blockquote>
  <p>An automated, rules-based stock trading system I designed and deployed on a self-administered Linux server – paper trading only – built as a statistics-first experiment: every decision logged to SQL, every strategy claim tested against a null baseline and a buy-and-hold benchmark before being believed.</p>
</blockquote>

<div>
{% include tech-badges.html %}
{% include project-callout.html text="Paper trading only ($10,000 simulated Alpaca account; no real money)." %}
</div>


<details open>
  <summary><strong>The Question</strong></summary>

  <div>

  <h3>Can a simple dip-buying rule beat the market – and how would I know?</h3>
  <p>Rather than hunting for a profitable backtest, I used this project to practice rigorous analysis. Every strategy claim had to survive four tests before being believed:</p>
  <ul>
    <li><strong>Monte Carlo null baseline:</strong> is the result distinguishable from random entry timing?</li>
    <li><strong>Risk-adjusted benchmark:</strong> how does it compare to SPY buy-and-hold on Sharpe ratio?</li>
    <li><strong>A/B test:</strong> does a news-sentiment filter improve results?</li>
    <li><strong>Power analysis:</strong> how much data would a real verdict need?</li>
  </ul>

  <h3>The Answer</h3>
  <p><strong>The strategy does not beat SPY, and the sentiment filter hurt returns.</strong> That negative result is the point of the project: I let the data say no.</p>

  </div>
</details>
<details>
  <summary><strong>System Diagram</strong></summary>

  <div>

  <p>One engine, config-driven. Runs daily at 3:45 pm ET on weekdays on a headless Ubuntu server, scheduled with systemd timers.</p>

  {% include pipeline-diagram.html caption="Review loop: a weekly human-in-the-loop review, where analysis proposes changes, I approve/reject, and approved changes must prove themselves on a separate paper account before promotion. Autonomous self-modification was deliberately rejected (it overfits to noise)." %}

  </div>
</details>
<details>
  <summary><strong>Strategy Design &amp; Key Decisions</strong></summary>

  <div>

  <h3>Trading Rules</h3>
  <ul>
    <li><strong>Entry:</strong> drop ≥ 1.5× the stock's 20-day ATR (volatility-normalized) AND below its 20-day moving average; skips stocks within 3 days of earnings</li>
    <li><strong>Sentiment filter:</strong> FinBERT scores recent headlines; negative-news dips are vetoed. Currently in "shadow mode": scored and logged, not enforced (see Results for why)</li>
    <li><strong>Risk guardrails:</strong> hard checks before any order: $500 fixed position, max 6 open positions, $400 max daily loss, kill switch, cash only. No automated process can change these.</li>
    <li><strong>Exits:</strong> +6% target, −6% stop, or 10 trading days</li>
  </ul>

  <h3>Design Choices</h3>
  <ul>
    <li><strong>ATR-normalized entry instead of a flat % drop:</strong> "a 3% drop in KO is an event; in TSLA it's Tuesday"</li>
    <li><strong>Avoided RSI&lt;30 on purpose:</strong> the most-taught retail signal is the most crowded</li>
    <li><strong>Watchlist chosen for sector spread</strong> (max 3/sector), varied volatility, and varied news coverage, so the sentiment filter could be tested where news is thick vs. thin</li>
    <li><strong>$10k paper balance</strong> (not the $100k default) so results transfer to realistic account sizes</li>
  </ul>

  <h3>Project Facts</h3>
  <table>
    <tbody>
      <tr><th scope="row">My role</th><td>Designed and directed, built with Claude Code. Sole owner: designed the strategy, set constraints, directed the build, and verified every result.</td></tr>
      <tr><th scope="row">Timeline</th><td>Started Aug 11, 2026; live paper trading since mid-Aug 2026; ongoing</td></tr>
      <tr><th scope="row">Status</th><td>Build complete (one optional test step left); in live forward-testing / review phase</td></tr>
      <tr><th scope="row">Budget</th><td>$0 – free data, free APIs, open-source model, reused hardware</td></tr>
      <tr><th scope="row">Money at risk</th><td>None – Alpaca paper account ($10,000 simulated)</td></tr>
      <tr><th scope="row">Scale</th><td>~13,000 lines of Python source, 1,504 automated tests, 99% line coverage on the risk module</td></tr>
      <tr><th scope="row">Backtest</th><td>10.6 years (2016–2026), 16 tickers, 45,000+ daily bars, 487 simulated round-trip trades</td></tr>
    </tbody>
  </table>

  <h3>Tech Stack</h3>
  <ul>
    <li><strong>Languages/data:</strong> Python (pandas), SQL (SQLite – trade log, schema migrations, append-only audit tables)</li>
    <li><strong>Data sources:</strong> Alpaca API (prices, news, order execution), yfinance (historical bars), FRED (macro)</li>
    <li><strong>ML/NLP:</strong> FinBERT (HuggingFace transformers) – financial-news sentiment scoring, run locally on CPU</li>
    <li><strong>Infrastructure:</strong> Ubuntu Server (headless), systemd timers for scheduling, SSH, Git/GitHub, nightly automated backups</li>
    <li><strong>Testing:</strong> pytest-style unit tests, mutation testing (deliberately breaking code to confirm tests catch it)</li>
    <li><strong>AI tooling:</strong> Claude Code (implementation), Claude (planning, review, analysis)</li>
  </ul>

  </div>
</details>
<details>
  <summary><strong>Results</strong></summary>

  <div>

  <p>All results below are from the backtest (2016–2026, live parameters, nothing tuned). They are not live trading results.</p>

  <h3>Backtest vs. SPY Buy-and-Hold</h3>
  <table class="results-table">
    <thead>
      <tr><th scope="col">Metric</th><th scope="col">Strategy</th><th scope="col">SPY buy-and-hold</th></tr>
    </thead>
    <tbody>
      <tr><td>Total return</td><td>+21.4%</td><td>+305.8%</td></tr>
      <tr><td>Sharpe ratio</td><td>0.644 (best parameter cell)</td><td>0.839</td></tr>
      <tr><td>Round-trip trades</td><td>487</td><td>–</td></tr>
    </tbody>
  </table>
  <p>The raw return comparison is unfair (the strategy averaged only 7.2% of capital deployed), so I used <strong>Sharpe ratio</strong> for the fair comparison. Buy-and-hold still wins on a risk-adjusted basis.</p>

  <h3>Null Baseline (Monte Carlo Permutation Test)</h3>
  <table class="results-table">
    <thead>
      <tr><th scope="col">Measure</th><th scope="col">Value</th></tr>
    </thead>
    <tbody>
      <tr><td>Test design</td><td>100 seeds × 2 generators × 2 fill-cost models</td></tr>
      <tr><td>Real strategy's percentile among random entry schedules</td><td>94th–97th</td></tr>
      <tr><td>Pre-registered threshold for a 9-cell parameter grid (family-wise correction)</td><td>99.43rd</td></tr>
      <tr><td>How often a cell hits the 97th percentile by chance</td><td>24% of the time</td></tr>
      <tr><td>Verdict</td><td>NOT statistically distinguishable from chance</td></tr>
    </tbody>
  </table>
  <p><strong>Sharper finding:</strong> when dates were kept but tickers shuffled, the edge nearly vanished. Timing carries what edge exists; stock selection doesn't.</p>

  <h3>Sentiment Filter A/B Test (2020–2026)</h3>
  <table class="results-table">
    <thead>
      <tr><th scope="col">Metric</th><th scope="col">Filter ON</th><th scope="col">Filter OFF</th></tr>
    </thead>
    <tbody>
      <tr><td>EV per trade</td><td>+$2.42</td><td>+$3.68</td></tr>
      <tr><td>Sharpe ratio</td><td>0.313</td><td>0.497</td></tr>
      <tr><td>Total, ON vs. OFF</td><td colspan="2">−$545</td></tr>
      <tr><td>By year</td><td colspan="2">ON worse in every year except 2023</td></tr>
    </tbody>
  </table>

  <table class="results-table">
    <thead>
      <tr><th scope="col">Trades</th><th scope="col">Win rate</th></tr>
    </thead>
    <tbody>
      <tr><td>Blocked by the filter</td><td>58.5%</td></tr>
      <tr><td>Kept by the filter</td><td>55.9%</td></tr>
    </tbody>
  </table>
  <ul>
    <li><strong>Mechanism:</strong> a dip big enough to trigger usually HAS negative news – that's what moved the price – so a negative-news filter removes the best rebounds.</li>
    <li><strong>Checked whether this was just COVID:</strong> it wasn't. Blocked trades spread across every year.</li>
    <li><strong>The filter is structurally a mega-cap filter:</strong> low-coverage stocks (KO, CAT) often have no news to read.</li>
  </ul>

  <h3>Market-Regime Analysis</h3>
  <table class="results-table">
    <thead>
      <tr><th scope="col">Measure</th><th scope="col">Value</th></tr>
    </thead>
    <tbody>
      <tr><td>Share of trading days carrying 32% of all signals</td><td>6.8%</td></tr>
      <tr><td>Signals on those days where the 6-position cap binds</td><td>64%</td></tr>
    </tbody>
  </table>
  <p>Signals cluster in market-wide shocks (Brexit, Feb 2018, COVID, April 2025 tariffs).</p>

  </div>
</details>
<details>
  <summary><strong>What I Learned</strong></summary>

  <div>

  <h3>Exits: Retracting My Own Recommendation</h3>
  <p>56% of trades exit on the 10-day time limit. That initially looked like "wasted" trades, but timeouts were the LARGEST profit contributor:</p>
  <table class="results-table">
    <thead>
      <tr><th scope="col">Exit type</th><th scope="col">Profit contribution</th></tr>
    </thead>
    <tbody>
      <tr><td>10-day time limit</td><td>+$1,311</td></tr>
      <tr><td>Target / stop</td><td>+$795</td></tr>
    </tbody>
  </table>
  <p>I retracted my own earlier recommendation to tighten exits. A 5-day max hold was clearly worse; 10 vs. 20 days was a plateau.</p>

  <h3>Win Rate vs. EV</h3>
  <p>The strategy with the best win rate (58.3%) earned less per trade than one winning 54.4%. Ranking by win rate inverted the right answer, so I chose EV per trade and Sharpe ratio as the metrics that matter.</p>

  <h3>Timing vs. Selection</h3>
  <p>Shuffling tickers while keeping dates nearly erased the edge: what edge exists comes from <em>when</em> the strategy buys, not <em>which</em> stock it picks.</p>

  <h3>Data Quality Catches</h3>
  <ul>
    <li>Caught a stock-split bug producing false signals at 20–30× ATR; fixed via split-adjusted data</li>
    <li>Caught the backtester computing ATR differently from the live bot (87 of 136 rows disagreed) and made them identical</li>
    <li>Found the vendor revised "final" volume data after the fact; narrowed a validation rule that had been over-trusted and pre-registered a test of when bars become final</li>
    <li>Found a verification script reporting 163 "blocking" disagreements, 158 of which were a stale data snapshot</li>
  </ul>

  <h3>Engineering Rigor</h3>
  <ul>
    <li><strong>Pre-registration:</strong> predictions and decision thresholds written down before running tests, to avoid fitting a story after the fact</li>
    <li><strong>Verify the verifier:</strong> planted known defects in comparison tools to confirm they detect them before trusting a "0 differences" result</li>
    <li><strong>Mutation testing</strong> on the money path (order submission/recovery)</li>
    <li><strong>Append-only audit trail:</strong> trade log and decision register can't be edited, only annotated</li>
  </ul>

  </div>
</details>
<details>
  <summary><strong>Limitations &amp; Honest Caveats</strong></summary>

  <div>

  <ul>
    <li><strong>Paper trading only.</strong> No real money is at risk, and no real profits or losses exist.</li>
    <li><strong>Backtest results, not live results.</strong> The live forward record is small (1 trade open, 0 closed as of 9/17/26). The backtest numbers above are the substantive results; there is no live performance data yet.</li>
    <li><strong>No out-of-sample split, by reasoned choice.</strong> 2020 held most stress events, so any chronological holdout would be either crisis-free or crisis-only – a holdout that can't fail returns "validated," which is worse than none. I used the null baseline instead.</li>
    <li><strong>The sentiment filter can't be tested evenly.</strong> Low-coverage stocks (KO, CAT) often have no news to read, so the filter is structurally a mega-cap filter.</li>
  </ul>

  <h3>Power Analysis: How Much Data a Verdict Needs</h3>
  <table class="results-table">
    <thead>
      <tr><th scope="col">Measure</th><th scope="col">Value</th></tr>
    </thead>
    <tbody>
      <tr><td>Per-trade standard deviation</td><td>$29.16</td></tr>
      <tr><td>Confidence interval at the v1 target of 30 trades</td><td>±$10.44/trade</td></tr>
      <tr><td>Backtest edge to detect</td><td>+$4.33/trade</td></tr>
      <tr><td>Trades needed to detect it</td><td>~175 (~3.8 years at the measured rate)</td></tr>
    </tbody>
  </table>
  <p>So the review process was designed NOT to wait on a verdict that 30 trades can't deliver.</p>

  </div>
</details>
<details>
  <summary><strong>Current Status &amp; What's Next</strong></summary>

  <div>

  <p><em>As of 2026-09-17.</em></p>
  <ul>
    <li>Live paper trading since mid-Aug 2026; 31 daily runs, 476 signals evaluated</li>
    <li>First strategy-chosen trade: BAC, Sep 16, 2026 (1.60× ATR dip, sentiment scored neutral → passed)</li>
    <li>First sentiment filter decision logged the same day</li>
    <li><strong>v1 goal:</strong> 30+ closed trades, projected ~April 2027 at the measured signal rate</li>
    <li><strong>Next milestone:</strong> final v1 report comparing live results to SPY (report script already built, waits on data)</li>
  </ul>
  <p>Source code is currently private.</p>

  </div>
</details>
