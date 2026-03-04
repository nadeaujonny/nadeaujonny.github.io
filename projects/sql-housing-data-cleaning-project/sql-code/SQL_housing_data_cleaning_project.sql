CREATE DATABASE nashville_housing; -- create database where we will put the tables
USE nashville_housing; -- navigate into created database

-- import csv via import wizard

SELECT COUNT(*) FROM housing_raw; -- check newly imported housing datatable size (total number of rows)

SELECT * FROM housing_raw LIMIT 10; -- check fields and get a glimpse of row values

CREATE TABLE housing_staging AS
SELECT * FROM housing_raw; -- create table we are to clean/manipulate first as a simple copy of the raw table

SELECT COUNT(*) FROM housing_staging; -- checking size (number or rows) of the new housing_staging table

SELECT 
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
FROM housing_staging; -- counts the number of cells in each column that contain the following values: NULL, empty string, or string with only spaces

SELECT `Sold As Vacant`, COUNT(*) AS count
FROM housing_staging
GROUP BY `Sold As Vacant`
ORDER BY count; -- counts the number Yes's and No's in the `Sold As Vacant` column

SELECT DISTINCT `Sold As Vacant`
FROM housing_staging; -- checks the different kinds of values in the `Sold As Vacant` column

SELECT
	COUNT(*) AS yes_count
FROM
	housing_staging
WHERE
	`Sold As Vacant` = 'Yes'; -- counts the number of Yes's in the `Sold As Vacant` column
    
SELECT
	COUNT(*) AS no_count
FROM
	housing_staging
WHERE
	`Sold As Vacant` = 'No'; -- counts the number of No's in the `Sold As Vacant` column
    
SELECT COUNT(*) AS duplicate_count
FROM (
    SELECT `Parcel ID`, `Property Address`, `Sale Price`, `Sale Date`, `Legal Reference`,
        ROW_NUMBER() OVER (
            PARTITION BY `Parcel ID`, `Property Address`, `Sale Price`, `Sale Date`, `Legal Reference`
            ORDER BY `Parcel ID`
        ) AS row_num
    FROM housing_staging
) duplicates
WHERE row_num > 1; 
/* counts the number of duplicates considering the condition of the values in all of those selected columns matching. 
We are counting the number of rows where the row number is greater than 1 being the instances of that row after the first instance. */

SELECT DISTINCT `Sale Date`
FROM housing_staging
ORDER BY `Sale Date`
LIMIT 20; -- selects all of the distinct sale dates and returns the 20 oldest dates from oldest to newest

ALTER TABLE housing_staging
ADD COLUMN SaleDateClean DATE; -- adding a new column for the cleaned date values

UPDATE housing_staging
SET SaleDateClean = STR_TO_DATE(`Sale Date`, '%Y-%m-%d');
/* populates the new cleaned dates column of the staging table with the corresponding 
date from each row and uses the string to date function to convert the datatype accordingly */

SELECT `Sale Date`, SaleDateClean
FROM housing_staging
LIMIT 5; -- let's us compare 5 cell values from the original date column to the cleaned dates column

SELECT 
    `Sale Date`,
    SaleDateClean,
    LENGTH(`Sale Date`) AS original_length,
    LENGTH(SaleDateClean) AS clean_length,
    YEAR(SaleDateClean) AS extracted_year,
    MONTH(SaleDateClean) AS extracted_month
FROM housing_staging
LIMIT 5; -- demonstrates our ability to now extract month and year from the cleaned date values

SELECT 
    COLUMN_NAME, 
    DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'nashville_housing'
    AND TABLE_NAME = 'housing_staging'
    AND COLUMN_NAME IN ('Sale Date', 'SaleDateClean'); -- let's us directly verify the data type of the raw versus cleaned date columns
    
SELECT a.`Parcel ID`, a.`Property Address`, b.`Property Address`
FROM housing_staging a
JOIN housing_staging b
    ON a.`Parcel ID` = b.`Parcel ID`
    AND a.`Property Address` != b.`Property Address`
WHERE TRIM(a.`Property Address`) = ''
LIMIT 10; 
/* self joins rows where parcel id's are equal but property addresses are not and selects parcel id and property addresses from table
copies a and b and filters for the rows where the property address from the table copy a is blank. Blank property address
values can be filled in using other rows that have the same parcel id and we can assume that rows with the same parcel id should have the same 
property address. */ 

UPDATE housing_staging a
JOIN housing_staging b
    ON a.`Parcel ID` = b.`Parcel ID`
    AND a.`Property Address` != b.`Property Address`
SET a.`Property Address` = b.`Property Address`
WHERE TRIM(a.`Property Address`) = '';
/* sets the property addresses of the rows with blank property addresses equal to the property 
address of another row that has the same parcel id as the row with the blank property address, using self-join again.
after running this. only 16 rows were affected, but we saw earlier that 159 rows had blank addresses, which means that for the remaining rows with blank addresses
the parcel id's didnt match any other existing rows with populated property addresses. */

SELECT 
    SUM(CASE WHEN TRIM(`Property Address`) = '' OR `Property Address` IS NULL THEN 1 ELSE 0 END) AS remaining_blank_addresses
FROM housing_staging; 
/* let's us verify how many property addresses are still blank after that last self-join update query and we would expect this count to be equal to 159-16 */

/* for this dataset and for this project at this point we may be out of luck in filling in the missing property addresses, but for real world cases that are similar
we could cross-reference external data using known parcel id numbers, geocode lookup using parcel id number, make rough inferenences from neighboring entries */

-- next step, simple trim clean ups for all remaining text columns. Get's rid of leading and trailing spaces. We have to use back ticks to refer to columns that have spaces in their names
UPDATE housing_staging
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
    
-- Check all column names in housing_staging
SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'nashville_housing'
    AND TABLE_NAME = 'housing_staging'; -- looking for unique identifier column
    
/* we are looking for a unique identifier column. But there is not one as of now. We may have 
gotten rid of it upon import when deselecting columns MyUnknownColumn and Unnamed: 0. Let's see if we can still 
successfully deduplicate the table. */

ALTER TABLE housing_staging
ADD COLUMN row_id INT AUTO_INCREMENT PRIMARY KEY; -- this adds a column of unique keys for each exsting row. we can then use these to deduplicate.

CREATE TEMPORARY TABLE temp_duplicates AS
SELECT row_id
FROM (
    SELECT row_id,
        ROW_NUMBER() OVER (
            PARTITION BY `Parcel ID`, `Property Address`, `Sale Price`, `Sale Date`, `Legal Reference`
            ORDER BY row_id
        ) AS row_num
    FROM housing_staging
) ranked
WHERE row_num > 1; 
/* creates a temp table of the row_id's of the duplicate rows. we compare `Parcel ID`, `Property Address`, 
`Sale Price`, `Sale Date`, `Legal Reference` of different rows to determine which rows are duplicates. 104 rows affected as expected. */

-- let's count how many duplicate rows we have just to make sure. 
SELECT COUNT(*) AS duplicates_to_delete FROM temp_duplicates;
-- Yes, we got 104.

-- now let's delete the rows from the staging table that have row ids that match the rows that are now in the duplicates temp table.
DELETE FROM housing_staging
WHERE row_id IN (SELECT row_id FROM temp_duplicates);

-- now let's count the number of rows that remain in the staging table. it should be 56636 original rows - 104 duplicate rows = 56532 remaining unique rows
SELECT COUNT(*) AS rows_after_dedup FROM housing_staging;
-- yes it is as expected.

-- next step: Drop unused columns
-- Sale Date: replaced by SaleDateClean
-- Tax District: not useful for analysis
-- image: not useful for analysis
-- row_id: was only needed for deduplication
ALTER TABLE housing_staging
DROP COLUMN `Sale Date`,
DROP COLUMN `Tax District`,
DROP COLUMN image,
DROP COLUMN row_id;

-- next let us create the final clean view (query shortcut for the cleaned data)
CREATE VIEW vw_housing_clean AS
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
FROM housing_staging;

CREATE INDEX idx_parcel_id ON housing_staging(`Parcel ID`);
CREATE INDEX idx_sale_date ON housing_staging(SaleDateClean);
CREATE INDEX idx_property_city ON housing_staging(`Property City`); -- we got an error here because we didn't specify how many characters to index. let's fix that next.
-- here we add indexes for commonly queried columns.

-- Fix: specify key length for TEXT column index. in this case let's just do 100 characters.
CREATE INDEX idx_property_city ON housing_staging(`Property City`(100));

-- let's do a Before/After Validation Summary
-- where we compare raw table vs cleaned staging table
SELECT 
    'Total Rows' AS Metric,
    (SELECT COUNT(*) FROM housing_raw) AS Before_Raw,
    (SELECT COUNT(*) FROM housing_staging) AS After_Clean -- first compares number of rows in raw vs cleaned table
UNION ALL
SELECT 
    'Duplicate Rows',
    104,
    0 -- gives duplicates before and after deduplication
UNION ALL
SELECT 
    'Blank Property Addresses', -- gives the blank property addresses we fixed.
    159,
    (SELECT SUM(CASE WHEN TRIM(`Property Address`) = '' OR `Property Address` IS NULL THEN 1 ELSE 0 END) FROM housing_staging)
UNION ALL
SELECT 
    'Sale Date Data Type', -- gives date data types that we changed accordingly
    0,
    1
UNION ALL
SELECT 
    'Columns Dropped', -- gives the columns we decided to drop
    0,
    4
UNION ALL
SELECT
    'Rows with Whitespace Cleaned', -- gives instances of cells that were cleaned of white space
    24172,
    0;

EXPLAIN SELECT *
FROM housing_staging
WHERE `Property City` = 'NASHVILLE'
AND SaleDateClean BETWEEN '2014-01-01' AND '2014-12-31';
-- shows that the indexes we added are being used to make the queries run faster.

-- Step 5.2: Transaction Control demonstration
-- Showing BEGIN/COMMIT/ROLLBACK pattern for safe data operations
-- NOTE: Our actual DELETE was already performed, so this demonstrates the concept

-- Example of how the deduplication DELETE should be wrapped in a transaction:
-- BEGIN;
-- DELETE FROM housing_staging WHERE row_id IN (SELECT row_id FROM temp_duplicates);
-- SELECT COUNT(*) FROM housing_staging; -- verify before committing
-- COMMIT; -- or ROLLBACK; if something went wrong

-- between the BEGIN and the COMMIT, nothing is saved or executed permanently 
-- so if something goes wrong you can rollback to undo the wrong thing that you 
-- did or if it went correctly then you can commit to save the changes.
-- this TRANSACTION CONTROL procedure is most helpful when performing deletes 
-- which would be bad and hard to recover if performed incorrectly.

-- next we can wrap up what we did when cleaning this data as a Stored Procedure — wraps the full cleaning pipeline
/*
CREATE PROCEDURE `clean_housing_data` ()
BEGIN
    -- Step 1: Add clean date column and convert
    ALTER TABLE housing_staging ADD COLUMN SaleDateClean DATE;
    UPDATE housing_staging SET SaleDateClean = STR_TO_DATE(`Sale Date`, '%Y-%m-%d');
    
    -- Step 2: Populate missing Property Addresses via self-join
    UPDATE housing_staging a
    JOIN housing_staging b
        ON a.`Parcel ID` = b.`Parcel ID`
        AND a.`Property Address` != b.`Property Address`
    SET a.`Property Address` = b.`Property Address`
    WHERE TRIM(a.`Property Address`) = '';
    
    -- Step 3: Trim whitespace from text columns
    UPDATE housing_staging
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
    
    -- Step 4: Remove duplicates
    ALTER TABLE housing_staging ADD COLUMN row_id INT AUTO_INCREMENT PRIMARY KEY;
    
    DROP TEMPORARY TABLE IF EXISTS temp_dup;
    CREATE TEMPORARY TABLE temp_dup AS
    SELECT row_id FROM (
        SELECT row_id,
            ROW_NUMBER() OVER (
                PARTITION BY `Parcel ID`, `Property Address`, `Sale Price`, `Sale Date`, `Legal Reference`
                ORDER BY row_id
            ) AS row_num
        FROM housing_staging
    ) ranked WHERE row_num > 1;
    
    DELETE FROM housing_staging WHERE row_id IN (SELECT row_id FROM temp_dup);
    DROP TEMPORARY TABLE IF EXISTS temp_dup;
    
    -- Step 5: Drop unused columns
    ALTER TABLE housing_staging DROP COLUMN `Sale Date`;
    ALTER TABLE housing_staging DROP COLUMN `Tax District`;
    ALTER TABLE housing_staging DROP COLUMN image;
    ALTER TABLE housing_staging DROP COLUMN row_id;
END
*/

-- got an error. i think we have to use the left panel to create a stored procedure
-- let's undo what we did in case we did anything incorrectly with that last command.
DROP PROCEDURE IF EXISTS clean_housing_data;

-- alright we correclty added the stored procedure written above into a routine tab and 
-- successfully stored it as a stored procedure within the stored procedures of this nashville_housing database.
-- Stored Procedure created via MySQL Workbench routine editor
-- To run the full cleaning pipeline on fresh data: CALL clean_housing_data();