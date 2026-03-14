/*
================================================================================
  SUPPLY CHAIN ANALYTICS — STORED PROCEDURE, MRP LOGIC & SCHEDULER JOB
  06_stored_procedure_mrp.sql
  
  Oracle Autonomous Database (19c)
  Author: Jonathan Nadeau
  
  This script creates:
    1. REFRESH_SUPPLY_CHAIN_DATA stored procedure
       - Refreshes INVENTORY_SNAPSHOT with current calculated positions
       - Reads demand forecasts from FORECAST_PLAN
       - Executes MRP net requirements calculation (gross-to-net netting,
         lot sizing, lead time offsets, exception flagging)
       - Writes planned orders to MRP_REQUIREMENTS
       - Logs refresh timestamp and row counts
    2. DBMS_SCHEDULER job for automated nightly execution at 2:00 AM
    3. Verification queries
  
  The MRP logic:
    - For each category with forecast data:
      - Gets starting inventory from INVENTORY_SNAPSHOT
      - Loops through each planning period (month)
      - Gross requirements = forecasted qty for that period
      - Projected on-hand = prior period on-hand - gross + scheduled receipts
      - Net requirements = MAX(0, gross - projected on-hand)
      - Planned order qty = net requirements rounded up to lot size
        (EOQ from PRODUCTS, or category avg if not set)
      - Planned release date = planning period minus lead time
      - Exception flags: EXPEDITE if on-hand drops below safety stock,
        RESCHEDULE if release date is in the past
  
  Prerequisites:
    - All tables from 01_schema_ddl.sql exist
    - Data loaded via 02b_data_normalization_fix.sql
    - Views from 05_reporting_views.sql exist
    - FORECAST_PLAN may be empty (procedure handles gracefully)
  
  Run: Paste entire script into a NEW clean worksheet, then F5.
================================================================================
*/


-- ============================================================================
-- 1. CREATE THE STORED PROCEDURE
-- ============================================================================

CREATE OR REPLACE PROCEDURE REFRESH_SUPPLY_CHAIN_DATA
AS
    v_start_time    TIMESTAMP := SYSTIMESTAMP;
    v_inv_count     NUMBER := 0;
    v_forecast_count NUMBER := 0;
    v_mrp_count     NUMBER := 0;
    v_category      VARCHAR2(150);
    v_period        DATE;
    v_gross_req     NUMBER(12,2);
    v_sched_rcpt    NUMBER(12,2);
    v_proj_on_hand  NUMBER(12,2);
    v_net_req       NUMBER(12,2);
    v_planned_qty   NUMBER(12,2);
    v_release_date  DATE;
    v_lot_method    VARCHAR2(20);
    v_lot_size      NUMBER(12,2);
    v_lead_time     NUMBER(5);
    v_safety_stock  NUMBER(12,2);
    v_exception     VARCHAR2(50);
    v_exc_message   VARCHAR2(500);
    v_prior_on_hand NUMBER(12,2);
    v_min_order_qty NUMBER(10);
BEGIN

    -- ========================================================================
    -- STEP 1: Refresh INVENTORY_SNAPSHOT with current calculated positions
    -- ========================================================================
    -- Recalculate inventory positions from order/shipment data.
    -- This gives MRP an up-to-date starting on-hand for each category.
    
    DELETE FROM INVENTORY_SNAPSHOT;
    
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
    
    SELECT COUNT(*) INTO v_inv_count FROM INVENTORY_SNAPSHOT;
    
    COMMIT;
    
    DBMS_OUTPUT.PUT_LINE('Step 1 complete: INVENTORY_SNAPSHOT refreshed — ' 
        || v_inv_count || ' categories');


    -- ========================================================================
    -- STEP 2: Check for forecast data
    -- ========================================================================
    SELECT COUNT(*) INTO v_forecast_count FROM FORECAST_PLAN;
    
    IF v_forecast_count = 0 THEN
        DBMS_OUTPUT.PUT_LINE('Step 2: No forecast data in FORECAST_PLAN — '
            || 'MRP calculation skipped. Load forecasts from Excel first.');
        DBMS_OUTPUT.PUT_LINE('Procedure completed at ' || TO_CHAR(SYSTIMESTAMP, 
            'YYYY-MM-DD HH24:MI:SS'));
        RETURN;  -- Exit early — nothing to calculate
    END IF;
    
    DBMS_OUTPUT.PUT_LINE('Step 2: Found ' || v_forecast_count 
        || ' forecast records — proceeding with MRP calculation');


    -- ========================================================================
    -- STEP 3: Clear previous MRP output
    -- ========================================================================
    DELETE FROM MRP_REQUIREMENTS;
    COMMIT;
    
    DBMS_OUTPUT.PUT_LINE('Step 3: MRP_REQUIREMENTS cleared');


    -- ========================================================================
    -- STEP 4: MRP Net Requirements Calculation
    -- ========================================================================
    -- Loop through each category that has forecast data.
    -- For each category, loop through each forecast period in chronological
    -- order, carrying the projected on-hand forward period to period.
    
    FOR cat_rec IN (
        SELECT DISTINCT fp.CATEGORY_NAME
        FROM FORECAST_PLAN fp
        WHERE fp.CATEGORY_NAME IN (
            SELECT CATEGORY_NAME FROM INVENTORY_SNAPSHOT
        )
        ORDER BY fp.CATEGORY_NAME
    ) LOOP
        
        v_category := cat_rec.CATEGORY_NAME;
        
        -- Get starting inventory (available qty) for this category
        BEGIN
            SELECT NVL(AVAILABLE_QTY, 0)
            INTO v_prior_on_hand
            FROM INVENTORY_SNAPSHOT
            WHERE CATEGORY_NAME = v_category
            AND ROWNUM = 1;
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                v_prior_on_hand := 0;
        END;
        
        -- Get planning parameters for this category
        -- Use the most common product in the category for lot sizing defaults
        BEGIN
            SELECT 
                NVL(MAX(LEAD_TIME_DAYS), 7),
                NVL(MAX(LOT_SIZING_METHOD), 'EOQ'),
                NVL(MAX(EOQ), 100),
                NVL(MAX(SAFETY_STOCK), 50),
                NVL(MAX(MIN_ORDER_QTY), 1)
            INTO v_lead_time, v_lot_method, v_lot_size, v_safety_stock, v_min_order_qty
            FROM PRODUCTS
            WHERE CATEGORY_NAME = v_category;
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                v_lead_time := 7;
                v_lot_method := 'EOQ';
                v_lot_size := 100;
                v_safety_stock := 50;
                v_min_order_qty := 1;
        END;
        
        -- Loop through each forecast period for this category (chronological)
        FOR period_rec IN (
            SELECT 
                FORECAST_PERIOD,
                FORECASTED_QTY
            FROM FORECAST_PLAN
            WHERE CATEGORY_NAME = v_category
            ORDER BY FORECAST_PERIOD
        ) LOOP
            
            v_period    := period_rec.FORECAST_PERIOD;
            v_gross_req := period_rec.FORECASTED_QTY;
            v_sched_rcpt := 0;  -- No scheduled receipts in simulation
            
            -- ----------------------------------------------------------------
            -- Projected On-Hand = prior on-hand - gross + scheduled receipts
            -- ----------------------------------------------------------------
            v_proj_on_hand := v_prior_on_hand - v_gross_req + v_sched_rcpt;
            
            -- ----------------------------------------------------------------
            -- Net Requirements = MAX(0, gross - prior on-hand - sched receipts)
            -- ----------------------------------------------------------------
            v_net_req := GREATEST(0, v_gross_req - v_prior_on_hand - v_sched_rcpt);
            
            -- ----------------------------------------------------------------
            -- Planned Order Quantity (apply lot sizing)
            -- ----------------------------------------------------------------
            IF v_net_req > 0 THEN
                CASE v_lot_method
                    WHEN 'EOQ' THEN
                        -- Round up to nearest EOQ multiple
                        v_planned_qty := CEIL(v_net_req / GREATEST(v_lot_size, 1)) 
                                         * GREATEST(v_lot_size, 1);
                    WHEN 'FIXED_LOT' THEN
                        -- Round up to nearest fixed lot multiple
                        v_planned_qty := CEIL(v_net_req / GREATEST(v_lot_size, 1)) 
                                         * GREATEST(v_lot_size, 1);
                    WHEN 'LOT_FOR_LOT' THEN
                        -- Order exactly what's needed
                        v_planned_qty := v_net_req;
                    ELSE
                        -- Default: round up to EOQ
                        v_planned_qty := CEIL(v_net_req / GREATEST(v_lot_size, 1)) 
                                         * GREATEST(v_lot_size, 1);
                END CASE;
                
                -- Enforce minimum order quantity
                IF v_planned_qty < v_min_order_qty THEN
                    v_planned_qty := v_min_order_qty;
                END IF;
                
                -- Recalculate projected on-hand with planned order
                v_proj_on_hand := v_proj_on_hand + v_planned_qty;
                
            ELSE
                v_planned_qty := 0;
            END IF;
            
            -- ----------------------------------------------------------------
            -- Planned Release Date = planning period minus lead time
            -- ----------------------------------------------------------------
            IF v_planned_qty > 0 THEN
                v_release_date := v_period - v_lead_time;
            ELSE
                v_release_date := NULL;
            END IF;
            
            -- ----------------------------------------------------------------
            -- Exception Flagging
            -- ----------------------------------------------------------------
            v_exception := NULL;
            v_exc_message := NULL;
            
            -- EXPEDITE: projected on-hand drops below safety stock
            IF v_proj_on_hand < v_safety_stock AND v_proj_on_hand >= 0 THEN
                v_exception := 'EXPEDITE';
                v_exc_message := 'Projected on-hand (' 
                    || ROUND(v_proj_on_hand, 0) 
                    || ') below safety stock (' 
                    || ROUND(v_safety_stock, 0) 
                    || '). Consider expediting replenishment.';
            END IF;
            
            -- STOCKOUT: projected on-hand goes negative (before planned order)
            IF (v_prior_on_hand - v_gross_req + v_sched_rcpt) < 0 
               AND v_exception IS NULL THEN
                v_exception := 'EXPEDITE';
                v_exc_message := 'Projected stockout — demand (' 
                    || ROUND(v_gross_req, 0) 
                    || ') exceeds available inventory (' 
                    || ROUND(v_prior_on_hand, 0) 
                    || '). Expedite order immediately.';
            END IF;
            
            -- RESCHEDULE: planned release date is in the past
            IF v_release_date IS NOT NULL AND v_release_date < TRUNC(SYSDATE) THEN
                v_exception := NVL(v_exception, 'RESCHEDULE');
                v_exc_message := NVL(v_exc_message, 
                    'Planned release date (' 
                    || TO_CHAR(v_release_date, 'YYYY-MM-DD') 
                    || ') is in the past. Reschedule or expedite.');
            END IF;
            
            -- ----------------------------------------------------------------
            -- Insert MRP record
            -- ----------------------------------------------------------------
            INSERT INTO MRP_REQUIREMENTS (
                CATEGORY_NAME, PLANNING_PERIOD, GROSS_REQUIREMENTS,
                SCHEDULED_RECEIPTS, PROJECTED_ON_HAND, NET_REQUIREMENTS,
                PLANNED_ORDER_QTY, PLANNED_RELEASE_DATE, LOT_SIZING_METHOD,
                EXCEPTION_FLAG, EXCEPTION_MESSAGE
            ) VALUES (
                v_category, v_period, v_gross_req,
                v_sched_rcpt, v_proj_on_hand, v_net_req,
                v_planned_qty, v_release_date, v_lot_method,
                v_exception, v_exc_message
            );
            
            -- Carry forward: this period's projected on-hand becomes next
            -- period's starting on-hand
            v_prior_on_hand := v_proj_on_hand;
            
            v_mrp_count := v_mrp_count + 1;
            
        END LOOP;  -- end period loop
        
    END LOOP;  -- end category loop
    
    COMMIT;
    
    DBMS_OUTPUT.PUT_LINE('Step 4: MRP calculation complete — ' 
        || v_mrp_count || ' planned records created');


    -- ========================================================================
    -- STEP 5: Log completion
    -- ========================================================================
    DBMS_OUTPUT.PUT_LINE('========================================');
    DBMS_OUTPUT.PUT_LINE('REFRESH_SUPPLY_CHAIN_DATA completed');
    DBMS_OUTPUT.PUT_LINE('Start:    ' || TO_CHAR(v_start_time, 'YYYY-MM-DD HH24:MI:SS'));
    DBMS_OUTPUT.PUT_LINE('End:      ' || TO_CHAR(SYSTIMESTAMP, 'YYYY-MM-DD HH24:MI:SS'));
    DBMS_OUTPUT.PUT_LINE('Inventory categories: ' || v_inv_count);
    DBMS_OUTPUT.PUT_LINE('Forecast records:     ' || v_forecast_count);
    DBMS_OUTPUT.PUT_LINE('MRP records created:  ' || v_mrp_count);
    DBMS_OUTPUT.PUT_LINE('========================================');

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('ERROR in REFRESH_SUPPLY_CHAIN_DATA: ' || SQLERRM);
        RAISE;
END REFRESH_SUPPLY_CHAIN_DATA;
/


-- ============================================================================
-- 2. VERIFY PROCEDURE COMPILED SUCCESSFULLY
-- ============================================================================
SELECT 
    OBJECT_NAME, 
    OBJECT_TYPE, 
    STATUS,
    CREATED
FROM USER_OBJECTS
WHERE OBJECT_NAME = 'REFRESH_SUPPLY_CHAIN_DATA'
AND OBJECT_TYPE = 'PROCEDURE';


-- ============================================================================
-- 3. TEST EXECUTION (should complete with "MRP calculation skipped" since
--    FORECAST_PLAN is empty — this is expected)
-- ============================================================================
SET SERVEROUTPUT ON;

BEGIN
    REFRESH_SUPPLY_CHAIN_DATA;
END;
/


-- ============================================================================
-- 4. VERIFY: Check tables after procedure run
-- ============================================================================
SELECT 'INVENTORY_SNAPSHOT' AS TBL, COUNT(*) AS CNT FROM INVENTORY_SNAPSHOT
UNION ALL SELECT 'FORECAST_PLAN', COUNT(*) FROM FORECAST_PLAN
UNION ALL SELECT 'MRP_REQUIREMENTS', COUNT(*) FROM MRP_REQUIREMENTS;


-- ============================================================================
-- 5. CREATE DBMS_SCHEDULER JOB (nightly at 2:00 AM)
-- ============================================================================
-- Drop existing job if re-running
BEGIN
    DBMS_SCHEDULER.DROP_JOB(
        job_name => 'JOB_REFRESH_SUPPLY_CHAIN',
        force    => TRUE
    );
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    DBMS_SCHEDULER.CREATE_JOB(
        job_name        => 'JOB_REFRESH_SUPPLY_CHAIN',
        job_type        => 'STORED_PROCEDURE',
        job_action      => 'REFRESH_SUPPLY_CHAIN_DATA',
        start_date      => TRUNC(SYSDATE + 1) + INTERVAL '2' HOUR,  -- Next day 2:00 AM
        repeat_interval => 'FREQ=DAILY; BYHOUR=2; BYMINUTE=0; BYSECOND=0',
        enabled         => TRUE,
        auto_drop       => FALSE,
        comments        => 'Nightly refresh: inventory snapshot recalculation, '
                        || 'MRP net requirements calculation, and reporting view '
                        || 'data update. Runs at 2:00 AM daily.'
    );
END;
/


-- ============================================================================
-- 6. VERIFY SCHEDULER JOB
-- ============================================================================
SELECT 
    JOB_NAME,
    JOB_TYPE,
    STATE,
    ENABLED,
    REPEAT_INTERVAL,
    NEXT_RUN_DATE,
    COMMENTS
FROM USER_SCHEDULER_JOBS
WHERE JOB_NAME = 'JOB_REFRESH_SUPPLY_CHAIN';


-- ============================================================================
-- 7. SUMMARY VERIFICATION
-- ============================================================================
SELECT 'Stored Procedure' AS OBJECT, OBJECT_NAME, STATUS 
FROM USER_OBJECTS 
WHERE OBJECT_NAME = 'REFRESH_SUPPLY_CHAIN_DATA' AND OBJECT_TYPE = 'PROCEDURE'
UNION ALL
SELECT 'Scheduler Job', JOB_NAME, STATE 
FROM USER_SCHEDULER_JOBS 
WHERE JOB_NAME = 'JOB_REFRESH_SUPPLY_CHAIN';