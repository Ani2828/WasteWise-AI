from prediction_engine import optimize_meal_preparation


result = optimize_meal_preparation(
    expected_attendance=420,
    previous_day_waste=7.2,
    avg_7day_waste=6.8,
    temperature=28,
    portion_size=100,
    event=0,
    holiday=0,
    day_of_week=2,
    meal_type="Lunch",
    menu_category="Rice-Based",
    current_meals_prepared=450
)


print("\n========================================")
print("       WASTEWISE AI OPTIMIZER")
print("========================================")

print(
    f"\nCurrent preparation : "
    f"{result['current_meals']} meals"
)

print(
    f"Current waste       : "
    f"{result['current_waste']} kg"
)

print(
    f"\nAI recommended      : "
    f"{result['recommended_meals']} meals"
)

print(
    f"Optimized waste     : "
    f"{result['optimized_waste']} kg"
)

print(
    f"\nWaste reduction     : "
    f"{result['waste_reduction']} kg"
)

print(
    f"Reduction           : "
    f"{result['reduction_percentage']}%"
)

print("\n========================================")