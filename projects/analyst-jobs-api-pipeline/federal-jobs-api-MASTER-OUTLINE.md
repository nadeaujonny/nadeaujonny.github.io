# Master Outline & Study Guide
## Federal Job Market Analytics Pipeline (Python, SQLite, Streamlit)

> **Purpose of this document:** A complete, self-contained reference for studying this
> portfolio project. Use it to prepare for interviews — to explain what was built, how it
> works, why each decision was made, and to answer probing technical questions. When
> studying with Claude, this is the file Claude reads to teach and quiz you.

---

## Table of Contents

1. [The 30-Second Pitch](#1-the-30-second-pitch)
2. [Why This Project Exists (Business Context)](#2-why-this-project-exists-business-context)
3. [The Tech Stack at a Glance](#3-the-tech-stack-at-a-glance)
4. [End-to-End Architecture](#4-end-to-end-architecture)
5. [The Data Source: USAJobs API](#5-the-data-source-usajobs-api)
6. [Stage 1 — Collection (`collect.py`)](#6-stage-1--collection-collectpy)
7. [Stage 2 — Transformation (`transform.py`)](#7-stage-2--transformation-transformpy)
8. [Stage 3 — Loading (`load.py`)](#8-stage-3--loading-loadpy)
9. [The Database Schema](#9-the-database-schema)
10. [Stage 4 — The Streamlit Dashboard (`app.py`)](#10-stage-4--the-streamlit-dashboard-apppy)
11. [Automation: GitHub Actions](#11-automation-github-actions)
12. [Key Results & Insights](#12-key-results--insights)
13. [Limitations & Future Enhancements](#13-limitations--future-enhancements)
14. [Design Decisions & Trade-offs (the "Why" behind everything)](#14-design-decisions--trade-offs)
15. [Interview Q&A](#15-interview-qa)
16. [How to Walk Through This Project Live](#16-how-to-walk-through-this-project-live)
17. [Glossary](#17-glossary)

---

## 1. The 30-Second Pitch

This project is a **fully automated ETL pipeline** that collects federal job postings from
the **USAJobs API every day**, cleans and standardizes the data, stores it in a **SQLite
database**, and surfaces the insights through an **interactive Streamlit dashboard**
deployed on Streamlit Community Cloud.

The pipeline runs **end-to-end with no manual intervention** — a scheduled GitHub Actions
job triggers it daily at 6 AM UTC. Over time it accumulates a growing historical dataset of
analyst, data, and technical roles across the federal government.

**One-line version:** "I built a self-updating data pipeline that turns thousands of
scattered federal job postings into a single queryable database and an interactive
dashboard, fully automated with GitHub Actions."

**Live dashboard:** https://usajobs-analytics-pipeline.streamlit.app
**GitHub repo:** https://github.com/nadeaujonny/usajobs-analytics-pipeline

---

## 2. Why This Project Exists (Business Context)

**The problem.** The U.S. federal government is one of the largest and most structured
employers in the country, but its hiring data is *scattered* across thousands of individual
postings on USAJobs.gov. There is no consolidated view of:

- Which agencies are hiring analyst/data roles
- What salaries look like by role, grade, and location
- Where demand is geographically concentrated

**Who has this pain.** Job seekers targeting federal analyst and data roles, plus workforce
planners and career advisors who guide candidates toward federal opportunities.

**The solution.** This pipeline aggregates the scattered postings into a **single,
queryable source that refreshes daily**. It converts a manual, repetitive search task into
an always-current analytics product.

**Why it's a good portfolio project.** It demonstrates the *full* data lifecycle —
API integration, ETL design, database modeling, automation/DevOps, and front-end
visualization — not just one slice. It is the kind of project that mirrors real data
engineering and analytics work.

---

## 3. The Tech Stack at a Glance

| Tool | Role in the project | Why it was chosen |
|---|---|---|
| **Python** | Core language for all four pipeline stages and the dashboard | General-purpose, strong data ecosystem |
| **requests** | HTTP calls to the USAJobs API | Standard, simple, supports headers/params/timeouts |
| **pandas** | Data manipulation, aggregation, filtering in the dashboard | Fast tabular operations |
| **SQLite** | Relational database storing the cleaned postings | Zero-config, file-based, no server needed |
| **Streamlit** | Interactive multi-page dashboard framework | Pure-Python UI, fast to build, free hosting |
| **Plotly** | Interactive charts (bar, histogram, scatter geo, pie, heatmap, line) | Rich interactivity, hover tooltips, maps |
| **GitHub Actions** | Scheduled daily pipeline execution (cron 6 AM UTC) | Free CI/CD, native to the GitHub repo |
| **Git / GitHub** | Version control + automated commits of the updated database | Source of truth; also the deployment trigger |
| **python-dotenv** | Loads the API key/email from a `.env` file locally | Keeps secrets out of source code |

---

## 4. End-to-End Architecture

The pipeline is built from **four standalone Python modules**. Each module can be run
independently for testing (each has an `if __name__ == "__main__":` block), but in
production they are chained together by GitHub Actions.

```
GitHub Actions (cron: 6 AM UTC daily)
        |
        v
  collect.py   ── Stage 1: COLLECT
  - Calls USAJobs Search API
  - 9 role keywords, each paginated
  - Retry logic (3 attempts per request)
  - Saves raw JSON to data/raw/raw_<timestamp>.json
        |
        v
  transform.py ── Stage 2: TRANSFORM
  - Reads the latest raw JSON file
  - Flattens the deeply nested API structure
  - Deduplicates by control_number
  - Classifies each posting into a role category
  - Parses salary strings; annualizes hourly pay
  - Returns a clean list of record dictionaries
        |
        v
  load.py      ── Stage 3: LOAD
  - Creates SQLite DB + tables if missing
  - INSERT OR IGNORE (skip duplicates across runs)
  - Logs each run to the pipeline_log table
        |
        v
  jobs.db (SQLite)
  - job_postings table (23 columns)
  - pipeline_log table (run audit trail)
        |
        v
  app.py (Streamlit) ── Stage 4: VISUALIZE
  - Deployed on Streamlit Community Cloud
  - 4 analytics pages + 1 data explorer
  - Sidebar filters: role, state, department
```

**Key architectural idea — separation of concerns.** Collection, transformation, and
loading are *separate modules* with clear inputs and outputs. This makes each stage easy to
test in isolation, debug, and reason about. The classic ETL = **E**xtract → **T**ransform →
**L**oad maps directly onto `collect.py` → `transform.py` → `load.py`.

**The "contract" between stages:**

- `collect.py` outputs a **raw JSON file** to `data/raw/`.
- `transform.py` reads that file and outputs an **in-memory list of clean dictionaries**.
- `load.py` takes that list and writes it to **`jobs.db`**.
- `app.py` reads **`jobs.db`** and renders the dashboard.

---

## 5. The Data Source: USAJobs API

**What it is.** The [USAJobs Search API](https://developer.usajobs.gov/) is a free,
public-domain data source maintained by the U.S. Office of Personnel Management (OPM). It
returns **currently open** federal job postings in JSON format.

**Access.** No paywall — just a free API key plus email registration. Authentication is via
HTTP headers:

```python
HEADERS = {
    "Authorization-Key": API_KEY,   # the free API key
    "User-Agent": EMAIL,            # the registered email
    "Host": "data.usajobs.gov"
}
```

The key and email are stored in environment variables (`USAJOBS_API_KEY`,
`USAJOBS_EMAIL`), loaded locally from a `.env` file via `python-dotenv` and provided as
GitHub Actions **secrets** in production. They are never committed to source code.

**Endpoint:** `https://data.usajobs.gov/api/Search`

**The 9 role categories searched** (the keywords passed to the API):

Data Analyst · Data Scientist · Data Engineer · Business Intelligence · Business Analyst ·
Statistician · Program Analyst · Management Analyst · IT Specialist

These cover the analyst, data, and technical job families most relevant to the data
analytics field.

**Important API behavior to know for interviews:**

- The Search API only returns **currently open** postings. Once a posting closes, the API
  no longer returns it. (The database *preserves* previously collected records, so the
  database grows even though the API view is always a snapshot.)
- The response is **deeply nested** — the useful fields are buried inside
  `MatchedObjectDescriptor`, `UserArea.Details`, `PositionLocation[]`, and
  `PositionRemuneration[]`. Flattening this nesting is the core job of `transform.py`.
- The same posting can be returned by **multiple keyword searches** (e.g., a "Data
  Scientist" posting may also match "data analyst"), which is exactly why deduplication is
  needed.

---

## 6. Stage 1 — Collection (`collect.py`)

**Job:** Call the USAJobs Search API for all 9 keywords, handle pagination and retries, and
save the raw responses to disk.

### Configuration
- `BASE_URL = "https://data.usajobs.gov/api/Search"`
- `RESULTS_PER_PAGE = 500` — the maximum the API allows per page (fewer API calls).
- `KEYWORDS` — the list of 9 search terms.
- Raw output directory: `data/raw/`.

### `fetch_keyword(keyword, max_retries=3, delay=5)`
Fetches **all** postings for a single keyword. Two loops are nested here:

1. **Pagination loop (`while True`).** Requests page 1, page 2, … For each page it builds
   the `params` dict (`Keyword`, `ResultsPerPage`, `Page`). It keeps going until either:
   - the page returns no items, or
   - `page * RESULTS_PER_PAGE >= total_results` (it has fetched everything available).

   `total_results` comes from `SearchResult.SearchResultCountAll` in the response.

2. **Retry loop (`for attempt in range(1, max_retries + 1)`).** Each HTTP request gets up
   to **3 attempts**. On a network error or bad JSON it waits `delay=5` seconds and tries
   again. If all 3 attempts fail, it gives up on that page and **returns whatever it has
   collected so far** (graceful degradation — a single bad page doesn't crash the run).

**Politeness / rate limiting:** `time.sleep(1)` between pages so the pipeline doesn't
hammer the API. Each request also has a **30-second timeout**.

**Error handling:** It catches `requests.RequestException` (covers connection errors,
timeouts, HTTP errors via `raise_for_status()`) and `json.JSONDecodeError` (malformed
response body).

### `collect_all()`
The orchestrator for this stage. It:
1. Creates `data/raw/` if it doesn't exist.
2. Builds a timestamp string: `YYYY-MM-DD_HHMMSS`.
3. Loops every keyword, calling `fetch_keyword`, accumulating results into a dict shaped
   `{keyword: [list of postings]}`.
4. Saves everything to a single file: `data/raw/raw_<timestamp>.json`.
5. Returns a summary dict (timestamp, total collected, output path, per-keyword counts).

**Output of the stage:** one timestamped raw JSON file containing every posting returned
for every keyword — *with duplicates still in it*. Deduplication happens in the next stage.

---

## 7. Stage 2 — Transformation (`transform.py`)

**Job:** Read the latest raw JSON, flatten the nested structure, clean and standardize the
data, deduplicate, and return a clean list of records ready for the database.

### `get_latest_raw_file()`
Finds the most recent file in `data/raw/`. It lists all `raw_*.json` files and takes the
last one **after an alphabetical sort**. This works *because* the timestamp filename format
(`YYYY-MM-DD_HHMMSS`) sorts chronologically when sorted alphabetically. (A subtle but
deliberate design choice — worth mentioning in interviews.)

### `parse_salary(salary_str)`
Converts a formatted salary string like `"$72,553.00"` into a number:
- Strips every character that isn't a digit or a dot using a regex: `re.sub(r'[^\d.]', '', salary_str)`.
- Converts to `float`.
- Returns `None` for missing, zero, or unparseable values (so bad data becomes a clean
  `NULL` rather than a misleading `0`).

### `classify_role(title, keyword)`
Assigns each posting to one of the 9 role categories using a **two-tier strategy**:
1. **Title first.** It checks the job title text for specific phrases ("data scientist",
   "data engineer", etc.). Title text is the most accurate signal.
2. **Keyword fallback.** If the title doesn't clearly match anything, it falls back to the
   search keyword that *returned* the posting via a `keyword_map` dictionary.
3. If neither matches, it returns `"Other"`.

This matters because one search keyword can return loosely related postings — classifying
by the actual title is more accurate than blindly trusting the keyword.

### `flatten_job(item, keyword)`
The heart of the transform. It digs into the nested API JSON and pulls out a **flat
dictionary** with one key per database column. Key extraction details:

- The real content lives under `item["MatchedObjectDescriptor"]`; agency detail lives under
  `UserArea.Details`.
- **Location:** a posting can have multiple locations — the code takes the **first** one
  (`PositionLocation[0]`) for `city`, `state`, `latitude`, `longitude`, etc.
- **Salary:** pulled from `PositionRemuneration[0]` — `MinimumRange`, `MaximumRange`, and
  `Description` (the pay interval, e.g. "Per Year" / "Per Hour").
- **Hourly-to-annual conversion:** if the interval contains the word "hour", the min and
  max are multiplied by **2,087** — the OPM standard number of work hours in a year. This
  makes all salaries comparable on an annual basis.
- **Salary midpoint:** `salary_mid = (salary_min + salary_max) / 2` — a single
  representative number used throughout the dashboard.
- **`control_number`** is taken from the API's `PositionID` field — the unique identifier
  for a posting, and the primary key of the database.

### `transform_raw_file(filepath=None)`
The orchestrator for this stage. It:
1. Reads the raw JSON dict (`{keyword: [items]}`).
2. Loops every keyword and every item, calling `flatten_job`.
3. **Deduplicates** using a `seen_control_numbers` set — the first time a control number is
   seen the record is kept; later occurrences are skipped.
4. Prints raw count, post-dedup count, and duplicates removed.
5. Returns the clean list of record dictionaries.

**Why dedup here:** the same posting matched several keyword searches. This step makes the
posting **unique per run** before it ever reaches the database.

---

## 8. Stage 3 — Loading (`load.py`)

**Job:** Create the SQLite database if needed, insert new records, skip ones already
present, and log the run.

### `get_connection()`
Opens a connection to `data/jobs.db` (creating the folder if needed) and sets
`PRAGMA journal_mode=WAL`. **WAL (Write-Ahead Logging)** allows reads and writes to happen
concurrently — useful because the dashboard may read the database while the pipeline
writes to it.

### `create_tables(conn)`
Runs `CREATE TABLE IF NOT EXISTS` for both tables (`job_postings` and `pipeline_log`). The
`IF NOT EXISTS` clause makes the function safe to call on every run — it builds the schema
the first time and is a no-op afterward.

### `load_records(records, source="daily")`
The core loader:
1. Defines the 23-column order explicitly.
2. Builds a parameterized SQL string:
   `INSERT OR IGNORE INTO job_postings (...) VALUES (?, ?, …)`.
3. Loops every record, executes the insert, and uses `cursor.rowcount` to tell whether the
   row was actually **inserted** (`rowcount > 0`) or **skipped** (already in the DB).
4. Writes one row to `pipeline_log` describing the run (timestamp, counts, source).
5. Commits, reads the total row count, and returns a summary dict.

**`INSERT OR IGNORE` — the key concept.** Because `control_number` is the PRIMARY KEY,
trying to insert a posting that's already in the database **silently fails for that row**
instead of raising an error. Result: each daily run only adds *genuinely new* postings, and
the database **accumulates history** without duplicates. This is what makes the pipeline
**idempotent** — running it twice does no harm.

> **Honest nuance to know for interviews:** `INSERT OR IGNORE` is *insert-only*. If an
> existing posting's details change (salary edited, close date moved), the database keeps
> the **original** version — it is never updated. A true "upsert" would use
> `INSERT … ON CONFLICT(control_number) DO UPDATE …`. The project documentation calls this
> "upsert logic," but precisely speaking it is *insert-if-new*. Being able to explain this
> distinction shows depth.

### Parameterized queries
Values are passed as `?` placeholders, never string-formatted into the SQL. This prevents
**SQL injection** and handles quoting/escaping/`NULL`s correctly.

---

## 9. The Database Schema

Two tables in a single SQLite file, `jobs.db`.

### `job_postings` — 23 columns

| Group | Columns |
|---|---|
| **Primary key** | `control_number` (unique posting ID, from the API's `PositionID`) |
| **Position** | `position_title`, `organization_name`, `department_name`, `sub_agency` |
| **Compensation** | `job_grade`, `pay_plan`, `salary_min`, `salary_max`, `salary_mid`, `salary_interval` |
| **Location** | `location_name`, `city`, `state`, `country`, `latitude`, `longitude` |
| **Metadata** | `position_url`, `open_date`, `close_date`, `role_category`, `search_keyword`, `collected_date` |

Column types are SQLite's flexible types — `TEXT` for strings, `REAL` for the numeric
salary and coordinate fields.

### `pipeline_log` — run audit trail

| Column | Meaning |
|---|---|
| `id` | Auto-incrementing primary key |
| `run_timestamp` | When the run happened |
| `records_collected` | Records seen by the loader |
| `records_after_dedup` | Records remaining after in-run dedup |
| `records_inserted` | Genuinely new rows added this run |
| `records_skipped` | Rows already in the DB (ignored) |
| `source` | Run type (e.g. `"daily"`) |

**Why a log table matters:** it gives an **audit trail**. You can answer "did the pipeline
run today? how many new postings did it find?" by querying one table — essential for
monitoring an automated system you can't watch run.

---

## 10. Stage 4 — The Streamlit Dashboard (`app.py`)

**Job:** Read `jobs.db` and present an interactive, multi-page analytics dashboard.

### App setup
- `st.set_page_config(...)` — wide layout, page title, 🏛️ icon.
- **Data loading is cached:** `@st.cache_data(ttl=3600)` wraps `load_data()`, which runs
  `SELECT * FROM job_postings` into a pandas DataFrame. The cache holds for **1 hour
  (3600 s)**, so the database isn't re-queried on every interaction — the app stays fast,
  and it refreshes hourly to pick up new data.

### Sidebar filters (apply to every page)
Three `st.multiselect` filters: **Role Category**, **State**, **Department**. The selected
values are applied to a copy of the DataFrame (`filtered`). Role Category defaults to "all
selected"; State and Department default to empty (= no filter). Every page renders from
`filtered`, so the filters are global.

### Navigation
`st.sidebar.radio` switches between 5 pages.

#### Page 1 — Executive Overview
High-level snapshot. Four **KPI cards** (`st.metric`): Total Postings, Avg Salary (Mid),
Agencies Hiring, States with Postings. Then four charts: postings by role category (horizontal
bar), postings by department top-10 (horizontal bar), salary distribution (histogram),
top-10 states (bar).

#### Page 2 — Salary Analysis
Four summary KPIs (median / average / min / max salary). Then: median salary by role
category, median salary by state (top 15, **requiring at least 3 postings** so tiny samples
don't distort the ranking), and salary by job grade (a line chart showing GS-grade
progression).

> The grade chart filters to grades that are **purely numeric** via
> `str.match(r"^\d+$")`. Promotion-ladder grades like `"13/14"` are excluded — a known
> limitation (see §13).

#### Page 3 — Geographic Demand
An interactive **US map** (`px.scatter_geo`, scope `"usa"`) plotting every posting with
coordinates, color-coded by role. Then top-15 states and top-15 cities bar charts, and a
**location-type pie chart** that buckets postings into Single Location / Multiple Locations
/ Negotiable.

#### Page 4 — Agency Analysis
Top-15 hiring organizations (bar), a department share **pie chart**, average salary by
department (top 10, min 3 postings), and a **role-by-department heatmap** (`px.imshow` over
a `pd.crosstab`) showing which departments favor which role categories.

#### Page 5 — Data Explorer
A searchable, sortable raw-data table. A text box filters `position_title`; the table shows
a curated column set sorted by `open_date`; a **download button** exports the filtered data
as CSV.

### Charting
All charts use **Plotly Express** (`px`) for interactivity — hover tooltips, zoom, pan.
Chart types used: horizontal/vertical bar, histogram, scatter-geo map, pie, line, and
heatmap.

---

## 11. Automation: GitHub Actions

The pipeline is fully automated by a **GitHub Actions workflow** (a YAML file in the repo's
`.github/workflows/` folder).

- **Trigger:** a `cron` schedule — **6 AM UTC every day**.
- **What it does:** checks out the repo, installs Python dependencies, runs the pipeline
  (collect → transform → load), and commits the updated `jobs.db` back to the repository.
- **Secrets:** the USAJobs API key and email are stored as **GitHub Actions secrets**, not
  in code.
- **Deployment link:** because the database is committed to the repo and the Streamlit app
  is deployed from that same repo, **Streamlit Community Cloud automatically redeploys**
  when the database file changes — so the live dashboard reflects the newest data without
  any manual step.

**The big picture:** *no human ever touches the pipeline after setup.* It collects,
cleans, loads, commits, and redeploys on its own — and the database grows into a historical
dataset one day at a time.

---

## 12. Key Results & Insights

**Data volume:** the initial collection pulled **1,632 raw postings** across the 9
keywords. After deduplication by `control_number`, **1,131 unique postings** were loaded
into the database. (The ~500 difference = the same postings matching multiple keyword
searches.)

**Headline insights from the dashboard:**

- **IT Specialist dominates volume.** It far outnumbers other categories — the federal
  government uses that classification broadly for technology roles.
- **The VA is the top hiring department.** Consistent with the Department of Veterans
  Affairs being the largest civilian federal employer (healthcare, benefits, IT at scale).
- **Salaries cluster at $100K–$150K.** Reflects the GS-12 to GS-14 pay bands most analyst
  roles fall into.
- **DC / Virginia / Maryland lead** in both posting volume *and* salary — federal HQs
  concentrate in the DC metro, and locality pay there is among the highest.
- **Data Scientists and Data Engineers earn the most** by role — specialized skills plus
  private-sector competition push compensation up.
- **Clear GS-grade salary progression** — a predictable step pattern confirms the
  structured federal pay system.
- **Some flexibility exists** — a portion of postings list "Negotiable" or "Multiple
  Locations" duty stations.

---

## 13. Limitations & Future Enhancements

### Known limitations (be ready to volunteer these — it shows maturity)

1. **No historical backfill.** The USAJobs Historical API doesn't support filtering by
   keyword/role, so the database can only start from the pipeline's launch date. Postings
   open *before* launch can't be retroactively collected.
2. **Only open postings are captured.** The Search API returns currently-open postings
   only. A posting that opens *and* closes between two daily runs is missed entirely.
3. **Grade-format parsing gap.** The salary-by-grade chart only accepts purely numeric
   grades (`"13"`, `"14"`). Promotion-ladder grades (`"13/14"`) are excluded, reducing the
   chart's coverage.
4. **`INSERT OR IGNORE` never updates.** If a live posting's details change, the database
   keeps the original (see §8).
5. **Only the first location is stored.** Multi-location postings lose their other duty
   stations because `flatten_job` takes `PositionLocation[0]`.

### Future enhancements

- **Trends over time.** As daily snapshots accumulate, add a "Trends" page tracking
  posting volume / salary / role mix week-over-week and month-over-month.
- **New-posting alerts.** Email/webhook notifications when postings match saved criteria
  (e.g., "Data Scientist above GS-13 in Texas").
- **PostgreSQL migration.** If data volume grows large, move from SQLite to PostgreSQL for
  better concurrency and querying under load.
- **Better grade parsing.** Handle promotion-ladder grades by extracting the target grade
  or displaying the full range.

---

## 14. Design Decisions & Trade-offs

Interviewers love "why" questions. Here are the deliberate choices and their rationale.

**Why four separate modules instead of one script?**
Separation of concerns. Each stage has a single responsibility, a clear input/output
contract, and its own `__main__` test block. You can debug transformation without
re-hitting the API, or re-load without re-transforming.

**Why save raw JSON to disk between collect and transform?**
Traceability and replayability. The raw response is preserved with a timestamp, so you can
re-run the transform against historical raw data, debug a parsing bug, or audit exactly
what the API returned on a given day. It also decouples a slow, network-bound stage from a
fast, CPU-bound one.

**Why SQLite instead of PostgreSQL or a cloud database?**
It's zero-configuration and file-based — no server to run or pay for. The database file
lives in the Git repo, which doubles as the deployment mechanism for Streamlit. For this
data volume (low thousands of rows) SQLite is more than enough. PostgreSQL is the planned
upgrade *if* volume grows.

**Why `INSERT OR IGNORE` keyed on `control_number`?**
It makes the pipeline **idempotent** — safe to run repeatedly. New postings are added;
already-seen ones are skipped automatically. The database accumulates a clean, deduplicated
history with no orchestration logic needed.

**Why deduplicate twice (in transform *and* in load)?**
They solve different problems. Transform dedups *within a single run* — the same posting
returned by multiple keyword searches. Load dedups *across runs* — a posting collected
today that was already collected yesterday.

**Why cache the dashboard data with a 1-hour TTL?**
Without caching, every filter click would re-query SQLite and reload the whole table —
slow. The 1-hour TTL is a balance: fast interaction, but fresh enough to pick up the daily
update soon after it lands.

**Why classify roles by title first, keyword second?**
The job title is the most accurate signal of what a role actually is. The search keyword is
a weaker signal (a keyword search returns loosely related results), so it's only a fallback.

**Why annualize hourly salaries with 2,087 hours?**
2,087 is the OPM (Office of Personnel Management) standard for work hours in a year. Using
it makes hourly and annual postings directly comparable on one salary axis.

**Why retry logic with 3 attempts?**
APIs fail transiently — network blips, timeouts, brief outages. Three attempts with a delay
absorb most transient failures. If all three fail, the pipeline degrades gracefully
(returns partial data) rather than crashing the whole run.

---

## 15. Interview Q&A

Practice answering these out loud. Model answers are written the way you'd actually speak.

**Q1． Walk me through this project end to end.**
"It's an automated ETL pipeline for federal job-market data. Every morning a GitHub Actions
job kicks off. Stage one, `collect.py`, calls the USAJobs API for nine analyst and tech
keywords, handles pagination and retries, and dumps the raw JSON to disk. Stage two,
`transform.py`, flattens that deeply nested JSON, parses and standardizes salaries,
classifies each posting into a role category, and deduplicates. Stage three, `load.py`,
inserts the clean records into a SQLite database using `INSERT OR IGNORE` so it only adds
new postings. Then a Streamlit dashboard, deployed on Streamlit Cloud, reads that database
and lets you explore hiring volume, salaries, geography, and agencies interactively. The
whole thing runs daily with zero manual work."

**Q2． What was the hardest part?**
"Flattening the API response. USAJobs returns deeply nested JSON — the fields I needed were
buried several levels down inside `MatchedObjectDescriptor`, `UserArea`,
`PositionRemuneration`, and a list of locations. I had to write defensive extraction code
that survives missing keys and empty lists, then map all of it onto a clean flat schema."

**Q3． How do you avoid duplicate records?**
"Two layers. Within a single run, the same posting can come back from multiple keyword
searches, so `transform.py` tracks a set of seen control numbers and keeps only the first.
Across runs, `load.py` uses `INSERT OR IGNORE` on a primary key — the control number — so a
posting already in the database is silently skipped. Together they keep the database clean
and let it accumulate history."

**Q4． What is `control_number` and why is it the primary key?**
"It's the unique identifier for a posting — it comes from the API's `PositionID` field.
Making it the primary key is what enables `INSERT OR IGNORE` to work as deduplication: the
database itself enforces uniqueness, so I don't need any extra logic to check whether a
record already exists."

**Q5． Is `INSERT OR IGNORE` really an upsert?**
"Not strictly. It's insert-if-new — if the posting already exists, the new row is just
dropped, so existing rows are never updated. A true upsert would use
`ON CONFLICT DO UPDATE`. For this project that's an acceptable trade-off because postings
are fairly static once published, but if I needed to track edits to a posting I'd switch to
a real upsert."

**Q6． How does the pipeline handle API failures?**
"Each HTTP request gets up to three attempts with a five-second delay. I catch both request
exceptions and JSON decode errors, and every request has a 30-second timeout. If all three
attempts fail on a page, the function returns the data it already has instead of crashing —
so one bad page degrades gracefully rather than killing the whole run."

**Q7． How does pagination work?**
"The API returns up to 500 results per page. For each keyword I loop pages, and after each
page I compare how many results I've fetched against `SearchResultCountAll` from the
response. Once I've fetched everything available — or a page comes back empty — I stop.
There's also a one-second pause between pages to be polite to the API."

**Q8． Why SQLite and not a 'real' database?**
"For this scale — low thousands of rows — SQLite is the right call. It's file-based and
needs no server, the database file ships inside the Git repo, and that's also what triggers
the Streamlit redeploy. If the dataset grew large or needed heavy concurrent access, I'd
migrate to PostgreSQL, which is already in my future-enhancements list."

**Q9． How is the dashboard kept fast?**
"The data load is wrapped in Streamlit's `cache_data` with a one-hour TTL. Without it,
every filter interaction would re-query SQLite and reload the entire table. With caching,
the query runs at most once an hour, and the TTL keeps it fresh enough to show the daily
update."

**Q10． How do you keep the API key secure?**
"It's never in the code. Locally it lives in a `.env` file loaded with python-dotenv and
the `.env` is git-ignored. In production it's a GitHub Actions secret injected as an
environment variable at runtime."

**Q11． How would you scale or extend this?**
"A few directions. A trends page once enough daily snapshots accumulate — that's the real
payoff of running it daily. Alerting when postings match saved criteria. PostgreSQL if
volume grows. And better grade parsing to handle promotion-ladder formats like '13/14'."

**Q12． What does annualizing salary mean and why do it?**
"Some postings quote pay per hour, others per year. To compare them I detect the 'Per Hour'
interval and multiply by 2,087 — the OPM standard work hours in a year. That puts every
posting on a single annual salary axis so charts and averages are meaningful."

**Q13． How does role classification work, and why two tiers?**
"First I scan the job title for specific phrases — the title is the most accurate signal of
what a role is. If the title doesn't clearly match, I fall back to the search keyword that
returned the posting. A keyword search returns loosely related results, so it's a weaker
signal and only a backup. Anything that matches neither is labeled 'Other'."

**Q14． What would break if the API changed its response shape?**
"`transform.py`'s `flatten_job` would be the failure point — it's coupled to the nested
field names. I use `.get()` with defaults everywhere so missing fields produce nulls rather
than crashes, but a structural rename would silently produce empty columns. A good
safeguard would be schema validation on the raw response, plus alerting if a run inserts
zero records."

**Q15． How do you know the pipeline ran successfully?**
"The `pipeline_log` table. Every run writes a row with the timestamp and counts —
collected, after dedup, inserted, skipped. That's the audit trail. I can query it to
confirm the job ran and see how many new postings it found, which matters a lot for an
automated process nobody is watching."

---

## 16. How to Walk Through This Project Live

If asked to screen-share and walk through the code, use this order:

1. **Start with the dashboard** (the live URL). Show the four analytics pages and the
   filters — lead with the *outcome*, the thing a user actually sees.
2. **Show the architecture diagram** (§4). Frame it as classic ETL: extract → transform →
   load → visualize.
3. **`collect.py`** — point to `fetch_keyword`: the pagination loop and the retry loop.
   Emphasize graceful degradation.
4. **`transform.py`** — point to `flatten_job` (the nested-JSON flattening), `parse_salary`
   + the 2,087 annualization, and the dedup set in `transform_raw_file`.
5. **`load.py`** — point to `INSERT OR IGNORE` and explain idempotency; show the
   `pipeline_log` insert.
6. **`app.py`** — point to `@st.cache_data`, the sidebar filters, and one Plotly chart.
7. **Close with automation** — the GitHub Actions cron and the auto-redeploy loop.
8. **Volunteer a limitation** (§13) before they ask — it signals engineering maturity.

**Pacing tip:** spend most of the time on `transform.py`. It has the most real logic and
the best stories (nested JSON, dedup, salary normalization). Collection and loading are
quicker to cover.

---

## 17. Glossary

- **ETL** — Extract, Transform, Load. The three-stage pattern this pipeline follows.
- **API** — Application Programming Interface; here, the USAJobs endpoint returning job
  data as JSON.
- **Pagination** — splitting a large result set into pages; the pipeline loops pages of
  500 results until it has them all.
- **Idempotent** — an operation safe to run repeatedly with the same result. `INSERT OR
  IGNORE` makes the load stage idempotent.
- **Upsert** — "update or insert." `INSERT OR IGNORE` is a *partial* upsert — insert-if-new
  with no update.
- **Primary key** — a column whose value is unique per row; here `control_number`.
- **Deduplication** — removing repeated records; done within a run (a set) and across runs
  (the primary key).
- **WAL (Write-Ahead Logging)** — a SQLite mode allowing concurrent reads and writes.
- **Cron** — a time-based scheduler; `0 6 * * *` means 6 AM UTC daily.
- **CI/CD** — Continuous Integration / Continuous Deployment; GitHub Actions provides it
  here.
- **TTL (Time To Live)** — how long a cached value stays valid; the dashboard cache uses
  3600 seconds.
- **KPI** — Key Performance Indicator; the metric cards at the top of the dashboard pages.
- **GS grade** — General Schedule, the federal government's structured pay-grade system.
- **OPM** — U.S. Office of Personnel Management, which runs USAJobs and sets the 2,087-hour
  standard.
- **Environment variable / secret** — a value (like the API key) provided at runtime
  instead of being written into the code.

---

*This study guide documents the project as built. When in doubt, the source files —
`code/collect.py`, `code/transform.py`, `code/load.py`, `code/app.py`, and `index.md` —
are the authoritative reference.*
