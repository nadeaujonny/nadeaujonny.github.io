/*
================================================================================
  SUPPLY CHAIN ANALYTICS — SCHEMA DDL
  01_schema_ddl.sql
  
  Oracle Autonomous Database (19c)
  Author: Jonathan Nadeau
  
  Creates the normalized relational schema from the DataCo Smart Supply Chain
  flat CSV (~180,000 rows, 53 columns). The flat file is decomposed into 5
  transactional tables (CUSTOMERS, PRODUCTS, ORDERS, ORDER_ITEMS, SHIPMENTS)
  plus 3 supply planning tables (FORECAST_PLAN, MRP_REQUIREMENTS,
  INVENTORY_SNAPSHOT) that support the MRP simulation and demand planning
  round-trip.
================================================================================
*/


-- ============================================================================
-- 1. DROP EXISTING OBJECTS (safe re-run)
-- ============================================================================
BEGIN EXECUTE IMMEDIATE 'DROP TABLE MRP_REQUIREMENTS CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE FORECAST_PLAN CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE INVENTORY_SNAPSHOT CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE SHIPMENTS CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE ORDER_ITEMS CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE ORDERS CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE PRODUCTS CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE CUSTOMERS CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE STG_DATACO CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/


-- ============================================================================
-- 2. STAGING TABLE (mirrors flat CSV for initial data load)
-- ============================================================================
CREATE TABLE STG_DATACO (
    TYPE                        VARCHAR2(50),
    DAYS_FOR_SHIPPING_REAL      NUMBER(5),
    DAYS_FOR_SHIPMENT_SCHEDULED NUMBER(5),
    BENEFIT_PER_ORDER           NUMBER(12,2),
    SALES_PER_CUSTOMER          NUMBER(14,4),
    DELIVERY_STATUS             VARCHAR2(50),
    LATE_DELIVERY_RISK          NUMBER(1),
    CATEGORY_ID                 NUMBER(10),
    CATEGORY_NAME               VARCHAR2(150),
    CUSTOMER_CITY               VARCHAR2(100),
    CUSTOMER_COUNTRY            VARCHAR2(100),
    CUSTOMER_EMAIL              VARCHAR2(200),
    CUSTOMER_FNAME              VARCHAR2(100),
    CUSTOMER_ID                 NUMBER(10),
    CUSTOMER_LNAME              VARCHAR2(100),
    CUSTOMER_PASSWORD           VARCHAR2(200),
    CUSTOMER_SEGMENT            VARCHAR2(50),
    CUSTOMER_STATE              VARCHAR2(100),
    CUSTOMER_STREET             VARCHAR2(200),
    CUSTOMER_ZIPCODE            VARCHAR2(20),
    DEPARTMENT_ID               NUMBER(10),
    DEPARTMENT_NAME             VARCHAR2(100),
    LATITUDE                    NUMBER(12,8),
    LONGITUDE                   NUMBER(12,8),
    MARKET                      VARCHAR2(100),
    ORDER_CITY                  VARCHAR2(100),
    ORDER_COUNTRY               VARCHAR2(100),
    ORDER_CUSTOMER_ID           NUMBER(10),
    ORDER_DATE                  TIMESTAMP,
    ORDER_ID                    NUMBER(10),
    ORDER_ITEM_CARDPROD_ID      NUMBER(10),
    ORDER_ITEM_DISCOUNT         NUMBER(12,4),
    ORDER_ITEM_DISCOUNT_RATE    NUMBER(10,6),
    ORDER_ITEM_ID               NUMBER(10),
    ORDER_ITEM_PRODUCT_PRICE    NUMBER(12,2),
    ORDER_ITEM_PROFIT_RATIO     NUMBER(10,6),
    ORDER_ITEM_QUANTITY         NUMBER(10),
    SALES                       NUMBER(14,4),
    ORDER_ITEM_TOTAL            NUMBER(14,4),
    ORDER_PROFIT_PER_ORDER      NUMBER(12,2),
    ORDER_REGION                VARCHAR2(100),
    ORDER_STATE                 VARCHAR2(100),
    ORDER_STATUS                VARCHAR2(50),
    ORDER_ZIPCODE               VARCHAR2(20),
    PRODUCT_CARD_ID             NUMBER(10),
    PRODUCT_CATEGORY_ID         NUMBER(10),
    PRODUCT_DESCRIPTION         VARCHAR2(1000),
    PRODUCT_IMAGE               VARCHAR2(500),
    PRODUCT_NAME                VARCHAR2(300),
    PRODUCT_PRICE               NUMBER(12,2),
    PRODUCT_STATUS              NUMBER(1),
    SHIPPING_DATE               TIMESTAMP,
    SHIPPING_MODE               VARCHAR2(50)
);

COMMENT ON TABLE STG_DATACO IS 'Staging table — mirrors flat CSV structure for initial data load. Data is split into normalized tables via INSERT...SELECT.';


-- ============================================================================
-- 3. DIMENSION TABLES
-- ============================================================================

-- CUSTOMERS
CREATE TABLE CUSTOMERS (
    CUSTOMER_ID         NUMBER(10)      NOT NULL,
    FIRST_NAME          VARCHAR2(100)   NOT NULL,
    LAST_NAME           VARCHAR2(100)   NOT NULL,
    EMAIL               VARCHAR2(200),
    SEGMENT             VARCHAR2(50)    NOT NULL,
    CITY                VARCHAR2(100),
    STATE               VARCHAR2(100),
    COUNTRY             VARCHAR2(100),
    STREET              VARCHAR2(200),
    ZIPCODE             VARCHAR2(20),
    LATITUDE            NUMBER(12,8),
    LONGITUDE           NUMBER(12,8),
    CONSTRAINT PK_CUSTOMERS PRIMARY KEY (CUSTOMER_ID)
);

COMMENT ON TABLE CUSTOMERS IS 'Customer master data — one row per unique customer';
COMMENT ON COLUMN CUSTOMERS.SEGMENT IS 'Consumer, Corporate, or Home Office';


-- PRODUCTS (with planning parameter columns for MRP)
CREATE TABLE PRODUCTS (
    PRODUCT_CARD_ID     NUMBER(10)      NOT NULL,
    PRODUCT_NAME        VARCHAR2(300)   NOT NULL,
    CATEGORY_ID         NUMBER(10)      NOT NULL,
    CATEGORY_NAME       VARCHAR2(150)   NOT NULL,
    DEPARTMENT_ID       NUMBER(10)      NOT NULL,
    DEPARTMENT_NAME     VARCHAR2(100)   NOT NULL,
    PRODUCT_PRICE       NUMBER(12,2)    NOT NULL,
    PRODUCT_STATUS      NUMBER(1)       DEFAULT 0,
    PRODUCT_DESCRIPTION VARCHAR2(1000),
    PRODUCT_IMAGE       VARCHAR2(500),
    PRODUCT_CATEGORY_ID NUMBER(10),
    -- Planning parameters (populated during inventory optimization phase)
    LEAD_TIME_DAYS      NUMBER(5)       DEFAULT 7,
    LOT_SIZING_METHOD   VARCHAR2(20)    DEFAULT 'EOQ',
    MIN_ORDER_QTY       NUMBER(10)      DEFAULT 1,
    EOQ                 NUMBER(12,2),
    SAFETY_STOCK        NUMBER(12,2),
    REORDER_POINT       NUMBER(12,2),
    CONSTRAINT PK_PRODUCTS PRIMARY KEY (PRODUCT_CARD_ID)
);

COMMENT ON TABLE PRODUCTS IS 'Product master data with planning parameters for MRP simulation';
COMMENT ON COLUMN PRODUCTS.LEAD_TIME_DAYS IS 'Default lead time in days — updated by inventory analysis';
COMMENT ON COLUMN PRODUCTS.LOT_SIZING_METHOD IS 'EOQ, FIXED_LOT, or LOT_FOR_LOT — drives MRP planned order qty';
COMMENT ON COLUMN PRODUCTS.SAFETY_STOCK IS 'Calculated from demand variability and service level Z-score';
COMMENT ON COLUMN PRODUCTS.REORDER_POINT IS '(Avg Daily Demand x Lead Time) + Safety Stock';


-- ============================================================================
-- 4. FACT TABLES
-- ============================================================================

-- ORDERS
CREATE TABLE ORDERS (
    ORDER_ID            NUMBER(10)      NOT NULL,
    ORDER_DATE          TIMESTAMP       NOT NULL,
    ORDER_STATUS        VARCHAR2(50)    NOT NULL,
    MARKET              VARCHAR2(100),
    ORDER_REGION        VARCHAR2(100),
    ORDER_COUNTRY       VARCHAR2(100),
    ORDER_CITY          VARCHAR2(100),
    ORDER_STATE         VARCHAR2(100),
    ORDER_ZIPCODE       VARCHAR2(20),
    CONSTRAINT PK_ORDERS PRIMARY KEY (ORDER_ID)
);

COMMENT ON TABLE ORDERS IS 'Order header — one row per unique order';


-- ORDER_ITEMS
CREATE TABLE ORDER_ITEMS (
    ORDER_ITEM_ID       NUMBER(10)      NOT NULL,
    ORDER_ID            NUMBER(10)      NOT NULL,
    PRODUCT_CARD_ID     NUMBER(10)      NOT NULL,
    CUSTOMER_ID         NUMBER(10)      NOT NULL,
    QUANTITY            NUMBER(10)      NOT NULL,
    UNIT_PRICE          NUMBER(12,2)    NOT NULL,
    DISCOUNT_AMOUNT     NUMBER(12,4)    DEFAULT 0,
    DISCOUNT_RATE       NUMBER(10,6)    DEFAULT 0,
    PROFIT_RATIO        NUMBER(10,6),
    SALES               NUMBER(14,4)    NOT NULL,
    ITEM_TOTAL          NUMBER(14,4),
    PROFIT_PER_ORDER    NUMBER(12,2),
    BENEFIT_PER_ORDER   NUMBER(12,2),
    SALES_PER_CUSTOMER  NUMBER(14,4),
    PAYMENT_TYPE        VARCHAR2(50),
    CONSTRAINT PK_ORDER_ITEMS PRIMARY KEY (ORDER_ITEM_ID),
    CONSTRAINT FK_OI_ORDER FOREIGN KEY (ORDER_ID) REFERENCES ORDERS(ORDER_ID),
    CONSTRAINT FK_OI_PRODUCT FOREIGN KEY (PRODUCT_CARD_ID) REFERENCES PRODUCTS(PRODUCT_CARD_ID),
    CONSTRAINT FK_OI_CUSTOMER FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMERS(CUSTOMER_ID)
);

COMMENT ON TABLE ORDER_ITEMS IS 'Line-item detail — one row per item per order';


-- SHIPMENTS
CREATE TABLE SHIPMENTS (
    SHIPMENT_ID         NUMBER(10)      GENERATED ALWAYS AS IDENTITY NOT NULL,
    ORDER_ITEM_ID       NUMBER(10)      NOT NULL,
    SHIPPING_MODE       VARCHAR2(50)    NOT NULL,
    SHIPPING_DATE       TIMESTAMP,
    DAYS_SHIPPING_REAL  NUMBER(5),
    DAYS_SHIPPING_SCHED NUMBER(5),
    DELIVERY_STATUS     VARCHAR2(50),
    LATE_DELIVERY_RISK  NUMBER(1)       DEFAULT 0,
    CONSTRAINT PK_SHIPMENTS PRIMARY KEY (SHIPMENT_ID),
    CONSTRAINT FK_SH_ORDER_ITEM FOREIGN KEY (ORDER_ITEM_ID) REFERENCES ORDER_ITEMS(ORDER_ITEM_ID)
);

COMMENT ON TABLE SHIPMENTS IS 'Fulfillment data — shipping performance and delivery status per order item';


-- ============================================================================
-- 5. SUPPLY PLANNING TABLES (created empty, populated in later phases)
-- ============================================================================

-- FORECAST_PLAN — receives demand forecasts from Excel (Phase 4)
CREATE TABLE FORECAST_PLAN (
    FORECAST_ID         NUMBER(10)      GENERATED ALWAYS AS IDENTITY NOT NULL,
    CATEGORY_NAME       VARCHAR2(150)   NOT NULL,
    FORECAST_PERIOD     DATE            NOT NULL,
    FORECASTED_QTY      NUMBER(12,2)    NOT NULL,
    FORECAST_METHOD     VARCHAR2(50),
    CONFIDENCE_LOWER    NUMBER(12,2),
    CONFIDENCE_UPPER    NUMBER(12,2),
    CREATED_DATE        TIMESTAMP       DEFAULT SYSTIMESTAMP,
    CONSTRAINT PK_FORECAST_PLAN PRIMARY KEY (FORECAST_ID)
);

COMMENT ON TABLE FORECAST_PLAN IS 'Demand forecast data — populated from Excel, consumed by MRP stored procedure';
COMMENT ON COLUMN FORECAST_PLAN.FORECAST_METHOD IS 'ETS, MOVING_AVG, or WEIGHTED_MA';
COMMENT ON COLUMN FORECAST_PLAN.FORECAST_PERIOD IS 'First day of the forecast month';


-- MRP_REQUIREMENTS — populated by stored procedure MRP logic (Phase 2)
CREATE TABLE MRP_REQUIREMENTS (
    MRP_ID              NUMBER(10)      GENERATED ALWAYS AS IDENTITY NOT NULL,
    CATEGORY_NAME       VARCHAR2(150)   NOT NULL,
    PLANNING_PERIOD     DATE            NOT NULL,
    GROSS_REQUIREMENTS  NUMBER(12,2)    DEFAULT 0,
    SCHEDULED_RECEIPTS  NUMBER(12,2)    DEFAULT 0,
    PROJECTED_ON_HAND   NUMBER(12,2)    DEFAULT 0,
    NET_REQUIREMENTS    NUMBER(12,2)    DEFAULT 0,
    PLANNED_ORDER_QTY   NUMBER(12,2)    DEFAULT 0,
    PLANNED_RELEASE_DATE DATE,
    LOT_SIZING_METHOD   VARCHAR2(20),
    EXCEPTION_FLAG      VARCHAR2(50),
    EXCEPTION_MESSAGE   VARCHAR2(500),
    CREATED_DATE        TIMESTAMP       DEFAULT SYSTIMESTAMP,
    CONSTRAINT PK_MRP_REQUIREMENTS PRIMARY KEY (MRP_ID)
);

COMMENT ON TABLE MRP_REQUIREMENTS IS 'MRP output — populated by REFRESH_SUPPLY_CHAIN_DATA stored procedure';
COMMENT ON COLUMN MRP_REQUIREMENTS.EXCEPTION_FLAG IS 'EXPEDITE, RESCHEDULE, SPLIT, or NULL if no exception';


-- INVENTORY_SNAPSHOT — simulated current inventory positions
CREATE TABLE INVENTORY_SNAPSHOT (
    SNAPSHOT_ID         NUMBER(10)      GENERATED ALWAYS AS IDENTITY NOT NULL,
    CATEGORY_NAME       VARCHAR2(150)   NOT NULL,
    ON_HAND_QTY         NUMBER(12,2)    DEFAULT 0,
    IN_TRANSIT_QTY      NUMBER(12,2)    DEFAULT 0,
    ALLOCATED_QTY       NUMBER(12,2)    DEFAULT 0,
    AVAILABLE_QTY       NUMBER(12,2)    DEFAULT 0,
    LAST_UPDATED        TIMESTAMP       DEFAULT SYSTIMESTAMP,
    CONSTRAINT PK_INVENTORY_SNAPSHOT PRIMARY KEY (SNAPSHOT_ID)
);

COMMENT ON TABLE INVENTORY_SNAPSHOT IS 'Simulated current inventory — derived from order/shipment data, feeds MRP starting position';


-- ============================================================================
-- 6. INDEXES (performance optimization for common query patterns)
-- ============================================================================

-- Order lookups by date (time series analysis, demand extraction)
CREATE INDEX IDX_ORDERS_DATE ON ORDERS(ORDER_DATE);

-- Order lookups by status (fulfillment KPIs, filtering)
CREATE INDEX IDX_ORDERS_STATUS ON ORDERS(ORDER_STATUS);

-- Order item lookups by order (joining line items to headers)
CREATE INDEX IDX_OI_ORDER_ID ON ORDER_ITEMS(ORDER_ID);

-- Order item lookups by product (product-level aggregation)
CREATE INDEX IDX_OI_PRODUCT_ID ON ORDER_ITEMS(PRODUCT_CARD_ID);

-- Order item lookups by customer (customer-level analysis)
CREATE INDEX IDX_OI_CUSTOMER_ID ON ORDER_ITEMS(CUSTOMER_ID);

-- Shipment lookups by order item (joining fulfillment to line items)
CREATE INDEX IDX_SH_ORDER_ITEM_ID ON SHIPMENTS(ORDER_ITEM_ID);

-- Shipment lookups by delivery status (late delivery analysis)
CREATE INDEX IDX_SH_DELIVERY_STATUS ON SHIPMENTS(DELIVERY_STATUS);

-- Product lookups by category (category-level reporting)
CREATE INDEX IDX_PROD_CATEGORY ON PRODUCTS(CATEGORY_NAME);

-- Forecast lookups by category and period (MRP consumption)
CREATE INDEX IDX_FORECAST_CAT_PERIOD ON FORECAST_PLAN(CATEGORY_NAME, FORECAST_PERIOD);

-- MRP lookups by category and period (supply plan reporting)
CREATE INDEX IDX_MRP_CAT_PERIOD ON MRP_REQUIREMENTS(CATEGORY_NAME, PLANNING_PERIOD);

-- Inventory lookups by category (MRP starting position)
CREATE INDEX IDX_INV_CATEGORY ON INVENTORY_SNAPSHOT(CATEGORY_NAME);


-- ============================================================================
-- 7. VERIFICATION
-- ============================================================================
SELECT table_name, num_rows
FROM user_tables
WHERE table_name IN (
    'STG_DATACO', 'CUSTOMERS', 'PRODUCTS', 'ORDERS', 'ORDER_ITEMS',
    'SHIPMENTS', 'FORECAST_PLAN', 'MRP_REQUIREMENTS', 'INVENTORY_SNAPSHOT'
)
ORDER BY table_name;