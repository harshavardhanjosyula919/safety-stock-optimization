"""
SKU Segmentation Model
Revenue + Volatility Quadrant Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Segmenter:
    """Segments SKUs into 4 quadrants based on Revenue and CV."""

    def __init__(self, cv_threshold: float = 0.40):
        self.cv_threshold = cv_threshold
        self.revenue_threshold_high = None

    def fit(self, df: pd.DataFrame):
        """Calculate revenue thresholds."""
        self.revenue_threshold_high = df["revenue_annual"].quantile(0.70)
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply segmentation logic."""
        df = df.copy()

        df["revenue_class"] = np.where(
            df["revenue_annual"] >= self.revenue_threshold_high,
            "High Revenue", "Low Revenue"
        )

        df["volatility_class"] = np.where(
            df["demand_volatility_cv"] > self.cv_threshold,
            "High Volatility", "Low Volatility"
        )

        conditions = [
            (df["revenue_class"] == "High Revenue") & (df["volatility_class"] == "High Volatility"),
            (df["revenue_class"] == "High Revenue") & (df["volatility_class"] == "Low Volatility"),
            (df["revenue_class"] == "Low Revenue") & (df["volatility_class"] == "High Volatility")
        ]
        choices = [
            "High Revenue + High Volatility",
            "High Revenue + Low Volatility",
            "Low Revenue + High Volatility"
        ]
        df["segment"] = np.select(conditions, choices, default="Low Revenue + Low Volatility")

        safety_map = {
            "High Revenue + High Volatility": 3.5,
            "High Revenue + Low Volatility": 1.5,
            "Low Revenue + High Volatility": 2.0,
            "Low Revenue + Low Volatility": 1.0
        }
        df["recommended_safety_stock_weeks"] = df["segment"].map(safety_map)

        return df

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.fit(df).transform(df)

    def get_summary_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate summary matching the artifact."""
        summary = df.groupby("segment").agg({
            "sku_id": "count",
            "revenue_annual": ["sum", "mean"],
            "demand_volatility_cv": "mean",
            "stockout_rate": "mean"
        }).round(2)

        summary.columns = ["sku_count", "total_revenue", "avg_revenue", "avg_cv", "avg_stockout_rate"]
        summary["sku_pct"] = (summary["sku_count"] / summary["sku_count"].sum() * 100).round(0)
        summary["revenue_share"] = (summary["total_revenue"] / summary["total_revenue"].sum() * 100).round(0)

        safety_map = {
            "High Revenue + High Volatility": 3.5,
            "High Revenue + Low Volatility": 1.5,
            "Low Revenue + High Volatility": 2.0,
            "Low Revenue + Low Volatility": 1.0
        }
        summary["recommended_weeks"] = summary.index.map(safety_map)

        return summary


def main():
    """Run segmentation."""
    df = pd.read_csv("../data/sample_inventory_data.csv")

    model = Segmenter(cv_threshold=0.40)
    segmented_df = model.fit_transform(df)

    summary = model.get_summary_stats(segmented_df)
    print("Segmentation Summary:")
    print(summary)

    segmented_df.to_csv("../data/sku_segments.csv", index=False)
    print("\nSegmentation complete. Saved to sku_segments.csv")


if __name__ == "__main__":
    main()
