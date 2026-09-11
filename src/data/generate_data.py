"""Module for generating synthetic dataset for pharmaceutical demand forecasting."""

import logging
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# Configure logging to MLOps standard output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def build_pharma_dataset(
    days: int = 365, num_products: int = 10, seed: int = 42
) -> pd.DataFrame:
    """Generate historical daily demand and stock levels for supply chain."""
    np.random.seed(seed)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    dates = [
        start_date + timedelta(days=d) for d in range(days)
    ]
    products = [
        f"MED_{i + 1:03d}" for i in range(num_products)
    ]

    rows = []

    for product in products:
        base_demand = np.random.randint(40, 180)
        current_stock = np.random.randint(600, 1800)

        for current_date in dates:
            # Winter seasonal spike (higher pharmaceutical demand)
            is_winter = current_date.month in [11, 12, 1, 2]
            seasonality = 1.25 if is_winter else 1.0

            # Weekend effect (lower order volumes)
            is_weekend = current_date.weekday() >= 5
            weekend_scale = 0.55 if is_weekend else 1.0

            # Compute final daily demand
            raw_demand = (
                np.random.normal(base_demand, 12)
                * seasonality
                * weekend_scale
            )
            demand = max(0, int(raw_demand))

            # Check stockout status and fulfill sales
            is_stockout = int(current_stock < demand)
            fulfilled_sales = min(current_stock, demand)
            current_stock -= fulfilled_sales

            # Automatic replenishment trigger
            if current_stock < 250:
                current_stock += np.random.randint(400, 900)

            rows.append(
                {
                    "date": current_date.strftime(
                        "%Y-%m-%d"
                    ),
                    "product_id": product,
                    "target_demand": demand,
                    "sales_volume": fulfilled_sales,
                    "stock_on_hand": current_stock,
                    "is_stockout": is_stockout,
                    "supplier_lead_time": int(
                        np.random.choice(
                            [2, 3, 5, 7],
                            p=[0.5, 0.3, 0.15, 0.05],
                        )
                    ),
                }
            )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    logging.info(
        "Generating synthetic pharmaceutical dataset..."
    )
    df_pharma = build_pharma_dataset()

    output_file = "src/data/pharmaceutical_demand.csv"
    df_pharma.to_csv(output_file, index=False)
    logging.info(
        f"Dataset generated successfully ({len(df_pharma)} rows) -> {output_file}"
    )
