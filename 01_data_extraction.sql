-- ============================================================================
-- SAFETY STOCK OPTIMIZATION: DATA EXTRACTION
-- Author: Sri Harshavardhan Josyula
-- Date: Q1 2025
-- Description: Base data extraction for 24-month demand history
-- ============================================================================

-- Create base view for demand history
CREATE OR REPLACE VIEW vw_demand_history AS
SELECT 
    sku_id,
    product_name,
    category,
    unit_cost,
    week_1_demand, week_2_demand, week_3_demand,
    lead_time_weeks,
    current_safety_stock_weeks,
    service_level_target,
    updated_at
FROM raw_inventory_data
WHERE status = 'ACTIVE'
  AND updated_at >= CURRENT_DATE - INTERVAL '24 months';

-- Extract summary statistics by SKU
CREATE OR REPLACE VIEW vw_demand_summary AS
SELECT 
    sku_id,
    product_name,
    category,
    unit_cost,
    AVG(weekly_demand) as avg_weekly_demand,
    STDDEV(weekly_demand) as stddev_weekly_demand,
    COUNT(weekly_demand) as data_points,
    (AVG(weekly_demand) * 52 * unit_cost) as annual_revenue,
    current_safety_stock_weeks,
    (AVG(weekly_demand) * current_safety_stock_weeks) as current_safety_stock_units,
    (AVG(weekly_demand) * current_safety_stock_weeks * unit_cost) as current_safety_stock_value
FROM (
    SELECT 
        sku_id, product_name, category, unit_cost,
        UNNEST(ARRAY[week_1_demand, week_2_demand, week_3_demand]) as weekly_demand,
        lead_time_weeks, current_safety_stock_weeks
    FROM vw_demand_history
) demand_unpivot
GROUP BY sku_id, product_name, category, unit_cost, current_safety_stock_weeks;

-- Data quality check
SELECT 
    'Total SKUs' as metric, COUNT(*) as value
FROM vw_demand_summary
UNION ALL
SELECT 
    'SKUs with < 52 weeks data', COUNT(*)
FROM vw_demand_summary 
WHERE data_points < 52;