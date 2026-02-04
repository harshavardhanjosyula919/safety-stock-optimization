"""
Demand Analysis Module
Calculates volatility metrics (CV, MAD, std dev)
Author: Sri Harshavardhan Josyula
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class DemandAnalyzer:
    """Analyzes demand patterns and calculates volatility metrics."""

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.metrics = None

    def calculate_cv(self, demand_series: pd.Series) -> float:
        """Calculate Coefficient of Variation = StdDev / Mean"""
        mean_demand = demand_series.mean()
        std_demand = demand_series.std()
        if mean_demand == 0:
            return np.nan
        return std_demand / mean_demand

    def analyze_all_skus(self) -> pd.DataFrame:
        """Calculate volatility metrics for all SKUs."""
        results = []

        for sku_id in self.data["sku_id"].unique():
            sku_data = self.data[self.data["sku_id"] == sku_id].copy()
            demand_series = sku_data["demand"]

            metrics = {
                "sku_id": sku_id,
                "avg_weekly_demand": demand_series.mean(),
                "stddev_demand": demand_series.std(),
                "cv_demand": self.calculate_cv(demand_series),
                "min_demand": demand_series.min(),
                "max_demand": demand_series.max(),
                "total_demand": demand_series.sum()
            }

            cv = metrics["cv_demand"]
            if pd.isna(cv):
                metrics["volatility_class"] = "INSUFFICIENT_DATA"
            elif cv > 0.40:
                metrics["volatility_class"] = "HIGH_VOLATILITY"
            elif cv > 0.20:
                metrics["volatility_class"] = "MEDIUM_VOLATILITY"
            else:
                metrics["volatility_class"] = "LOW_VOLATILITY"

            results.append(metrics)

        self.metrics = pd.DataFrame(results)
        return self.metrics

    def plot_volatility_distribution(self, save_path: str = None):
        """Create visualization of CV distribution."""
        if self.metrics is None:
            self.analyze_all_skus()

        plt.figure(figsize=(10, 6))
        sns.histplot(self.metrics["cv_demand"].dropna(), bins=30, kde=True, color="steelblue")
        plt.axvline(x=0.40, color="red", linestyle="--", label="High Volatility (40%)")
        plt.axvline(x=0.20, color="orange", linestyle="--", label="Medium Volatility (20%)")
        plt.xlabel("Coefficient of Variation (CV)")
        plt.ylabel("Count of SKUs")
        plt.title("Demand Volatility Distribution")
        plt.legend()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.show()


def main():
    """Example usage."""
    df = pd.read_csv("../data/sample_inventory_data.csv")

    np.random.seed(42)
    demand_records = []

    for _, row in df.head(100).iterrows():
        base_demand = row["avg_weekly_demand"]
        cv = row["demand_volatility_cv"]

        for week in range(1, 25):
            noise = np.random.normal(0, base_demand * cv)
            demand = max(0, base_demand + noise)
            demand_records.append({
                "sku_id": row["sku_id"],
                "week": week,
                "demand": demand
            })

    demand_df = pd.DataFrame(demand_records)

    analyzer = DemandAnalyzer(demand_df)
    metrics = analyzer.analyze_all_skus()

    print("Volatility Analysis Summary:")
    print(metrics["volatility_class"].value_counts())

    metrics.to_csv("../data/demand_volatility_metrics.csv", index=False)
    print("\nResults saved to demand_volatility_metrics.csv")


if __name__ == "__main__":
    main()
