from simulator import (
    simulate_scenario,
    compare_scenarios
)


# =========================================
# COMMON CONDITIONS
# =========================================

common_inputs = {
    "expected_attendance": 420,
    "previous_day_waste": 7.2,
    "avg_7day_waste": 6.8,
    "temperature": 28,
    "portion_size": 100,
    "event": 0,
    "holiday": 0,
    "day_of_week": 2,
    "meal_type": "Lunch",
    "menu_category": "Rice-Based"
}


# =========================================
# BASELINE SCENARIO
# =========================================

baseline = simulate_scenario(
    meals_prepared=450,
    **common_inputs
)


# =========================================
# OPTIMIZED SCENARIO
# =========================================

optimized = simulate_scenario(
    meals_prepared=433,
    **common_inputs
)


# =========================================
# COMPARISON
# =========================================

comparison = compare_scenarios(
    baseline,
    optimized
)


# =========================================
# DISPLAY
# =========================================

print("\n========================================")
print("        WASTEWISE WHAT-IF SIMULATOR")
print("========================================")

print("\nBASELINE")
print("----------------------------------------")
print(
    f"Meals prepared : "
    f"{baseline['meals_prepared']}"
)
print(
    f"Predicted waste: "
    f"{baseline['predicted_waste']} kg"
)


print("\nOPTIMIZED")
print("----------------------------------------")
print(
    f"Meals prepared : "
    f"{optimized['meals_prepared']}"
)
print(
    f"Predicted waste: "
    f"{optimized['predicted_waste']} kg"
)


print("\nIMPACT")
print("----------------------------------------")
print(
    f"Waste reduction : "
    f"{comparison['waste_reduction_kg']} kg"
)
print(
    f"Reduction       : "
    f"{comparison['reduction_percentage']}%"
)

print("\n========================================")