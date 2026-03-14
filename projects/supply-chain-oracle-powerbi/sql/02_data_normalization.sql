/*
================================================================================
  SUPPLY CHAIN ANALYTICS — DATA NORMALIZATION
  02_data_normalization.sql
  
  Oracle Autonomous Database (19c)
  Author: Jonathan Nadeau
  
  Splits the flat STG_DATACO staging table (~180,500 rows) into 5 normalized
  transactional tables: CUSTOMERS, PRODUCTS, ORDERS, ORDER_ITEMS, SHIPMENTS.
  
  The 3 planning tables (FORECAST_PLAN, MRP_REQUIREMENTS, INVENTORY_SNAPSHOT)
  remain empty — they are populated in later phases.
  
  IMPORTANT: Run 01_schema_ddl.sql first, then load the CSV into STG_DATACO
  via Data Load, then run this script.
  
  Run order:
    1. CUSTOMERS  (dimension — no dependencies)
    2. PRODUCTS   (dimension — no dependencies)
    3. ORDERS     (fact header — no FK dependencies on other fact tables)
    4. ORDER_ITEMS (fact detail — depends on ORDERS, PRODUCTS, CUSTOMERS)
    5. SHIPMENTS  (fact — depends on ORDER_ITEMS)
    6. INVENTORY_SNAPSHOT (derived from loaded data)
    7. Verification queries
================================================================================
*/


-- ============================================================================
-- 1. CUSTOMERS (deduplicated from staging)
-- ============================================================================
-- The staging table has one row per order item, so customers repeat.
-- We take the first occurrence of each Customer Id.

INSERT INTO CUSTOMERS (
    CUSTOMER_ID, FIRST_NAME, LAST_NAME, EMAIL, SEGMENT,
    CITY, STATE, COUNTRY, STREET, ZIPCODE, LATITUDE, LONGITUDE
)
SELECT
    CUSTOMER_ID,
    CUSTOMER_FNAME,
    CUSTOMER_LNAME,
    CUSTOMER_EMAIL,
    CUSTOMER_SEGMENT,
    CUSTOMER_CITY,
    CUSTOMER_STATE,
    CUSTOMER_COUNTRY,
    CUSTOMER_STREET,
    CUSTOMER_ZIPCODE,
    LATITUDE,
    LONGITUDE
FROM (
    SELECT
        s.*,
        ROW_NUMBER() OVER (PARTITION BY s.CUSTOMER_ID ORDER BY s.ORDER_DATE DESC) AS rn
    FROM STG_DATACO s
)
WHERE rn = 1; -- window function here used to include only distinct instances per customer

COMMIT;


-- ============================================================================
-- 2. PRODUCTS (deduplicated from staging)
-- ============================================================================
-- Multiple order items reference the same product. We take one row per
-- Product Card Id. Planning parameter columns keep their defaults and
-- will be updated during the inventory optimization phase.

INSERT INTO PRODUCTS (
    PRODUCT_CARD_ID, PRODUCT_NAME, CATEGORY_ID, CATEGORY_NAME,
    DEPARTMENT_ID, DEPARTMENT_NAME, PRODUCT_PRICE, PRODUCT_STATUS,
    PRODUCT_DESCRIPTION, PRODUCT_IMAGE, PRODUCT_CATEGORY_ID
)
SELECT
    PRODUCT_CARD_ID,
    PRODUCT_NAME,
    CATEGORY_ID,
    CATEGORY_NAME,
    DEPARTMENT_ID,
    DEPARTMENT_NAME,
    PRODUCT_PRICE,
    PRODUCT_STATUS,
    PRODUCT_DESCRIPTION,
    PRODUCT_IMAGE,
    PRODUCT_CATEGORY_ID
FROM (
    SELECT
        s.*,
        ROW_NUMBER() OVER (PARTITION BY s.PRODUCT_CARD_ID ORDER BY s.ORDER_DATE DESC) AS rn
    FROM STG_DATACO s
)
WHERE rn = 1; -- window function here used to include only distinct instances per product

COMMIT;


-- ============================================================================
-- 3. ORDERS (deduplicated from staging)
-- ============================================================================
-- Each Order Id can appear multiple times in the flat file (one row per
-- order item). We extract unique order headers.

INSERT INTO ORDERS (
    ORDER_ID, ORDER_DATE, ORDER_STATUS, MARKET,
    ORDER_REGION, ORDER_COUNTRY, ORDER_CITY, ORDER_STATE, ORDER_ZIPCODE
)
SELECT
    ORDER_ID,
    ORDER_DATE,
    ORDER_STATUS,
    MARKET,
    ORDER_REGION,
    ORDER_COUNTRY,
    ORDER_CITY,
    ORDER_STATE,
    ORDER_ZIPCODE
FROM (
    SELECT
        s.*,
        ROW_NUMBER() OVER (PARTITION BY s.ORDER_ID ORDER BY s.ORDER_ITEM_ID) AS rn
    FROM STG_DATACO s
)
WHERE rn = 1; -- window function here used to include only distinct instances per order

COMMIT;


-- ============================================================================
-- 4. ORDER_ITEMS (one row per order item from staging)
-- ============================================================================
-- Each row in STG_DATACO represents one order item. ORDER_ITEM_ID is unique.
-- ORDER_CUSTOMER_ID maps to CUSTOMER_ID (confirmed they match).
-- ORDER_ITEM_CARDPROD_ID maps to PRODUCT_CARD_ID (confirmed they match).

INSERT INTO ORDER_ITEMS (
    ORDER_ITEM_ID, ORDER_ID, PRODUCT_CARD_ID, CUSTOMER_ID,
    QUANTITY, UNIT_PRICE, DISCOUNT_AMOUNT, DISCOUNT_RATE,
    PROFIT_RATIO, SALES, ITEM_TOTAL, PROFIT_PER_ORDER,
    BENEFIT_PER_ORDER, SALES_PER_CUSTOMER, PAYMENT_TYPE
)
SELECT
    ORDER_ITEM_ID,
    ORDER_ID,
    PRODUCT_CARD_ID,
    CUSTOMER_ID,
    ORDER_ITEM_QUANTITY,
    ORDER_ITEM_PRODUCT_PRICE,
    ORDER_ITEM_DISCOUNT,
    ORDER_ITEM_DISCOUNT_RATE,
    ORDER_ITEM_PROFIT_RATIO,
    SALES,
    ORDER_ITEM_TOTAL,
    ORDER_PROFIT_PER_ORDER,
    BENEFIT_PER_ORDER,
    SALES_PER_CUSTOMER,
    TYPE
FROM STG_DATACO;

COMMIT;


-- ============================================================================
-- 5. SHIPMENTS (one row per order item from staging)
-- ============================================================================
-- Each order item has associated shipping data. SHIPMENT_ID is auto-generated
-- via identity column.

INSERT INTO SHIPMENTS (
    ORDER_ITEM_ID, SHIPPING_MODE, SHIPPING_DATE,
    DAYS_SHIPPING_REAL, DAYS_SHIPPING_SCHED,
    DELIVERY_STATUS, LATE_DELIVERY_RISK
)
SELECT
    ORDER_ITEM_ID,
    SHIPPING_MODE,
    SHIPPING_DATE,
    DAYS_FOR_SHIPPING_REAL,
    DAYS_FOR_SHIPMENT_SCHEDULED,
    DELIVERY_STATUS,
    LATE_DELIVERY_RISK
FROM STG_DATACO;

COMMIT;


-- ============================================================================
-- 6. INVENTORY_SNAPSHOT (simulated starting inventory)
-- ============================================================================
-- We derive a simulated inventory position per category from the order data.
-- This gives the MRP simulation a realistic starting point.
-- Logic: estimate on-hand as a fraction of average monthly demand to simulate
-- a mid-cycle inventory position.

INSERT INTO INVENTORY_SNAPSHOT (
    CATEGORY_NAME, ON_HAND_QTY, IN_TRANSIT_QTY,
    ALLOCATED_QTY, AVAILABLE_QTY
)
SELECT
    CATEGORY_NAME,
    ROUND(AVG_MONTHLY_DEMAND * 1.5, 0)  AS ON_HAND_QTY,      -- ~6 weeks of stock
    ROUND(AVG_MONTHLY_DEMAND * 0.3, 0)  AS IN_TRANSIT_QTY,    -- ~1 week in transit
    ROUND(AVG_MONTHLY_DEMAND * 0.2, 0)  AS ALLOCATED_QTY,     -- ~1 week allocated
    ROUND(AVG_MONTHLY_DEMAND * 1.5, 0)
        + ROUND(AVG_MONTHLY_DEMAND * 0.3, 0)
        - ROUND(AVG_MONTHLY_DEMAND * 0.2, 0) AS AVAILABLE_QTY -- on_hand + transit - allocated
FROM (
    SELECT
        p.CATEGORY_NAME,
        ROUND(COUNT(oi.ORDER_ITEM_ID) / 
            GREATEST(
                MONTHS_BETWEEN(MAX(o.ORDER_DATE), MIN(o.ORDER_DATE)),
                1
            ), 2) AS AVG_MONTHLY_DEMAND
    FROM ORDER_ITEMS oi
    JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    GROUP BY p.CATEGORY_NAME
);

COMMIT;


-- ============================================================================
-- 7. VERIFICATION
-- ============================================================================

-- Row counts for all tables
SELECT 'STG_DATACO' AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM STG_DATACO
UNION ALL
SELECT 'CUSTOMERS', COUNT(*) FROM CUSTOMERS
UNION ALL
SELECT 'PRODUCTS', COUNT(*) FROM PRODUCTS
UNION ALL
SELECT 'ORDERS', COUNT(*) FROM ORDERS
UNION ALL
SELECT 'ORDER_ITEMS', COUNT(*) FROM ORDER_ITEMS
UNION ALL
SELECT 'SHIPMENTS', COUNT(*) FROM SHIPMENTS
UNION ALL
SELECT 'INVENTORY_SNAPSHOT', COUNT(*) FROM INVENTORY_SNAPSHOT
UNION ALL
SELECT 'FORECAST_PLAN', COUNT(*) FROM FORECAST_PLAN
UNION ALL
SELECT 'MRP_REQUIREMENTS', COUNT(*) FROM MRP_REQUIREMENTS
ORDER BY TABLE_NAME;
-- this script had some errors. here is a script that corrects what the one above did wrong:

/*
================================================================================
  SUPPLY CHAIN ANALYTICS — DATA NORMALIZATION FIX
  02b_data_normalization_fix.sql
  
  Fixes the NULL last name issue in CUSTOMERS and reruns the failed inserts.
  Run this AFTER the first attempt of 02_data_normalization.sql.
  
  What happened:
    - CUSTOMERS failed: some rows have NULL CUSTOMER_LNAME
    - PRODUCTS: OK (118 rows)
    - ORDERS: OK (65,752 rows)
    - ORDER_ITEMS: failed (FK to CUSTOMERS failed because customers didn't load)
    - SHIPMENTS: failed (FK to ORDER_ITEMS failed because order items didn't load)
    - INVENTORY_SNAPSHOT: 0 rows (no order items to calculate from)
  
  Fix: Use NVL() to replace NULLs with placeholder values, then rerun.
================================================================================
*/


-- ============================================================================
-- 1. CLEAR FAILED/PARTIAL DATA (keep PRODUCTS and ORDERS which succeeded)
-- ============================================================================
DELETE FROM INVENTORY_SNAPSHOT;
COMMIT;

DELETE FROM SHIPMENTS;
COMMIT;

DELETE FROM ORDER_ITEMS;
COMMIT;

DELETE FROM CUSTOMERS;
COMMIT;


-- ============================================================================
-- 2. CUSTOMERS (fixed — handle NULLs)
-- ============================================================================
INSERT INTO CUSTOMERS (
    CUSTOMER_ID, FIRST_NAME, LAST_NAME, EMAIL, SEGMENT,
    CITY, STATE, COUNTRY, STREET, ZIPCODE, LATITUDE, LONGITUDE
)
SELECT
    CUSTOMER_ID,
    NVL(CUSTOMER_FNAME, 'Unknown'),
    NVL(CUSTOMER_LNAME, 'Unknown'),
    CUSTOMER_EMAIL,
    NVL(CUSTOMER_SEGMENT, 'Unknown'),
    CUSTOMER_CITY,
    CUSTOMER_STATE,
    CUSTOMER_COUNTRY,
    CUSTOMER_STREET,
    CUSTOMER_ZIPCODE,
    LATITUDE,
    LONGITUDE
FROM (
    SELECT
        s.*,
        ROW_NUMBER() OVER (PARTITION BY s.CUSTOMER_ID ORDER BY s.ORDER_DATE DESC) AS rn
    FROM STG_DATACO s
)
WHERE rn = 1;

COMMIT;


-- ============================================================================
-- 3. ORDER_ITEMS (rerun — CUSTOMERS now loaded)
-- ============================================================================
INSERT INTO ORDER_ITEMS (
    ORDER_ITEM_ID, ORDER_ID, PRODUCT_CARD_ID, CUSTOMER_ID,
    QUANTITY, UNIT_PRICE, DISCOUNT_AMOUNT, DISCOUNT_RATE,
    PROFIT_RATIO, SALES, ITEM_TOTAL, PROFIT_PER_ORDER,
    BENEFIT_PER_ORDER, SALES_PER_CUSTOMER, PAYMENT_TYPE
)
SELECT
    ORDER_ITEM_ID,
    ORDER_ID,
    PRODUCT_CARD_ID,
    CUSTOMER_ID,
    ORDER_ITEM_QUANTITY,
    ORDER_ITEM_PRODUCT_PRICE,
    ORDER_ITEM_DISCOUNT,
    ORDER_ITEM_DISCOUNT_RATE,
    ORDER_ITEM_PROFIT_RATIO,
    SALES,
    ORDER_ITEM_TOTAL,
    ORDER_PROFIT_PER_ORDER,
    BENEFIT_PER_ORDER,
    SALES_PER_CUSTOMER,
    TYPE
FROM STG_DATACO;

COMMIT;


-- ============================================================================
-- 4. SHIPMENTS (rerun — ORDER_ITEMS now loaded)
-- ============================================================================
INSERT INTO SHIPMENTS (
    ORDER_ITEM_ID, SHIPPING_MODE, SHIPPING_DATE,
    DAYS_SHIPPING_REAL, DAYS_SHIPPING_SCHED,
    DELIVERY_STATUS, LATE_DELIVERY_RISK
)
SELECT
    ORDER_ITEM_ID,
    SHIPPING_MODE,
    SHIPPING_DATE,
    DAYS_FOR_SHIPPING_REAL,
    DAYS_FOR_SHIPMENT_SCHEDULED,
    DELIVERY_STATUS,
    LATE_DELIVERY_RISK
FROM STG_DATACO;

COMMIT;


-- ============================================================================
-- 5. INVENTORY_SNAPSHOT (rerun — ORDER_ITEMS now has data)
-- ============================================================================
INSERT INTO INVENTORY_SNAPSHOT (
    CATEGORY_NAME, ON_HAND_QTY, IN_TRANSIT_QTY,
    ALLOCATED_QTY, AVAILABLE_QTY
)
SELECT
    CATEGORY_NAME,
    ROUND(AVG_MONTHLY_DEMAND * 1.5, 0)  AS ON_HAND_QTY,
    ROUND(AVG_MONTHLY_DEMAND * 0.3, 0)  AS IN_TRANSIT_QTY,
    ROUND(AVG_MONTHLY_DEMAND * 0.2, 0)  AS ALLOCATED_QTY,
    ROUND(AVG_MONTHLY_DEMAND * 1.5, 0)
        + ROUND(AVG_MONTHLY_DEMAND * 0.3, 0)
        - ROUND(AVG_MONTHLY_DEMAND * 0.2, 0) AS AVAILABLE_QTY
FROM (
    SELECT
        p.CATEGORY_NAME,
        ROUND(COUNT(oi.ORDER_ITEM_ID) / 
            GREATEST(
                MONTHS_BETWEEN(MAX(o.ORDER_DATE), MIN(o.ORDER_DATE)),
                1
            ), 2) AS AVG_MONTHLY_DEMAND
    FROM ORDER_ITEMS oi
    JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    GROUP BY p.CATEGORY_NAME
);

COMMIT;


-- ============================================================================
-- 6. VERIFICATION
-- ============================================================================
SELECT 'STG_DATACO' AS TBL, COUNT(*) AS CNT FROM STG_DATACO
UNION ALL SELECT 'CUSTOMERS', COUNT(*) FROM CUSTOMERS
UNION ALL SELECT 'PRODUCTS', COUNT(*) FROM PRODUCTS
UNION ALL SELECT 'ORDERS', COUNT(*) FROM ORDERS
UNION ALL SELECT 'ORDER_ITEMS', COUNT(*) FROM ORDER_ITEMS
UNION ALL SELECT 'SHIPMENTS', COUNT(*) FROM SHIPMENTS
UNION ALL SELECT 'INVENTORY_SNAPSHOT', COUNT(*) FROM INVENTORY_SNAPSHOT
UNION ALL SELECT 'FORECAST_PLAN', COUNT(*) FROM FORECAST_PLAN
UNION ALL SELECT 'MRP_REQUIREMENTS', COUNT(*) FROM MRP_REQUIREMENTS;