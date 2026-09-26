import numpy as np
import pandas as pd

np.random.seed(42)

N = 2000

dates = pd.date_range(start="2024-01-01", periods=N, freq="D")

df = pd.DataFrame({
    "date": dates,
    "expected_attendance": np.random.randint(200, 601, N),
    "meals_prepared": np.random.randint(220, 650, N),
    "previous_day_waste": np.random.uniform(2, 20, N),
    "avg_7day_waste": np.random.uniform(3, 18, N),
    "temperature": np.random.uniform(18, 35, N),
    "portion_size": np.random.uniform(85, 115, N),
    "event": np.random.choice([0, 1], N, p=[0.85, 0.15]),
    "holiday": np.random.choice([0, 1], N, p=[0.9, 0.1]),
})

df["day_of_week"] = df["date"].dt.dayofweek

df["meal_type"] = np.random.choice(
    ["Breakfast", "Lunch", "Dinner"],
    N,
    p=[0.2, 0.5, 0.3]
)

df["menu_category"] = np.random.choice(
    ["Rice-Based", "Roti-Based", "Mixed", "Light Meal"],
    N
)

# Base waste calculation
base_waste = (
    0.035 * df["meals_prepared"]
    - 0.025 * df["expected_attendance"]
    + 0.30 * df["previous_day_waste"]
    + 0.20 * df["avg_7day_waste"]
    + 0.04 * (df["portion_size"] - 100)
    + 1.5 * df["event"]
    + 1.0 * df["holiday"]
)

# Menu effects
menu_effect = {
    "Rice-Based": 2.0,
    "Roti-Based": 1.0,
    "Mixed": 1.5,
    "Light Meal": 0.5
}

df["waste_kg"] = (
    base_waste
    + df["menu_category"].map(menu_effect)
    + np.random.normal(0, 1.5, N)
)

df["waste_kg"] = df["waste_kg"].clip(lower=0.5)

df.to_csv("data/cafeteria_waste.csv", index=False)

print("Dataset created successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print("\nFirst 5 rows:")
print(df.head())