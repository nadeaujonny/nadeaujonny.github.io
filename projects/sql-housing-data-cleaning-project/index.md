---
layout: default
title: Nashville Housing Data Cleaning & Transformation (MySQL)
description: "End-to-end SQL data cleaning project using MySQL — demonstrating DDL, DML, string functions, type conversions, and transformation techniques on 56,000+ Nashville property records."
---

<a href="/projects/" class="back-to-projects btn">← Back to Projects</a>

# Nashville Housing Data Cleaning & Transformation (MySQL)

> This project demonstrates the DDL/DML side of SQL by cleaning and transforming 56,000+ Nashville housing records in MySQL — covering database creation, staging table patterns, data type conversions, self-join updates, deduplication, whitespace cleaning, views, indexes, and stored procedures.

<p><span style="display:inline-block; background:#00758f; color:#fff; padding:4px 12px; border-radius:4px; font-size:0.85em; font-weight:600;">MySQL</span></p>

---

<details>
  <summary><strong>Project Overview</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Overview</h3>
  <p>
    This is an end-to-end SQL data cleaning project built in MySQL using the Nashville Housing dataset from Kaggle
    (~56,636 rows, 29 columns). The project walks through creating a database, importing raw CSV data, building a
    staging copy, identifying quality issues, and systematically cleaning the data using core SQL DDL and DML operations.
  </p>

  <h3>Business Context</h3>
  <p>
    Data cleaning is a foundational skill in any analytics role — real-world datasets rarely arrive analysis-ready.
    This project exists in the portfolio to fill the DDL/DML gap left by the
    <a href="/projects/sql-ecommerce-analysis/">BigQuery e-commerce analysis project</a>, which focuses on
    SELECT-side analytics (CTEs, window functions, joins, aggregations). Together, the two SQL projects cover
    the full spectrum of practical SQL skills: querying <em>and</em> transforming data.
  </p>

  <h3>Objectives</h3>
  <ul>
    <li>Demonstrate CREATE DATABASE, CREATE TABLE, ALTER TABLE, UPDATE, DELETE operations</li>
    <li>Apply string functions (TRIM, STR_TO_DATE) and type conversions</li>
    <li>Use self-joins to populate missing data from related rows</li>
    <li>Identify and remove duplicate rows using ROW_NUMBER() and temporary tables</li>
    <li>Build reusable views, performance indexes, and stored procedures</li>
  </ul>

  <h3>Dataset Overview</h3>
  <p>
    <strong>Nashville Housing Data</strong> from Kaggle (CC0 Public Domain), published by Timothy James.
    ~56,636 rows of Nashville property sale records from 2013–2016.
  </p>

  <h4>Key Columns</h4>
  <ul>
    <li>Parcel ID, Land Use, Property Address, Property City</li>
    <li>Sale Date, Sale Price, Legal Reference, Sold As Vacant</li>
    <li>Owner Name, Address, City, State</li>
    <li>Acreage, Land Value, Building Value, Total Value</li>
    <li>Year Built, Bedrooms, Full Bath, Half Bath</li>
  </ul>

  <h3>SQL Techniques Demonstrated</h3>
  <ul>
    <li>CREATE DATABASE, CREATE TABLE</li>
    <li>ALTER TABLE (ADD COLUMN, MODIFY COLUMN, DROP COLUMN)</li>
    <li>UPDATE...SET, UPDATE...JOIN (self-join)</li>
    <li>DELETE</li>
    <li>CREATE VIEW, CREATE INDEX, CREATE PROCEDURE</li>
    <li>STR_TO_DATE, TRIM</li>
    <li>ROW_NUMBER() OVER (PARTITION BY)</li>
    <li>CTE, CASE statements</li>
    <li>INFORMATION_SCHEMA queries</li>
    <li>EXPLAIN (query performance analysis)</li>
    <li>Staging table pattern (raw → staging → clean workflow)</li>
  </ul>

  <p style="margin-top: 10px;">
    <a href="sql-code/SQL_housing_data_cleaning_project.sql">View full SQL script</a>
  </p>

</details>
<details>
  <summary><strong>Setup &amp; Data Loading</strong></summary>

  <div style="margin-top: 12px;"></div>

  <p>
    Created the <code>nashville_housing</code> database, imported the CSV via MySQL Workbench's Table Data Import
    Wizard, and created a staging copy to preserve the raw data. All columns were imported as TEXT to avoid
    import errors from mixed or inconsistent formatting.
  </p>

  <h3>Create Database</h3>
  <pre><code class="language-sql">CREATE DATABASE nashville_housing;
USE nashville_housing;</code></pre>

  <h3>Import CSV</h3>
  <pre><code class="language-sql">-- import csv via import wizard</code></pre>

  <h3>Verify Row Count</h3>
  <pre><code class="language-sql">SELECT COUNT(*) FROM housing_raw;
-- Result: 56,636 rows</code></pre>

  <h3>Create Staging Copy</h3>
  <pre><code class="language-sql">CREATE TABLE housing_staging AS
SELECT * FROM housing_raw;</code></pre>

  <p>
    <strong>Why a staging table?</strong> The raw data stays untouched in <code>housing_raw</code> as a safety net.
    All cleaning and transformation happens on the <code>housing_staging</code> copy, so the original import can
    always be referenced or re-used if needed.
  </p>

</details>
<details>
  <summary><strong>Data Exploration &amp; Quality Assessment</strong></summary>

  <div style="margin-top: 12px;"></div>

  <p>
    Before cleaning, I explored the data to establish a baseline and identify quality issues that needed to be addressed.
  </p>

  <h3>NULL &amp; Blank Value Counts</h3>
  <pre><code class="language-sql">SELECT
    SUM(CASE WHEN `Parcel ID` IS NULL OR TRIM(`Parcel ID`) = '' THEN 1 ELSE 0 END) AS ParcelID_nulls,
    SUM(CASE WHEN `Land Use` IS NULL OR TRIM(`Land Use`) = '' THEN 1 ELSE 0 END) AS LandUse_nulls,
    SUM(CASE WHEN `Property Address` IS NULL OR TRIM(`Property Address`) = '' THEN 1 ELSE 0 END) AS PropertyAddress_nulls,
    SUM(CASE WHEN `Property City` IS NULL OR TRIM(`Property City`) = '' THEN 1 ELSE 0 END) AS PropertyCity_nulls,
    SUM(CASE WHEN `Sale Date` IS NULL OR TRIM(`Sale Date`) = '' THEN 1 ELSE 0 END) AS SaleDate_nulls,
    SUM(CASE WHEN `Sale Price` IS NULL OR TRIM(`Sale Price`) = '' THEN 1 ELSE 0 END) AS SalePrice_nulls,
    SUM(CASE WHEN `Sold As Vacant` IS NULL OR TRIM(`Sold As Vacant`) = '' THEN 1 ELSE 0 END) AS SoldAsVacant_nulls,
    SUM(CASE WHEN `Owner Name` IS NULL OR TRIM(`Owner Name`) = '' THEN 1 ELSE 0 END) AS OwnerName_nulls,
    SUM(CASE WHEN `Address` IS NULL OR TRIM(`Address`) = '' THEN 1 ELSE 0 END) AS OwnerAddress_nulls,
    SUM(CASE WHEN `Acreage` IS NULL OR TRIM(`Acreage`) = '' THEN 1 ELSE 0 END) AS Acreage_nulls,
    SUM(CASE WHEN `Year Built` IS NULL OR TRIM(`Year Built`) = '' THEN 1 ELSE 0 END) AS YearBuilt_nulls,
    SUM(CASE WHEN `Bedrooms` IS NULL OR TRIM(`Bedrooms`) = '' THEN 1 ELSE 0 END) AS Bedrooms_nulls
FROM housing_staging;</code></pre>

  <h4>Results</h4>
  <table>
    <thead>
      <tr>
        <th>Column</th>
        <th>Blank / NULL Count</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Parcel ID</td><td>0</td></tr>
      <tr><td>Land Use</td><td>0</td></tr>
      <tr><td>Property Address</td><td>159</td></tr>
      <tr><td>Property City</td><td>159</td></tr>
      <tr><td>Sale Date</td><td>0</td></tr>
      <tr><td>Sale Price</td><td>0</td></tr>
      <tr><td>Sold As Vacant</td><td>0</td></tr>
      <tr><td>Owner Name</td><td>31,375</td></tr>
      <tr><td>Owner Address</td><td>30,619</td></tr>
      <tr><td>Acreage</td><td>30,619</td></tr>
      <tr><td>Year Built</td><td>32,471</td></tr>
      <tr><td>Bedrooms</td><td>32,477</td></tr>
    </tbody>
  </table>

  <h3>Sold As Vacant Distribution</h3>
  <pre><code class="language-sql">SELECT `Sold As Vacant`, COUNT(*) AS count
FROM housing_staging
GROUP BY `Sold As Vacant`
ORDER BY count;
-- Result: Yes (4,895) and No (51,741) — already clean, no Y/N inconsistency</code></pre>

  <h3>Duplicate Count</h3>
  <pre><code class="language-sql">SELECT COUNT(*) AS duplicate_count
FROM (
    SELECT `Parcel ID`, `Property Address`, `Sale Price`, `Sale Date`, `Legal Reference`,
        ROW_NUMBER() OVER (
            PARTITION BY `Parcel ID`, `Property Address`, `Sale Price`, `Sale Date`, `Legal Reference`
            ORDER BY `Parcel ID`
        ) AS row_num
    FROM housing_staging
) duplicates
WHERE row_num > 1;
-- Result: 104 duplicate rows</code></pre>

  <h3>Summary of Data Quality Issues</h3>
  <ul>
    <li><strong>159 blank Property Addresses</strong> — fixable via Parcel ID self-join</li>
    <li><strong>104 duplicate rows</strong> — to be removed</li>
    <li><strong>Sold As Vacant already clean</strong> — only Yes/No values, no Y/N inconsistency</li>
    <li><strong>Sale Date stored as TEXT</strong> — needs DATE type conversion</li>
    <li><strong>~30,000–32,000 rows missing Owner/Acreage/YearBuilt/Bedrooms</strong> — these are condo entries and are not fixable from within the dataset</li>
    <li><strong>Whitespace issues</strong> — leading/trailing spaces in multiple text columns</li>
  </ul>

</details>
<details>
  <summary><strong>Step 1 — Standardize Date Format</strong></summary>

  <div style="margin-top: 12px;"></div>

  <p>
    The <code>Sale Date</code> column was stored as TEXT after the CSV import. I added a new DATE column and
    converted the values using <code>STR_TO_DATE</code>.
  </p>

  <h3>Convert Sale Date to DATE Type</h3>
  <pre><code class="language-sql">ALTER TABLE housing_staging
ADD COLUMN SaleDateClean DATE;

UPDATE housing_staging
SET SaleDateClean = STR_TO_DATE(`Sale Date`, '%Y-%m-%d');</code></pre>

  <h3>Verify Data Types</h3>
  <pre><code class="language-sql">SELECT
    COLUMN_NAME,
    DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'nashville_housing'
    AND TABLE_NAME = 'housing_staging'
    AND COLUMN_NAME IN ('Sale Date', 'SaleDateClean');
-- Result: Sale Date = text, SaleDateClean = date</code></pre>

  <p>
    <strong>Why does DATE type matter?</strong> Proper DATE typing enables date comparisons, date arithmetic
    (e.g., calculating days between sales), YEAR/MONTH extraction, and efficient indexing — none of which work
    reliably on TEXT columns.
  </p>

</details>
<details>
  <summary><strong>Step 2 — Populate Missing Property Addresses</strong></summary>

  <div style="margin-top: 12px;"></div>

  <p>
    159 rows had blank Property Addresses. Since rows with the same Parcel ID share the same address, I used a
    self-join to populate blanks from matching rows that already had an address.
  </p>

  <h3>Preview: Blank Addresses with Matching Parcel IDs</h3>
  <pre><code class="language-sql">SELECT a.`Parcel ID`, a.`Property Address`, b.`Property Address`
FROM housing_staging a
JOIN housing_staging b
    ON a.`Parcel ID` = b.`Parcel ID`
    AND a.`Property Address` != b.`Property Address`
WHERE TRIM(a.`Property Address`) = ''
LIMIT 10;</code></pre>

  <h3>Update Blank Addresses via Self-Join</h3>
  <pre><code class="language-sql">UPDATE housing_staging a
JOIN housing_staging b
    ON a.`Parcel ID` = b.`Parcel ID`
    AND a.`Property Address` != b.`Property Address`
SET a.`Property Address` = b.`Property Address`
WHERE TRIM(a.`Property Address`) = '';
-- Result: 16 rows updated</code></pre>

  <h3>Verify Remaining Blanks</h3>
  <pre><code class="language-sql">SELECT
    SUM(CASE WHEN TRIM(`Property Address`) = '' OR `Property Address` IS NULL THEN 1 ELSE 0 END) AS remaining_blank_addresses
FROM housing_staging;
-- Result: 143 remaining (159 - 16 = 143)</code></pre>

  <p>
    Only 16 rows were fixed because those were the only blank-address rows whose Parcel ID matched another row
    with a populated address. The remaining 143 rows had Parcel IDs that did not appear elsewhere in the dataset
    with a valid address — so there was nothing to pull from. In a production setting, these could be resolved
    through external data sources, geocoding lookups, or manual research.
  </p>

</details>
<details>
  <summary><strong>Step 3 — Clean Text Fields</strong></summary>

  <div style="margin-top: 12px;"></div>

  <p>
    Trimmed leading and trailing whitespace from all key text columns using <code>TRIM</code>.
  </p>

  <pre><code class="language-sql">UPDATE housing_staging
SET
    `Property Address` = TRIM(`Property Address`),
    `Property City` = TRIM(`Property City`),
    `Owner Name` = TRIM(`Owner Name`),
    `Address` = TRIM(`Address`),
    `City` = TRIM(`City`),
    `State` = TRIM(`State`),
    `Land Use` = TRIM(`Land Use`),
    Grade = TRIM(Grade),
    `Exterior Wall` = TRIM(`Exterior Wall`),
    `Foundation Type` = TRIM(`Foundation Type`);
-- Result: 24,172 rows changed — nearly half the dataset had whitespace issues</code></pre>

</details>
<details>
  <summary><strong>Step 4 — Remove Duplicate Rows</strong></summary>

  <div style="margin-top: 12px;"></div>

  <p>
    Used <code>ROW_NUMBER()</code> with <code>PARTITION BY</code> to identify duplicates, created a temporary
    table of duplicate row IDs, then deleted them. MySQL doesn't support <code>DELETE</code> directly from a CTE,
    so the temporary table approach was used as a workaround.
  </p>

  <h3>Add Unique Row ID</h3>
  <pre><code class="language-sql">ALTER TABLE housing_staging
ADD COLUMN row_id INT AUTO_INCREMENT PRIMARY KEY;</code></pre>

  <h3>Create Temp Table of Duplicate Row IDs</h3>
  <pre><code class="language-sql">CREATE TEMPORARY TABLE temp_duplicates AS
SELECT row_id
FROM (
    SELECT row_id,
        ROW_NUMBER() OVER (
            PARTITION BY `Parcel ID`, `Property Address`, `Sale Price`, `Sale Date`, `Legal Reference`
            ORDER BY row_id
        ) AS row_num
    FROM housing_staging
) ranked
WHERE row_num > 1;</code></pre>

  <h3>Verify &amp; Delete</h3>
  <pre><code class="language-sql">SELECT COUNT(*) AS duplicates_to_delete FROM temp_duplicates;
-- Result: 104

DELETE FROM housing_staging
WHERE row_id IN (SELECT row_id FROM temp_duplicates);

SELECT COUNT(*) AS rows_after_dedup FROM housing_staging;
-- Result: 56,532 (56,636 - 104 = 56,532)</code></pre>

</details>
<details>
  <summary><strong>Step 5 — Drop Unused Columns</strong></summary>

  <div style="margin-top: 12px;"></div>

  <p>
    Removed columns that were redundant or not useful for analysis.
  </p>

  <pre><code class="language-sql">ALTER TABLE housing_staging
DROP COLUMN `Sale Date`,    -- replaced by SaleDateClean
DROP COLUMN `Tax District`, -- not useful for analysis
DROP COLUMN image,          -- not useful for analysis
DROP COLUMN row_id;         -- only needed for deduplication</code></pre>

</details>
<details>
  <summary><strong>Final Output — View &amp; Indexes</strong></summary>

  <div style="margin-top: 12px;"></div>

  <p>
    Created a reusable VIEW with clean column aliases for downstream consumption, and added indexes on commonly
    queried columns to improve query performance.
  </p>

  <h3>Create Clean View</h3>
  <pre><code class="language-sql">CREATE VIEW vw_housing_clean AS
SELECT
    `Parcel ID`,
    `Land Use`,
    `Property Address`,
    `Property City`,
    SaleDateClean AS SaleDate,
    `Sale Price`,
    `Legal Reference`,
    `Sold As Vacant`,
    `Multiple Parcels Involved in Sale`,
    `Owner Name`,
    `Address` AS OwnerAddress,
    `City` AS OwnerCity,
    `State` AS OwnerState,
    Acreage,
    `Land Value`,
    `Building Value`,
    `Total Value`,
    `Year Built`,
    Bedrooms,
    `Full Bath`,
    `Half Bath`
FROM housing_staging;</code></pre>

  <h3>Add Performance Indexes</h3>
  <pre><code class="language-sql">CREATE INDEX idx_parcel_id ON housing_staging(`Parcel ID`);
CREATE INDEX idx_sale_date ON housing_staging(SaleDateClean);
CREATE INDEX idx_property_city ON housing_staging(`Property City`(100));</code></pre>

  <p>
    <strong>What do indexes do?</strong> Indexes create optimized lookup structures that let MySQL find matching
    rows without scanning the entire table. These three columns were chosen because they are the most likely
    filter and join targets: <code>Parcel ID</code> for record lookups, <code>SaleDateClean</code> for date-range
    queries, and <code>Property City</code> for geographic filtering.
  </p>

</details>
<details>
  <summary><strong>Validation Summary</strong></summary>

  <div style="margin-top: 12px;"></div>

  <p>
    Before-and-after comparison showing every improvement made during the cleaning process:
  </p>

  <table>
    <thead>
      <tr>
        <th>Metric</th>
        <th>Before (Raw)</th>
        <th>After (Clean)</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Total Rows</td><td>56,636</td><td>56,532</td></tr>
      <tr><td>Duplicate Rows</td><td>104</td><td>0</td></tr>
      <tr><td>Blank Property Addresses</td><td>159</td><td>143</td></tr>
      <tr><td>Sale Date Data Type</td><td>TEXT</td><td>DATE</td></tr>
      <tr><td>Columns Dropped</td><td>—</td><td>4</td></tr>
      <tr><td>Rows with Whitespace Cleaned</td><td>24,172</td><td>0</td></tr>
    </tbody>
  </table>

</details>
<details>
  <summary><strong>Stretch Goals</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>EXPLAIN (Query Performance)</h3>
  <p>
    Used <code>EXPLAIN</code> to verify that the indexes are being used by the query optimizer:
  </p>

  <pre><code class="language-sql">EXPLAIN SELECT *
FROM housing_staging
WHERE `Property City` = 'NASHVILLE'
AND SaleDateClean BETWEEN '2014-01-01' AND '2014-12-31';</code></pre>

  <p>
    Key results from the EXPLAIN output:
  </p>
  <ul>
    <li><strong>type: ref</strong> — MySQL is using an index to find matching rows (not scanning the full table)</li>
    <li><strong>key: idx_property_city</strong> — confirms the Property City index is being used</li>
    <li><strong>rows: ~28,488</strong> — roughly half the table is scanned instead of all 56,532 rows</li>
  </ul>

  <h3>Transaction Control</h3>
  <p>
    The <code>BEGIN</code> / <code>COMMIT</code> / <code>ROLLBACK</code> pattern wraps destructive operations
    (like DELETE) in a safety net. Between <code>BEGIN</code> and <code>COMMIT</code>, nothing is saved
    permanently — if something goes wrong, <code>ROLLBACK</code> undoes the changes. This is especially
    important for DELETE operations, which are hard to recover from if performed incorrectly.
  </p>

  <pre><code class="language-sql">-- Example of how the deduplication DELETE should be wrapped in a transaction:
-- BEGIN;
-- DELETE FROM housing_staging WHERE row_id IN (SELECT row_id FROM temp_duplicates);
-- SELECT COUNT(*) FROM housing_staging; -- verify before committing
-- COMMIT; -- or ROLLBACK; if something went wrong</code></pre>

  <h3>Stored Procedure</h3>
  <p>
    The full cleaning pipeline was wrapped in a stored procedure called <code>clean_housing_data</code> so it
    can be re-run on fresh data with a single command:
  </p>

  <pre><code class="language-sql">CALL clean_housing_data();</code></pre>

  <p>
    The procedure was created via the MySQL Workbench routine editor. It encapsulates all five cleaning steps
    (date conversion, address population, whitespace trimming, deduplication, and column drops) into a single
    reusable routine.
  </p>

</details>
<details>
  <summary><strong>SQL Skills Demonstrated</strong></summary>

  <div style="margin-top: 12px;"></div>

  <table>
    <thead>
      <tr>
        <th>Technique</th>
        <th>Where Used</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>CREATE DATABASE</td><td>Phase 1 — Setup</td></tr>
      <tr><td>CREATE TABLE</td><td>Raw table import, staging copy</td></tr>
      <tr><td>ALTER TABLE — ADD COLUMN</td><td>SaleDateClean, row_id</td></tr>
      <tr><td>ALTER TABLE — DROP COLUMN</td><td>Removing unused columns</td></tr>
      <tr><td>UPDATE...SET</td><td>Date conversion, whitespace trimming</td></tr>
      <tr><td>UPDATE...JOIN (self-join)</td><td>Populating missing addresses</td></tr>
      <tr><td>DELETE</td><td>Removing duplicate rows</td></tr>
      <tr><td>CREATE VIEW</td><td>Final clean dataset</td></tr>
      <tr><td>CREATE INDEX</td><td>Performance optimization</td></tr>
      <tr><td>CREATE PROCEDURE</td><td>Stored procedure (stretch goal)</td></tr>
      <tr><td>STR_TO_DATE</td><td>Date type conversion</td></tr>
      <tr><td>TRIM</td><td>Whitespace cleaning</td></tr>
      <tr><td>ROW_NUMBER() OVER (PARTITION BY)</td><td>Duplicate identification</td></tr>
      <tr><td>CASE statements</td><td>NULL/empty value counting</td></tr>
      <tr><td>INFORMATION_SCHEMA queries</td><td>Data type verification</td></tr>
      <tr><td>EXPLAIN</td><td>Query performance analysis</td></tr>
      <tr><td>Staging table pattern</td><td>Raw → staging → clean workflow</td></tr>
    </tbody>
  </table>

</details>
<details>
  <summary><strong>Conclusion</strong></summary>

  <div style="margin-top: 12px;"></div>

  <p>
    This project cleaned and transformed 56,000+ Nashville housing records from a raw CSV import into a
    structured, deduplicated, and indexed MySQL dataset — ready for downstream analysis or reporting.
  </p>

  <p>
    The cleaning pipeline addressed date type conversions, missing address population via self-joins,
    whitespace trimming across 10 text columns, duplicate removal using ROW_NUMBER(), and column pruning.
    The final output includes a reusable VIEW, performance indexes, and a stored procedure that can re-run
    the entire pipeline on fresh data.
  </p>

  <p>
    <strong>How this complements the BigQuery e-commerce project:</strong> The
    <a href="/projects/sql-ecommerce-analysis/">e-commerce analysis</a> focuses on SELECT-side analytics —
    CTEs, window functions, aggregations, and business KPIs. This project covers the other half of SQL:
    DDL/DML operations that create, alter, update, and delete data. Together, the two projects demonstrate
    the full spectrum of practical SQL skills.
  </p>

  <p>
    MySQL-specific syntax demonstrated includes <code>STR_TO_DATE</code> for date parsing, <code>TRIM</code>
    for whitespace cleaning, <code>INFORMATION_SCHEMA</code> queries for metadata inspection, and prefix-length
    indexing for TEXT columns.
  </p>

  <p style="margin-top: 10px;">
    <a href="sql-code/SQL_housing_data_cleaning_project.sql">View full SQL script</a>
  </p>

</details>
