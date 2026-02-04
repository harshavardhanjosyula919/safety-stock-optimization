"""
Safety Stock Optimization Calculator
"""

import pandas as pd
import numpy as np
import json


class SafetyStockOptimizer:
    """Calculates optimal safety stock levels and financial impact."""

    def __init__(self, service_level: float = 0.95, carrying_cost_rate: float = 0.25):
        self.service_level = service_level
        self.carrying_cost_rate = carrying_cost_rate

    def calculate_annual_carrying_cost(self, safety_stock_units: float, unit_cost: float) -> float:
        """Calculate annual cost to hold safety stock."""
        inventory_value = safety_stock_units * unit_cost
        return inventory_value * self.carrying_cost_rate

    def calculate_stockout_cost(self, stockout_rate: float, annual_revenue: float, 
                               gross_margin: float = 0.30) -> float:
        """Estimate annual stockout cost."""
        lost_revenue = annual_revenue * stockout_rate
        return lost_revenue * gross_margin

    def optimize_sku(self, row: pd.Series) -> dict:
        """Calculate before/after scenarios for a single SKU."""
        current_units = row["current_safety_stock_units"]
        current_value = current_units * row["unit_cost"]
        current_carrying = self.calculate_annual_carrying_cost(current_units, row["unit_cost"])
        current_stockout = self.calculate_stockout_cost(row["stockout_rate"], row["revenue_annual"])

        rec_weeks = row["recommended_safety_stock_weeks"]
        rec_units = rec_weeks * row["avg_weekly_demand"]
        rec_value = rec_units * row["unit_cost"]
        rec_carrying = self.calculate_annual_carrying_cost(rec_units, row["unit_cost"])

        cv = row["demand_volatility_cv"]
        if cv > 0.40:
            stockout_reduction = (rec_weeks - 2.0) * 0.03
            new_stockout_rate = max(0.028, row["stockout_rate"] - stockout_reduction)
        else:
            new_stockout_rate = row["stockout_rate"] * 0.7

        rec_stockout = self.calculate_stockout_cost(new_stockout_rate, row["revenue_annual"])

        return {
            "current_safety_stock_value": current_value,
            "recommended_safety_stock_value": rec_value,
            "inventory_value_change": rec_value - current_value,
            "carrying_cost_change": rec_carrying - current_carrying,
            "stockout_cost_change": rec_stockout - current_stockout,
            "net_benefit": (current_carrying - rec_carrying) + (current_stockout - rec_stockout),
            "projected_stockout_rate": new_stockout_rate
        }

    def calculate_portfolio_impact(self, df: pd.DataFrame):
        """Calculate optimization impact across entire portfolio."""
        results = []

        for _, row in df.iterrows():
            optimization = self.optimize_sku(row)
            combined = {**row.to_dict(), **optimization}
            results.append(combined)

        results_df = pd.DataFrame(results)

        summary = {
            "total_skus": len(results_df),
            "current_inventory_value": results_df["current_safety_stock_value"].sum(),
            "recommended_inventory_value": results_df["recommended_safety_stock_value"].sum(),
            "inventory_reduction": results_df["inventory_value_change"].sum(),
            "carrying_cost_savings": -results_df["carrying_cost_change"].sum(),
            "stockout_cost_savings": -results_df["stockout_cost_change"].sum(),
            "net_annual_benefit": results_df["net_benefit"].sum(),
            "avg_stockout_rate_before": results_df["stockout_rate"].mean(),
            "avg_stockout_rate_after": results_df["projected_stockout_rate"].mean()
        }

        return results_df, summary


def main():
    """Calculate financial impact."""
    df = pd.read_csv("../data/sample_inventory_data.csv")

    optimizer = SafetyStockOptimizer(service_level=0.95)
    results, summary = optimizer.calculate_portfolio_impact(df)

    print("=" * 60)
    print("SAFETY STOCK OPTIMIZATION: FINANCIAL IMPACT")
    print("=" * 60)
    print(f"\nPortfolio Overview:")
    print(f"  Total SKUs: {summary["total_skus"]:,}")
    print(f"\nInventory Value:")
    print(f"  Before: ${summary["current_inventory_value"]:,.0f}")
    print(f"  After:  ${summary["recommended_inventory_value"]:,.0f}")
    print(f"  Reduction: ${summary["inventory_reduction"]:,.0f}")
    print(f"\nAnnual Benefit:")
    print(f"  Net Annual Benefit: ${summary["net_annual_benefit"]:,.0f}")
    print(f"\nService Levels:")
    print(f"  Avg Stockout Rate: {summary["avg_stockout_rate_before"]*100:.1f}% → {summary["avg_stockout_rate_after"]*100:.1f}%")

    results.to_csv("../data/optimization_results.csv", index=False)
    with open("../data/financial_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)

    print("\nOptimization complete. Results saved.")


if __name__ == "__main__":
    main()
