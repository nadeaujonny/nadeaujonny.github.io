# Master Outline & Study Guide
## Nashville Housing Data Cleaning & Transformation (MySQL)

> **Purpose of this document:** A complete, self-contained reference for studying this
> portfolio project. Use it to prepare for interviews — to explain what was built, how it
> works, why each decision was made, and to answer probing technical questions. When
> studying with Claude, this is the file Claude reads to teach and quiz you.
>
> **One sentence to anchor everything:** This is an end-to-end **SQL data-cleaning**
> project in MySQL — it takes 56,000+ raw Nashville property records and, through a
> disciplined **raw → staging → clean** workflow, fixes data types, fills missing values
> with a self-join, removes duplicates, trims whitespace, and ships a clean view — and it
> exists specifically to demonstrate the **DDL/DML side of SQL** (the *transform* half),
> as a companion to the e-commerce project's SELECT-side analytics.

---

## Table of Contents

1. [The 30-Second Pitch](#1-the-30-second-pitch)
2. [Why This Project Exists (Context)](#2-why-this-project-exists-context)
3. [The Tech Stack & Dataset](#3-the-tech-stack--dataset)
4. [The raw → staging → clean Workflow](#4-the-raw--staging--clean-workflow)
5. [Data Quality Assessment](#5-data-quality-assessment)
6. [Step 1 — Standardize the Date Format](#6-step-1--standardize-the-date-format)
7. [Step 2 — Populate Missing Addresses (Self-Join)](#7-step-2--populate-missing-addresses-self-join)
8. [Step 3 — Clean Text Fields (Whitespace)](#8-step-3--clean-text-fields-whitespace)
9. [Step 4 — Remove Duplicate Rows](#9-step-4--remove-duplicate-rows)
10. [Step 5 — Drop Unused Columns](#10-step-5--drop-unused-columns)
11. [Final Output — View & Indexes](#11-final-output--view--indexes)
12. [Stretch Goals — EXPLAIN, Transactions, Stored Procedure](#12-stretch-goals--explain-transactions-stored-procedure)
13. [SQL Concepts to Know Cold](#13-sql-concepts-to-know-cold)
14. [Limitations & Honest Caveats](#14-limitations--honest-caveats)
15. [Interview Q&A](#15-interview-qa)
16. [How to Walk Through This Project Live](#16-how-to-walk-through-this-project-live)
17. [Glossary](#17-glossary)

---

## 1. The 30-Second Pitch

This is an **end-to-end SQL data-cleaning project** built in **MySQL** on the **Nashville
Housing dataset** from Kaggle — ~**56,636 rows, 29 columns** of Nashville property sales
from 2013–2016.

It walks the full transformation lifecycle: create a database, import the raw CSV, build a
**staging copy** to protect the original, **assess data quality**, then systematically
clean the data in five steps — **(1)** convert the sale-date text to a real DATE type,
**(2)** fill blank property addresses using a **self-join** on Parcel ID, **(3)** trim
whitespace from 10 text columns, **(4)** remove **104 duplicate rows** with `ROW_NUMBER()`,
**(5)** drop unused columns — and finishes by shipping a **clean reusable VIEW**,
**performance indexes**, and a **stored procedure** that can re-run the whole pipeline.

The deliberate purpose: it demonstrates the **DDL/DML side of SQL** — `CREATE`, `ALTER`,
`UPDATE`, `DELETE`, the *transform* half of the language — as the intentional companion to
the BigQuery e-commerce project, which covers the *query/analytics* half (CTEs, window
functions, joins). Together the two cover the full practical SQL spectrum.

**One-line version:** "I built an end-to-end SQL data-cleaning pipeline in MySQL — a
disciplined raw-to-staging-to-clean workflow that fixes types, fills missing data with a
self-join, deduplicates with ROW_NUMBER(), and ships a clean view plus a re-runnable stored
procedure on 56,000+ housing records."

---

## 2. Why This Project Exists (Context)

**The premise.** Data cleaning is the foundational, unglamorous skill of every analytics
role — **real-world datasets almost never arrive analysis-ready**. Before you can run a
single meaningful query, you have to fix types, fill gaps, remove duplicates, and
standardize text. This project demonstrates exactly that workflow on a realistically messy
dataset.

**The deliberate portfolio role — this is the key framing.** The project exists *on
purpose* to **fill a gap**. The portfolio's other SQL project — the **BigQuery e-commerce
analysis** — is entirely **SELECT-side**: querying, CTEs, window functions, aggregations,
KPIs. That's the *analyze* half of SQL. This project covers the *other* half: **DDL and
DML** — the statements that **create, alter, update, and delete** data. The two projects
are an intentional pair, and together they show the **full spectrum of practical SQL** —
both querying data and transforming it.

**Why it's a good portfolio project.** Cleaning is what analysts actually spend most of
their time on, and doing it *well* — with a staging copy, a quality baseline, defensible
decisions about each issue, and a re-runnable pipeline — is a real skill. It also showcases
the parts of SQL that pure-analytics projects never touch: `ALTER TABLE`, transactions,
views, indexes, stored procedures.

---

## 3. The Tech Stack & Dataset

| | |
|---|---|
| **Database** | **MySQL** (via MySQL Workbench) |
| **Deliverable** | One SQL script — `SQL_housing_data_cleaning_project.sql` |
| **Dataset** | Nashville Housing Data (Kaggle, CC0 public domain, by Timothy James) |
| **Scale** | ~56,636 rows × 29 columns; Nashville property sales, 2013–2016 |

**Why MySQL specifically.** The project deliberately uses MySQL (not BigQuery, where the
e-commerce project lives) — and the write-up calls out **MySQL-specific syntax** that
distinguishes the dialect: `STR_TO_DATE` for date parsing, `TRIM` for whitespace,
`INFORMATION_SCHEMA` queries for metadata inspection, and **prefix-length indexing** for
TEXT columns (more on that in §11). Knowing that SQL has dialects — and which functions are
MySQL-specific — is itself a point worth making in an interview.

**The dataset's key columns:** Parcel ID, Land Use, Property Address, Property City, Sale
Date, Sale Price, Legal Reference, Sold As Vacant, Owner Name/Address/City/State, Acreage,
Land/Building/Total Value, Year Built, Bedrooms, Full Bath, Half Bath.

**One import detail that drives everything downstream:** the CSV was imported with **all
columns as TEXT**. That's a deliberate choice — importing everything as text avoids import
errors from mixed or inconsistent formatting — but it means the *first cleaning job* is
fixing the types that should be something else (notably the sale date).

---

## 4. The raw → staging → clean Workflow

**This three-table discipline is the project's structural backbone. Know it cold.**

```
  CSV import
      │
      ▼
  housing_raw      ← the original imported data — NEVER touched again
      │  CREATE TABLE housing_staging AS SELECT * FROM housing_raw
      ▼
  housing_staging  ← the working copy — ALL cleaning happens here
      │  (5 cleaning steps applied in place)
      ▼
  vw_housing_clean ← a VIEW exposing the cleaned staging table to consumers
```

**The setup:**
1. `CREATE DATABASE nashville_housing;`
2. Import the CSV into `housing_raw` (via MySQL Workbench's import wizard).
3. Verify the row count: `SELECT COUNT(*) FROM housing_raw;` → **56,636 rows**.
4. `CREATE TABLE housing_staging AS SELECT * FROM housing_raw;` — a full copy.

**Why a staging copy — the discipline to explain.** The raw data stays **untouched** in
`housing_raw` as a **safety net**. Every cleaning and transformation operation runs on the
`housing_staging` copy. If a step goes wrong, or you need to re-reference what the original
import actually contained, `housing_raw` is always there. This is the same "preserve the
raw data" principle that good ETL pipelines follow everywhere — *never edit your source in
place.*

---

## 5. Data Quality Assessment

**Before cleaning anything, the project establishes a baseline** — you can't clean what you
haven't measured, and the before/after comparison is what proves the cleaning worked.

**The NULL/blank check** uses **conditional aggregation** — `SUM(CASE WHEN col IS NULL OR
TRIM(col) = '' THEN 1 ELSE 0 END)` for each column in one pass. (The `TRIM(col) = ''` part
matters: because everything imported as TEXT, "missing" values are often *empty strings* or
*whitespace*, which `IS NULL` alone wouldn't catch.)

**The six quality issues found:**

| Issue | Count / detail | Verdict |
|---|---|---|
| Blank Property Address / City | **159** rows | Fixable (partly) via Parcel ID self-join |
| Duplicate rows | **104** | Remove |
| Sale Date stored as TEXT | whole column | Convert to DATE |
| Missing Owner / Acreage / Year Built / Bedrooms | **~30,000–32,000** rows each | **Not fixable** — these are condo entries with no such data |
| Whitespace in text columns | many columns | Trim |
| `Sold As Vacant` consistency | Yes (4,895) / No (51,741) | **Already clean** — no Y/N inconsistency |

**Two mature judgment calls to highlight:**
- The **~30K missing Owner/Acreage/etc.** rows were **deliberately *not* "fixed."** They're
  condo records that genuinely don't have that data, and there's nothing within the dataset
  to fill them from. Inventing values would be worse than leaving honest NULLs. Knowing
  when *not* to clean is a real skill.
- `Sold As Vacant` was *checked* and found **already clean** — only "Yes"/"No", no "Y"/"N"
  mess. The project verified rather than assumed, and reports the non-finding honestly.

---

## 6. Step 1 — Standardize the Date Format

**The problem.** `Sale Date` came in as **TEXT** (from the all-text import). Text dates
can't be compared, can't do date arithmetic, can't be indexed efficiently.

**The fix — add a new typed column, don't overwrite:**
```sql
ALTER TABLE housing_staging ADD COLUMN SaleDateClean DATE;
UPDATE housing_staging SET SaleDateClean = STR_TO_DATE(`Sale Date`, '%Y-%m-%d');
```
`STR_TO_DATE` parses the text string into a real `DATE` using the format mask
`'%Y-%m-%d'`. The original `Sale Date` text column is left in place for now (it's dropped
later in Step 5) — adding a *new* column rather than overwriting in place is the safer
pattern.

**Verification** uses an `INFORMATION_SCHEMA.COLUMNS` query to confirm `Sale Date` is still
`text` and `SaleDateClean` is now `date`.

**Why it matters.** Proper `DATE` typing is what enables date comparisons, date arithmetic
(days between sales), `YEAR`/`MONTH` extraction, and efficient date-range indexing — none of
which work reliably on a TEXT column.

---

## 7. Step 2 — Populate Missing Addresses (Self-Join)

**This is the project's most clever step — know the self-join logic.**

**The problem.** 159 rows had a blank `Property Address`.

**The insight.** A property's **Parcel ID** uniquely identifies the parcel — so **two rows
with the same Parcel ID describe the same property and must share the same address.** If a
row with a given Parcel ID has a blank address but *another* row with that same Parcel ID
has the address filled in, you can copy it across.

**The fix — a self-join `UPDATE`:**
```sql
UPDATE housing_staging a
JOIN housing_staging b
  ON a.`Parcel ID` = b.`Parcel ID`
  AND a.`Property Address` != b.`Property Address`
SET a.`Property Address` = b.`Property Address`
WHERE TRIM(a.`Property Address`) = '';
```
The table is joined **to itself** — alias `a` is the row with the blank, alias `b` is a
different row sharing the Parcel ID that *has* an address. The `UPDATE` copies `b`'s
address into `a`.

**The result — and the honest accounting.** Only **16 of the 159** rows were fixed; **143
remain blank.** Why only 16? Those 16 were the only blank-address rows whose Parcel ID
*also appeared elsewhere* with a valid address. The other 143 had Parcel IDs that didn't
recur — there was simply nothing within the dataset to pull from. The project states this
plainly and notes that in production these would need external data, geocoding, or manual
research.

**The teachable point.** A **self-join** — joining a table to itself — is the right tool
when rows in the *same* table can fill each other's gaps. And the honest "16 of 159, here's
why the rest can't be fixed from within the data" is exactly the kind of candid limitation
that signals analytical maturity.

---

## 8. Step 3 — Clean Text Fields (Whitespace)

**The problem.** Leading/trailing whitespace in text columns — invisible, but it breaks
`GROUP BY`, joins, and filters ("Nashville" and "Nashville " become two different values).

**The fix — one `UPDATE` that `TRIM`s 10 text columns at once:** Property Address, Property
City, Owner Name, Address, City, State, Land Use, Grade, Exterior Wall, Foundation Type.

**The result: 24,172 rows changed — nearly half the dataset.** That's the striking number:
whitespace issues are pervasive and silent. Without this step, almost half the table would
have subtle inconsistencies that corrupt every later grouping or join.

**The teachable point.** Whitespace is the classic "invisible" data-quality problem — it
doesn't show up in a casual look at the data, but it quietly produces duplicate categories
and failed joins. `TRIM` is cheap; skipping it is expensive.

---

## 9. Step 4 — Remove Duplicate Rows

**The problem.** 104 fully-duplicate rows (same Parcel ID, Property Address, Sale Price,
Sale Date, and Legal Reference — i.e., the same sale recorded twice).

**The technique — `ROW_NUMBER()` to *flag* duplicates:**
```sql
ROW_NUMBER() OVER (
  PARTITION BY `Parcel ID`, `Property Address`, `Sale Price`, `Sale Date`, `Legal Reference`
  ORDER BY row_id
) AS row_num
```
`ROW_NUMBER()` numbers rows *within each group* of identical records. The **first**
occurrence of any sale gets `row_num = 1`; every *duplicate* gets `row_num > 1`. So
"`WHERE row_num > 1`" precisely isolates the rows to delete while keeping one copy of each.

**The MySQL-specific workaround — and the detail to know.** **MySQL cannot `DELETE`
directly from a CTE.** So the project does it in three moves:
1. `ALTER TABLE ... ADD COLUMN row_id INT AUTO_INCREMENT PRIMARY KEY` — give every row a
   unique handle.
2. `CREATE TEMPORARY TABLE temp_duplicates AS SELECT row_id ... WHERE row_num > 1` — capture
   the IDs of the duplicate rows.
3. `DELETE FROM housing_staging WHERE row_id IN (SELECT row_id FROM temp_duplicates)`.

**The result: 104 rows deleted → 56,636 becomes 56,532.**

**The teachable point.** `ROW_NUMBER() OVER (PARTITION BY ...)` is *the* standard SQL idiom
for de-duplication — partition by the columns that define a duplicate, keep `row_num = 1`,
delete the rest. And being able to explain *why* the temp-table workaround was needed
(MySQL's restriction on deleting from a CTE) is a strong dialect-awareness signal.

---

## 10. Step 5 — Drop Unused Columns

**The fix — one `ALTER TABLE` dropping 4 columns:**
- `Sale Date` — the original TEXT column, now **replaced by `SaleDateClean`**.
- `Tax District` — not useful for analysis.
- `image` — not useful for analysis.
- `row_id` — the auto-increment key that **was only needed for the deduplication step** in
  Step 4; its job is done.

**The teachable point.** Cleaning isn't only *adding* — it's also *removing*. Dropping the
superseded text date, the analysis-irrelevant columns, and the now-unneeded scaffolding
column (`row_id`) leaves a leaner, clearer table. Note the lifecycle of `row_id`: created
in Step 4 purely as a deduplication handle, dropped in Step 5 once that job is finished.

---

## 11. Final Output — View & Indexes

**The clean VIEW.** `CREATE VIEW vw_housing_clean AS SELECT ...` exposes the cleaned
staging table with **tidy column aliases** — e.g., `SaleDateClean AS SaleDate`, `Address AS
OwnerAddress`, `City AS OwnerCity`, `State AS OwnerState` (disambiguating the *owner's*
address from the *property's*). A view is a saved query that downstream consumers select
from as if it were a table — they get the clean, well-named result without seeing the
messy staging internals.

**The performance indexes.** Three indexes on the columns most likely to be filtered or
joined:
- `idx_parcel_id` on `Parcel ID` — record lookups.
- `idx_sale_date` on `SaleDateClean` — date-range queries.
- `idx_property_city` on `Property City(100)` — geographic filtering. **Note the `(100)`** —
  that's a **prefix-length index** (MySQL-specific): you can't index a full TEXT column
  directly, so you index the first 100 characters. Knowing that detail is a dialect signal.

**What an index does** — it builds an optimized lookup structure so MySQL can find matching
rows *without scanning the whole table*.

**The validation summary — the before/after proof:**

| Metric | Before (Raw) | After (Clean) |
|---|---|---|
| Total rows | 56,636 | **56,532** |
| Duplicate rows | 104 | **0** |
| Blank Property Addresses | 159 | **143** |
| Sale Date data type | TEXT | **DATE** |
| Columns dropped | — | **4** |
| Rows with whitespace cleaned | 24,172 | **0** |

---

## 12. Stretch Goals — EXPLAIN, Transactions, Stored Procedure

Three "stretch" features that go beyond basic cleaning:

**`EXPLAIN` — verifying the indexes work.** Running `EXPLAIN` on a filtered query shows the
optimizer's plan. The key results: **`type: ref`** (MySQL is using an index, not a full
table scan), **`key: idx_property_city`** (confirms the city index is being used), and
**`rows: ~28,488`** (it estimates scanning ~half the table instead of all 56,532). `EXPLAIN`
is how you *prove* an index is helping rather than just hoping.

**Transaction control — `BEGIN` / `COMMIT` / `ROLLBACK`.** This pattern wraps destructive
operations (like the dedup `DELETE`) in a safety net: between `BEGIN` and `COMMIT` nothing
is permanently saved, so if something looks wrong you `ROLLBACK` and undo it. It's
especially important for `DELETE`, which is otherwise hard to recover from. The project
documents the pattern as how the deduplication `DELETE` *should* be wrapped.

**Stored procedure — `clean_housing_data()`.** The entire five-step pipeline (date
conversion, address population, whitespace trimming, deduplication, column drops) was
wrapped into a **stored procedure** so it can be re-run on fresh data with a single
command: `CALL clean_housing_data();`. This turns a one-off cleaning script into a
**reusable, automatable routine** — the difference between cleaning data once and building
a cleaning *tool*.

---

## 13. SQL Concepts to Know Cold

**DDL vs. DML — the most important distinction for this project.**
- **DDL (Data Definition Language)** — statements that define *structure*: `CREATE`,
  `ALTER`, `DROP`. They change the *schema* (tables, columns, views, indexes).
- **DML (Data Manipulation Language)** — statements that change *data inside* tables:
  `INSERT`, `UPDATE`, `DELETE`, `SELECT`.
This project is a tour of both — the e-commerce project was almost pure `SELECT` (DML query
side); this one is heavy on DDL and the modifying DML.

**`CREATE TABLE ... AS SELECT`** — creates a new table populated from a query; used to make
the staging copy.

**`ALTER TABLE`** — modifies an existing table's structure: `ADD COLUMN`, `MODIFY COLUMN`,
`DROP COLUMN`.

**`UPDATE ... SET`** — changes values in existing rows.

**`UPDATE ... JOIN` (self-join update)** — updates a table using values from a join,
including a join *to itself*; used to fill blank addresses.

**`DELETE`** — removes rows.

**Staging table pattern** — copy the raw import to a working table; clean the copy; keep
the raw untouched as a safety net.

**`STR_TO_DATE(text, format)`** — MySQL function that parses a text string into a `DATE`
using a format mask.

**`TRIM`** — removes leading/trailing whitespace from a string.

**`ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)`** — a window function that numbers
rows within each partition; the standard de-duplication idiom (keep `row_num = 1`).

**Window function** — a function computed over a set of related rows without collapsing
them (`ROW_NUMBER` here).

**CTE (Common Table Expression)** — a named temporary result set defined with `WITH`.

**`CASE` statement** — conditional logic; used inside `SUM` for the null/blank counts.

**`INFORMATION_SCHEMA`** — built-in metadata tables; querying them tells you about your
tables and columns (used to verify the date-type conversion).

**`VIEW`** — a saved query that behaves like a virtual table.

**Index** — an optimized lookup structure that speeds up filters and joins by avoiding full
table scans. A **prefix-length index** (`col(100)`) indexes only the first N characters —
MySQL requires this for TEXT columns.

**`EXPLAIN`** — shows the query optimizer's execution plan; used to confirm indexes are
being used.

**Transaction (`BEGIN`/`COMMIT`/`ROLLBACK`)** — a unit of work that can be committed
(saved) or rolled back (undone) as a whole.

**Stored procedure** — a saved, named, callable block of SQL; run with `CALL`.

---

## 14. Limitations & Honest Caveats

Volunteer these — the project itself is candid about most of them.

1. **143 of 159 blank addresses remain unfixed.** Only the 16 with a recurring Parcel ID
   could be filled from within the data; the rest genuinely have no source. Honest NULLs
   beat invented values — but it *is* a limitation, and production would need external
   data, geocoding, or manual research.
2. **~30,000+ rows are missing Owner / Acreage / Year Built / Bedrooms** and were
   deliberately left as-is — they're condo records with no such data in the source. The
   project doesn't pretend to fix what can't be fixed.
3. **The dataset is a fixed Kaggle snapshot** (2013–2016 Nashville sales) — the cleaning
   *methodology* is the transferable skill, not these specific records.
4. **Some steps depend on MySQL Workbench's GUI** — the CSV import wizard and the stored
   procedure's routine editor were used through the GUI rather than pure script, so the
   `.sql` file isn't a 100% standalone reproducible artifact end to end.
5. **The transaction wrapping is documented, not applied in the committed script** — the
   `BEGIN`/`COMMIT`/`ROLLBACK` pattern is shown as commented guidance for how the `DELETE`
   *should* be wrapped, rather than executed that way in the script.
6. **No downstream analysis.** This project's scope ends at a clean, indexed dataset — it
   produces the *input* to analysis, not the analysis itself. (That's by design — the
   analysis half is the e-commerce project.)

---

## 15. Interview Q&A

Practice these out loud.

**Q1. Give me the overview of this project.**
"It's an end-to-end SQL data-cleaning project in MySQL on the Nashville Housing dataset —
about 56,000 property-sale records. I created a database, imported the raw CSV, made a
staging copy to protect the original, assessed the data quality, then cleaned it in five
steps: convert the sale date from text to a real DATE, fill blank addresses with a
self-join, trim whitespace, remove duplicates with ROW_NUMBER, and drop unused columns. I
finished with a clean view, performance indexes, and a stored procedure that re-runs the
whole pipeline. The project exists to show the DDL/DML side of SQL — the transform half."

**Q2. What's the difference between DDL and DML, and why does that matter here?**
"DDL is Data Definition Language — CREATE, ALTER, DROP — it changes the structure, the
schema. DML is Data Manipulation Language — INSERT, UPDATE, DELETE, SELECT — it changes the
data inside tables. It matters because my two SQL projects deliberately split the
spectrum: my e-commerce analysis project is almost pure SELECT, the query side; this
project is heavy on DDL and the modifying DML. Together they cover both halves of
practical SQL."

**Q3. Why did you create a staging table instead of cleaning the raw import directly?**
"As a safety net. The raw import stays untouched in a table called housing_raw, and all my
cleaning happens on a copy, housing_staging. If a cleaning step goes wrong, or I need to
re-check what the original actually contained, the raw data is always there. It's the same
principle as never editing your source data in place — you preserve the original and
transform a copy."

**Q4. Walk me through how you filled the missing addresses.**
"159 rows had a blank Property Address. The insight is that Parcel ID uniquely identifies a
property — so two rows with the same Parcel ID must have the same address. I used a
self-join: I joined the staging table to itself, matched on Parcel ID, with alias 'a' being
the row with the blank address and alias 'b' being a different row that had the address
filled in, and copied b's address into a. It fixed 16 of the 159. Only 16, because those
were the only blank rows whose Parcel ID also appeared elsewhere with a valid address —
the other 143 had unique Parcel IDs, so there was nothing within the data to pull from."

**Q5. How did you remove the duplicates?**
"I used ROW_NUMBER with PARTITION BY. I partitioned by the columns that define a duplicate
— Parcel ID, Property Address, Sale Price, Sale Date, Legal Reference — so ROW_NUMBER
numbers the rows within each group of identical sales. The first copy gets row number 1,
every duplicate gets a number above 1. One detail: MySQL won't let you DELETE directly from
a CTE, so I added an auto-increment row_id, captured the duplicate row_ids into a temporary
table, and deleted where row_id was in that temp table. It removed 104 rows."

**Q6. The whitespace step changed 24,000 rows — why does whitespace matter so much?**
"Whitespace is invisible but it breaks things silently. 'Nashville' and 'Nashville ' with a
trailing space are two different values to SQL — they'd show up as separate groups in a
GROUP BY, and they'd fail to match in a join. Almost half my dataset, over 24,000 rows, had
leading or trailing spaces. If I'd skipped TRIM, every later grouping or join on those text
columns would have been subtly wrong."

**Q7. What's a stored procedure and why did you build one?**
"A stored procedure is a saved, named block of SQL you can run with a single CALL command.
I wrapped all five cleaning steps into one procedure called clean_housing_data. The reason
is reusability — if fresh data comes in, instead of re-running a long script step by step,
you just CALL clean_housing_data and the whole pipeline runs. It turns a one-off cleaning
script into a re-runnable tool."

**Q8. What do indexes do, and how did you confirm they work?**
"An index is an optimized lookup structure that lets MySQL find matching rows without
scanning the whole table. I added three — on Parcel ID for lookups, on the clean sale date
for date-range queries, and on Property City for geographic filtering. To confirm they're
actually used, I ran EXPLAIN on a filtered query — the output showed type 'ref', meaning
it's using an index, and named idx_property_city as the key, and estimated scanning about
half the table instead of all of it."

**Q9. You left 30,000 rows with missing data unfixed — why?**
"Because they couldn't be honestly fixed. Those rows are condo entries that genuinely don't
have Owner, Acreage, Year Built, or Bedrooms data, and there's nothing within the dataset
to fill them from. Inventing values would be worse than leaving honest NULLs — it would
fabricate data. Knowing when not to clean is part of cleaning. In a real setting you'd go
to an external source for that data."

**Q10. What would you do differently or add?**
"I'd make the pipeline fully script-reproducible — right now the CSV import and the stored
procedure creation went through MySQL Workbench's GUI. I'd actually wrap the destructive
DELETE in a BEGIN/COMMIT transaction in the script, not just document the pattern. And for
the 143 still-blank addresses, I'd integrate an external geocoding or parcel-records lookup
to resolve them."

---

## 16. How to Walk Through This Project Live

If asked to screen-share the SQL script:

1. **State the purpose first** — "this is the DDL/DML, *transform* half of SQL, the
   companion to my e-commerce analytics project."
2. **Show the raw → staging → clean workflow** — explain *why* the staging copy exists
   (safety net, never touch the source).
3. **Show the quality assessment** — the conditional-aggregation null check, and the six
   issues found. Make the "all columns imported as TEXT" point.
4. **Walk the five cleaning steps** — date conversion (STR_TO_DATE), the **self-join
   address fill** (spend time here — it's the cleverest step), the whitespace TRIM (the
   24,000-row number), the **ROW_NUMBER dedup** (spend time here too, and explain the MySQL
   temp-table workaround), and the column drops.
5. **Show the final output** — the clean VIEW and the indexes, including the prefix-length
   index detail.
6. **Mention the stretch goals** — EXPLAIN proving the indexes work, transaction safety,
   and the re-runnable stored procedure.
7. **Close on the before/after validation table** — duplicates 104 → 0, date TEXT → DATE,
   etc. End on the proof that the cleaning worked.

**Pacing tip:** spend the most time on the **self-join address fill** and the
**ROW_NUMBER deduplication** — those are the two cleverest, most technical steps. And lead
with the DDL-vs-DML framing so the interviewer understands *why* this project exists
alongside the e-commerce one.

---

## 17. Glossary

- **MySQL** — the relational database this project uses.
- **DDL (Data Definition Language)** — statements that define structure: `CREATE`,
  `ALTER`, `DROP`.
- **DML (Data Manipulation Language)** — statements that manipulate data: `INSERT`,
  `UPDATE`, `DELETE`, `SELECT`.
- **Staging table** — a working copy of the raw data; cleaning happens here, the raw is
  preserved.
- **`CREATE TABLE ... AS SELECT`** — create a new table populated from a query.
- **`ALTER TABLE`** — modify a table's structure (`ADD`/`MODIFY`/`DROP COLUMN`).
- **`UPDATE ... SET`** — change values in existing rows.
- **Self-join** — joining a table to itself; used so rows can fill each other's gaps.
- **`UPDATE ... JOIN`** — an update whose new values come from a join.
- **`DELETE`** — remove rows from a table.
- **`STR_TO_DATE`** — MySQL function parsing text into a `DATE` via a format mask.
- **`TRIM`** — removes leading/trailing whitespace.
- **`ROW_NUMBER() OVER (PARTITION BY ...)`** — a window function numbering rows within
  groups; the standard de-duplication idiom.
- **Window function** — a function over related rows that doesn't collapse them.
- **CTE** — a named temporary result set defined with `WITH`.
- **Temporary table** — a short-lived table; used here because MySQL can't `DELETE` from a
  CTE.
- **`CASE` statement** — in-query conditional logic.
- **`INFORMATION_SCHEMA`** — built-in metadata tables describing the database's own
  structure.
- **`VIEW`** — a saved query that acts as a virtual table.
- **Index** — an optimized lookup structure that avoids full table scans.
- **Prefix-length index** — `index(col(N))` — indexing the first N characters; MySQL
  requires it for TEXT columns.
- **`EXPLAIN`** — shows the query optimizer's execution plan.
- **Transaction** — `BEGIN`/`COMMIT`/`ROLLBACK`; a unit of work saved or undone as a whole.
- **Stored procedure** — a saved, callable block of SQL; run with `CALL`.
- **Conditional aggregation** — `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`; used for the
  null/blank counts.
- **Parcel ID** — the unique identifier of a property parcel; the key for the self-join.

---

*This study guide documents the project as built. The authoritative references are the SQL
script `sql-code/SQL_housing_data_cleaning_project.sql` and the portfolio page `index.md`.
When this guide and the script disagree, the script wins.*