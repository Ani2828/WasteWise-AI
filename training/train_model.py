import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# =========================
# 1. LOAD DATA
# =========================

df = pd.read_csv("data/cafeteria_waste.csv")

print("Dataset loaded successfully!")
print(f"Dataset shape: {df.shape}")


# =========================
# 2. FEATURES & TARGET
# =========================

X = df.drop(columns=["date", "waste_kg"])
y = df["waste_kg"]


# =========================
# 3. FEATURE TYPES
# =========================

categorical_features = [
    "meal_type",
    "menu_category"
]

numerical_features = [
    "expected_attendance",
    "meals_prepared",
    "previous_day_waste",
    "avg_7day_waste",
    "temperature",
    "portion_size",
    "event",
    "holiday",
    "day_of_week"
]


# =========================
# 4. PREPROCESSING
# =========================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)


# =========================
# 5. RANDOM FOREST
# =========================

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)


# =========================
# 6. COMPLETE PIPELINE
# =========================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# =========================
# 7. TRAIN / TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")


# =========================
# 8. TRAIN MODEL
# =========================

print("\nTraining Random Forest...")

pipeline.fit(X_train, y_train)

print("Training completed!")


# =========================
# 9. PREDICTION
# =========================

predictions = pipeline.predict(X_test)


# =========================
# 10. EVALUATION
# =========================

mae = mean_absolute_error(y_test, predictions)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)


print("\n======================================")
print("       WASTEWISE AI MODEL")
print("======================================")

print(f"MAE  : {mae:.3f} kg")
print(f"RMSE : {rmse:.3f} kg")
print(f"R²   : {r2:.3f}")

print("======================================")


# =========================
# 11. SAVE MODEL
# =========================

joblib.dump(
    pipeline,
    "models/waste_prediction_model.pkl"
)

print("\nModel saved successfully!")
print("Location: models/waste_prediction_model.pkl")