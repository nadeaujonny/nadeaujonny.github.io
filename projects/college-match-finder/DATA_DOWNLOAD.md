# Data Download Instructions

All raw data for this project is free and public. Download each file below
and place it (unzipped) into `data/raw/`. The `data_prep.py` script reads
files from that folder by the exact filenames listed.

After download and placement, your `data/raw/` folder should contain:

```
data/raw/
├── Most-Recent-Cohorts-Institution.csv
├── Most-Recent-Cohorts-Field-of-Study.csv
├── MERGED2019_20_PP.csv
├── MERGED2021_22_PP.csv
├── Criminal_Offenses_On_campus.csv
└── zip_lat_long.csv
```

---

## 1. College Scorecard — Current Institution-Level Data

**What it is:** One row per U.S. Title IV college with thousands of columns
covering cost, admissions, outcomes, earnings, and debt. This is the main
file that drives the app.

**Where to get it:** <https://collegescorecard.ed.gov/data/>
- Under "Featured Downloads," click **Most Recent Cohorts (Institution-Level Data)**.
- Direct link (as of late 2025):
  <https://ed-public-download.scorecard.network/downloads/Most-Recent-Cohorts-Institution_10032025.zip>

**File to keep:** After unzipping, the file is named something like
`Most-Recent-Cohorts-Institution_10032025.csv`. **Rename it to
`Most-Recent-Cohorts-Institution.csv`** (drop the date suffix) and place
it in `data/raw/`.

---

## 2. College Scorecard — Field of Study Data

**What it is:** Program-level earnings and debt, by CIP code. Used for
major-specific results in the detail cards.

**Where to get it:** Same page as above, under "Featured Downloads," click
**Most Recent Cohorts (Field of Study Data)**.
- Direct link:
  <https://ed-public-download.scorecard.network/downloads/Most-Recent-Cohorts-Field-of-Study_04172025.zip>

**File to keep:** Unzip and rename to
`Most-Recent-Cohorts-Field-of-Study.csv`.

---

## 3. College Scorecard — Historical Snapshots (for trend arrows)

**What it is:** Two older institution-level snapshots. The app compares
current values against these to compute trend arrows (↑/↓/↔).

**Where to get it:** <https://collegescorecard.ed.gov/data/>
- Scroll to the **"All Data Files"** section.
- Download the zip labeled **"All Data"** (it contains many `MERGED*.csv` files,
  one per academic year).
- Direct link:
  <https://ed-public-download.scorecard.network/downloads/CollegeScorecard_Raw_Data.zip>

**Files to keep:** From the unzipped archive, extract just these two and
place them in `data/raw/`:
- `MERGED2019_20_PP.csv` — snapshot from ~4 years ago
- `MERGED2021_22_PP.csv` — snapshot from ~2 years ago

Delete the rest of the archive unless you want them for other analyses;
they are large (~1 GB total).

---

## 4. Data Dictionary (optional but highly recommended)

**What it is:** An Excel file that documents every column in the Scorecard
files. Useful for reference; not read by the app.

**Where to get it:**
<https://collegescorecard.ed.gov/assets/CollegeScorecardDataDictionary.xlsx>

Place it wherever you like — `data/` or `docs/`.

---

## 5. Clery Act Campus Safety Data

**What it is:** Counts of reported on-campus criminal offenses by institution,
year, and category (burglary, motor vehicle theft, robbery, aggravated
assault, etc.). Legally mandated reporting under the Clery Act.

**Where to get it:** <https://ope.ed.gov/campussafety/>
- Click **"Download Custom Data File"** (or similar — the UI changes periodically).
- Select **"Criminal Offenses"** as the data category.
- Select the most recent reporting year (typically 2 years behind the current year).
- Download as CSV.

**File to keep:** Rename to `Criminal_Offenses_On_campus.csv` and place
in `data/raw/`.

**Note:** If the ED Clery download tool is down or schemas changed, an
alternative is the IPEDS Safety and Security component from NCES, which
covers the same data. We will flag column differences in `data_prep.py`
if they appear.

---

## 6. ZIP Code → Latitude/Longitude Lookup

**What it is:** A mapping from U.S. ZIP codes to lat/long coordinates,
used to compute the user's distance to each campus.

**Where to get it:** Free from SimpleMaps.
- <https://simplemaps.com/data/us-zips>
- Click the **"Basic — Free"** download. A `.zip` downloads.
- Unzip and open `uszips.csv`. We only need three columns: `zip`, `lat`, `lng`.

**File to keep:** Rename the unzipped file to `zip_lat_long.csv` (keep all
columns; `data_prep.py` will subset and clean it). Place in `data/raw/`.

---

## Summary checklist

Before running `data_prep.py`, confirm:

- [ ] `data/raw/Most-Recent-Cohorts-Institution.csv` exists (~1 GB)
- [ ] `data/raw/Most-Recent-Cohorts-Field-of-Study.csv` exists (~500 MB)
- [ ] `data/raw/MERGED2019_20_PP.csv` exists
- [ ] `data/raw/MERGED2021_22_PP.csv` exists
- [ ] `data/raw/Criminal_Offenses_On_campus.csv` exists
- [ ] `data/raw/zip_lat_long.csv` exists

If all six are present, you are ready for Phase 1's prep script.

---

## Phase 9 Raw Files

These three files support the BLS Occupational Layer (Phase 9), which maps
college majors to occupations and attaches wage and job-growth data. All are
free and public. Place them (unzipped) in `data/raw/`.

**Cycle:** CIP 2020 / SOC 2018 crosswalk; May 2024 OEWS; 2024–34 Employment
Projections. Earlier planning docs referenced the 2023–33 / May 2023 cycle;
those references are superseded.

---

### 7. NCES CIP 2020 → SOC 2018 Crosswalk

**File:** `data/raw/CIP2020_SOC2018_Crosswalk.xlsx`
**Approx size:** ~250 KB
**Refresh cadence:** Updated alongside CIP edition revisions (currently CIP 2020). No annual refresh.
**Source:** <https://nces.ed.gov/ipeds/cipcode/Files/CIP2020_SOC2018_Crosswalk.xlsx>

**What it is:** A many-to-many mapping between 6-digit CIP codes (Classification
of Instructional Programs, 2020 edition) and 6-digit SOC codes (Standard
Occupational Classification, 2018 edition). Used in Phase 9 to route each
college major to its likely occupation destinations. The primary sheet is
`CIP-SOC` (6,097 mapping rows). Read with `dtype=str` to prevent pandas from
corrupting leading-zero CIP codes.

---

### 8. BLS OEWS National May 2024

**File:** `data/raw/national_M2024_dl.xlsx`
**Approx size:** ~700 KB
**Refresh cadence:** Annual. May 20XX release published roughly April of the following year. Next: May 2025 expected April 2026.
**Source:** <https://www.bls.gov/oes/special-requests/oesm24nat.zip> (unzip; keep the inner XLSX)

**What it is:** National Occupational Employment and Wage Statistics for May 2024,
one row per detailed SOC code (831 rows after filtering to
`I_GROUP == 'cross-industry'` and `O_GROUP == 'detailed'`). Provides mean and
percentile wages (annual and hourly) plus total employment counts. Primary wage
source for Phase 9.

---

### 9. BLS Employment Projections — Occupation Table 2024–34

**File:** `data/raw/occupation.xlsx`
**Approx size:** ~600 KB
**Refresh cadence:** Biennial. 2024–34 cycle released August 28, 2025. Next cycle (2026–36) expected late 2027.
**Source:** <https://www.bls.gov/emp/ind-occ-matrix/occupation.xlsx>

**What it is:** BLS 10-year occupational employment projections. The primary
sheet is `Table 1.2` (read with `header=1`), filtered to
`Occupation type == 'Line item'` for 832 detailed SOC rows. Provides 2024–34
percent employment change, annual job openings, and typical education
requirements. Primary growth-rate source for Phase 9.

---

## Phase 10 Raw Files

These four files support the Geographic and Work Context layer (Phase 10), which adds state-level employment concentration (choropleth) and per-occupation work-environment ratings. All are free and public. Place them (unzipped, with original filenames) in `data/raw/`.

**Cycle:** May 2024 OEWS State (matches the May 2024 national release used in Phase 9); O*NET 30.2 (released February 2026). The O*NET Interests file is also captured here as a Phase 12 prerequisite so all O*NET dependencies are pinned to release 30.2.

---

### 10. BLS OEWS State May 2024

**File:** `data/raw/state_M2024_dl.xlsx`
**Approx size:** ~7.5 MB (combined-state file, extracted from `oesm24st.zip`)
**Refresh cadence:** Annual. Same release schedule as the national file (entry #8). Next: May 2025 expected April 2026.
**Source:** <https://www.bls.gov/oes/special-requests/oesm24st.zip> (unzip; the combined-state file is the one used)

**What it is:** State-level Occupational Employment and Wage Statistics for May 2024, one row per area-SOC-O_GROUP combination across 54 areas (50 states + DC + Puerto Rico + Guam + Virgin Islands). 37,609 rows total; 36,367 detailed SOC rows after filtering to `O_GROUP == 'detailed'`. Provides total employment, location quotient, and wage percentiles per state-occupation cell. Phase 10's choropleth uses `LOC_QUOTIENT` as the primary metric (more robust to BLS suppression than raw employment counts). Read with `dtype=str` for consistency with Phase 9 patterns. Use `PRIM_STATE` (2-letter postal code) for Plotly choropleth joins.

---

### 11. O\*NET 30.2 Work Context

**File:** `data/raw/Work Context.xlsx` (preserve the space in the filename)
**Approx size:** ~14 MB
**Refresh cadence:** Quarterly minor releases; primary update Q3 each year.
**License:** CC BY 4.0 (attribution required — see `data/raw/RAW_DATA_NOTES.md`)
**Source:** <https://www.onetcenter.org/dl_files/database/db_30_2_excel/Work%20Context.xlsx>

**What it is:** Per-occupation work environment ratings across 57 elements (hours worked, time pressure, autonomy, physical demands, etc.) for 894 O\*NET-SOC occupations. 297,676 rows total across 4 Scale ID variants (CX, CXP, CT, CTP); Phase 10.5 uses only the 49,170 rows where `Scale ID == 'CX'` (mean numeric ratings). O\*NET-SOC codes are 8-digit (e.g., `15-1252.00`); strip the `.XX` suffix to join to BLS SOC2018. Drop rows where `Recommend Suppress == 'Y'` before averaging.

---

### 12. O\*NET 30.2 Work Context Categories

**File:** `data/raw/Work Context Categories.xlsx`
**Approx size:** <100 KB
**Refresh cadence:** Same as Work Context.
**License:** CC BY 4.0
**Source:** <https://www.onetcenter.org/dl_files/database/db_30_2_excel/Work%20Context%20Categories.xlsx>

**What it is:** Lookup file (281 rows) for decoding the categorical CXP and CTP rows in the Work Context file. Not used in Phase 10; pinned to release 30.2 for future polish (e.g., a "see breakdown" hover in Phase 14).

---

### 13. O\*NET 30.2 Interests (Phase 12 prerequisite)

**File:** `data/raw/Interests.xlsx`
**Approx size:** <500 KB
**Refresh cadence:** Same as Work Context.
**License:** CC BY 4.0
**Source:** <https://www.onetcenter.org/dl_files/database/db_30_2_excel/Interests.xlsx>

**What it is:** Per-occupation RIASEC interest scores for ~890 occupations. 8,307 rows across 9 elements: the 6 RIASEC dimensions (Realistic, Investigative, Artistic, Social, Enterprising, Conventional) plus First/Second/Third Interest High-Point codes that pre-rank each occupation's top three RIASEC dimensions. Not used in Phase 10; locks Phase 12's RIASEC questionnaire matching to O\*NET 30.2.