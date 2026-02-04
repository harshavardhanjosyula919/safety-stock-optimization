# Safety Stock Optimization Model

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-PostgreSQL%2FMySQL-orange)](https://www.postgresql.org/)

## Overview

This project implements a **segmented safety stock optimization model** that dynamically adjusts inventory buffers based on demand volatility (CV) and revenue contribution.

**Business Impact:**
- 📉 Stockout rate reduced by **66%** (8.2% → 2.8%)
- 💰 Working capital freed: **$720K** (48% reduction)
- 📦 Expedited freight savings: **$255K** annually

## The Problem

Traditional uniform safety stock policies ignore demand variability:
- **25% of SKUs** had demand volatility >40% CV but received same buffer as stable SKUs
- **10% of SKUs** caused **67%** of stockout costs
- **55% of SKUs** were over-protected, tying up capital

## The Solution

**Segmented Safety Stock Policy:**

| Segment | SKU Count | Revenue Share | Safety Stock | Rationale |
|---------|-----------|---------------|--------------|-----------|
| High Revenue + High Volatility | 420 (10%) | 35% | 3.5 weeks | Cannot afford stockouts |
| High Revenue + Low Volatility | 840 (20%) | 45% | 1.5 weeks | Stable = reduce buffer |
| Low Revenue + High Volatility | 630 (15%) | 12% | 2.0 weeks | Balance investment |
| Low Revenue + Low Volatility | 2,310 (55%) | 8% | 1.0 week | Minimal protection |

## Project Structure

```
├── data/
│   └── sample_inventory_data.csv    # Synthetic 4,200 SKU dataset
├── sql/
│   ├── 01_data_extraction.sql       # Base queries
│   ├── 02_cv_calculation.sql        # Volatility metrics
│   └── 03_segmentation.sql          # Quadrant assignment
├── python/
│   ├── demand_analysis.py           # CV analysis & trends
│   ├── segmentation_model.py        # Revenue + CV quadrants
│   └── safety_stock_calc.py         # Dynamic buffer calculation
└── docs/
    └── methodology.md               # Detailed technical docs
```

## Quick Start

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn scipy
```

### Run the Model
```bash
# 1. Analyze demand volatility
cd python
python demand_analysis.py

# 2. Run segmentation
python segmentation_model.py

# 3. Calculate financial impact
python safety_stock_calc.py
```

## Key Features

- **SQL Analytics:** 24-month rolling CV calculation using window functions
- **Python Modeling:** Statistical volatility analysis + Monte Carlo simulation
- **Excel Automation:** Power Query connection + VBA macros for weekly refresh

## Results Validation

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Stockout Rate (Volatile SKUs) | 8.2% | 2.8% | -66% |
| Excess Inventory | $1.5M | $780K | -48% |
| Expedited Freight | $340K | $85K | -75% |


## 📄 Executive Summary

View the full case study: [Tradeoff Analysis (PDF)](reports/Tradeoff%20Analysis%3A%20Safety%20Stock%20Optimization.pdf)
Or view the analysis in the `reports/` folder.

## Contact

**Sri Harshavardhan Josyula**  
Business Analyst | Supply Chain Operations  
📧 harshajosyula75@gmail.com | 📱 (945) 393-9565  
🔗 [LinkedIn](https://linkedin.com/in/harshajosyula)

**Confidentiality Note:** This repository contains synthetic data and reconstructed methodology. All proprietary information has been anonymized.
