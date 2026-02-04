-- ============================================================================
-- SKU SEGMENTATION: REVENUE + VOLATILITY QUADRANTS
-- ============================================================================

CREATE OR REPLACE VIEW vw_sku_segments AS
WITH revenue_percentiles AS (
    SELECT 
        sku_id,
        annual_revenue,
        demand_volatility_cv,
        volatility_class,
        current_safety_stock_weeks,
        current_safety_stock_value,
        NTILE(10) OVER (ORDER BY annual_revenue DESC) as revenue_decile
    FROM vw_volatility_metrics
)

SELECT 
    rp.sku_id,
    rp.annual_revenue,
    rp.demand_volatility_cv,
    rp.volatility_class,
    rp.current_safety_stock_weeks,
    rp.current_safety_stock_value,
    CASE 
        WHEN rp.revenue_decile <= 3 AND rp.demand_volatility_cv > 0.40 
        THEN 'High Revenue + High Volatility'
        WHEN rp.revenue_decile <= 3 AND rp.demand_volatility_cv <= 0.40 
        THEN 'High Revenue + Low Volatility'
        WHEN rp.revenue_decile > 3 AND rp.demand_volatility_cv > 0.40 
        THEN 'Low Revenue + High Volatility'
        ELSE 'Low Revenue + Low Volatility'
    END as segment,
    CASE 
        WHEN rp.revenue_decile <= 3 AND rp.demand_volatility_cv > 0.40 THEN 1
        WHEN rp.revenue_decile <= 3 AND rp.demand_volatility_cv <= 0.40 THEN 2
        WHEN rp.revenue_decile > 3 AND rp.demand_volatility_cv > 0.40 THEN 3
        ELSE 4
    END as segment_priority,
    CASE 
        WHEN rp.revenue_decile <= 3 AND rp.demand_volatility_cv > 0.40 THEN 3.5
        WHEN rp.revenue_decile <= 3 AND rp.demand_volatility_cv <= 0.40 THEN 1.5
        WHEN rp.revenue_decile > 3 AND rp.demand_volatility_cv > 0.40 THEN 2.0
        ELSE 1.0
    END as recommended_safety_stock_weeks
FROM revenue_percentiles rp;

-- Segment summary (matches artifact exactly)
SELECT 
    segment,
    COUNT(*) as sku_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 0) as sku_pct,
    ROUND(SUM(annual_revenue), 0) as total_revenue,
    ROUND(SUM(annual_revenue) * 100.0 / SUM(SUM(annual_revenue)) OVER(), 0) as revenue_share,
    ROUND(AVG(recommended_safety_stock_weeks), 1) as recommended_weeks
FROM vw_sku_segments
GROUP BY segment
ORDER BY segment_priority;