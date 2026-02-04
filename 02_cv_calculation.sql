-- ============================================================================
-- COEFFICIENT OF VARIATION (CV) CALCULATION
-- Description: Calculate demand volatility metrics
-- ============================================================================

CREATE OR REPLACE VIEW vw_volatility_metrics AS
WITH weekly_stats AS (
    SELECT 
        sku_id,
        AVG(weekly_demand) as mean_demand,
        STDDEV(weekly_demand) as stddev_demand,
        CASE 
            WHEN AVG(weekly_demand) > 0 
            THEN STDDEV(weekly_demand) / AVG(weekly_demand)
            ELSE NULL 
        END as cv_demand,
        MIN(weekly_demand) as min_demand,
        MAX(weekly_demand) as max_demand
    FROM (
        SELECT sku_id, UNNEST(ARRAY[week_1_demand, week_2_demand, week_3_demand]) as weekly_demand
        FROM vw_demand_history
    ) weekly_data
    GROUP BY sku_id
)

SELECT 
    ds.sku_id,
    ds.product_name,
    ds.category,
    ds.unit_cost,
    ds.avg_weekly_demand,
    ds.annual_revenue,
    ws.cv_demand as demand_volatility_cv,
    ws.stddev_demand,
    CASE 
        WHEN ws.cv_demand > 0.40 THEN 'HIGH_VOLATILITY'
        WHEN ws.cv_demand > 0.20 THEN 'MEDIUM_VOLATILITY'
        ELSE 'LOW_VOLATILITY'
    END as volatility_class,
    LEAST(100, ROUND((ws.cv_demand * 100), 0)) as volatility_risk_score,
    ds.current_safety_stock_weeks,
    ds.current_safety_stock_units,
    ds.current_safety_stock_value
FROM vw_demand_summary ds
LEFT JOIN weekly_stats ws ON ds.sku_id = ws.sku_id
WHERE ws.cv_demand IS NOT NULL;

-- Volatility distribution summary
SELECT 
    volatility_class,
    COUNT(*) as sku_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as pct_of_total,
    ROUND(SUM(annual_revenue), 0) as total_revenue,
    ROUND(AVG(demand_volatility_cv), 2) as avg_cv
FROM vw_volatility_metrics
GROUP BY volatility_class
ORDER BY avg_cv DESC;