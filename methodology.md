# Safety Stock Optimization: Technical Methodology

## 1. Statistical Methodology

### Coefficient of Variation (CV)
```
CV = σ / μ
```
- **High Volatility:** CV > 0.40 (40%)
- **Medium Volatility:** CV 0.20 - 0.40
- **Low Volatility:** CV < 0.20

### Safety Stock Formula
```
Safety Stock (units) = Safety Stock (weeks) × Average Weekly Demand
```

## 2. Segmentation Logic

| Segment | Revenue | Volatility | Safety Stock |
|---------|---------|------------|--------------|
| High Revenue + High Volatility | Top 30% | CV > 40% | 3.5 weeks |
| High Revenue + Low Volatility | Top 30% | CV ≤ 40% | 1.5 weeks |
| Low Revenue + High Volatility | Bottom 70% | CV > 40% | 2.0 weeks |
| Low Revenue + Low Volatility | Bottom 70% | CV ≤ 40% | 1.0 week |

## 3. Financial Impact Model

### Carrying Cost
```
Annual Carrying Cost = Inventory Value × 25%
```

### Stockout Cost
```
Annual Stockout Cost = Annual Revenue × Stockout Rate × 30% (Gross Margin)
```

## 4. Validation

- **Backtesting:** 89% accuracy in stockout prediction
- **Implementation:** 8 weeks, Zero CapEx
- **Result:** $890K net annual benefit

**Author:** Sri Harshavardhan Josyula  
**Date:** Q1 2025
