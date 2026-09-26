from prediction_engine import (
    predict_waste,
    generate_recommendation
)


# Example cafeteria scenario

expected_attendance = 420
meals_prepared = 450

predicted_waste = predict_waste(
    expected_attendance=expected_attendance,
    meals_prepared=meals_prepared,
    previous_day_waste=7.2,
    avg_7day_waste=6.8,
    temperature=28,
    portion_size=100,
    event=0,
    holiday=0,
    day_of_week=2,
    meal_type="Lunch",
    menu_category="Rice-Based"
)


recommendation = generate_recommendation(
    expected_attendance,
    meals_prepared,
    predicted_waste,
    "Rice-Based"
)


print("\n===================================")
print("        WASTEWISE AI")
print("===================================")

print(
    f"\nExpected attendance : "
    f"{expected_attendance}"
)

print(
    f"Meals prepared      : "
    f"{meals_prepared}"
)

print(
    f"Predicted waste     : "
    f"{predicted_waste:.2f} kg"
)

print(
    f"\nWaste risk          : "
    f"{recommendation['risk']}"
)

print(
    f"Preparation gap     : "
    f"{recommendation['preparation_gap']} meals"
)

print(
    f"Recommended meals   : "
    f"{recommendation['recommended_meals']}"
)

print(
    f"\nAI Recommendation:\n"
    f"{recommendation['action']}"
)

print("\n===================================")