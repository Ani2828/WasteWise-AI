from prediction_engine import predict_waste


def simulate_scenario(
    expected_attendance,
    meals_prepared,
    previous_day_waste,
    avg_7day_waste,
    temperature,
    portion_size,
    event,
    holiday,
    day_of_week,
    meal_type,
    menu_category
):
    """
    Simulate expected waste for a specific
    meal-preparation scenario.
    """

    predicted_waste = predict_waste(
        expected_attendance=expected_attendance,
        meals_prepared=meals_prepared,
        previous_day_waste=previous_day_waste,
        avg_7day_waste=avg_7day_waste,
        temperature=temperature,
        portion_size=portion_size,
        event=event,
        holiday=holiday,
        day_of_week=day_of_week,
        meal_type=meal_type,
        menu_category=menu_category
    )

    return {
        "meals_prepared": meals_prepared,
        "predicted_waste": round(predicted_waste, 2)
    }


def compare_scenarios(
    baseline,
    optimized
):
    """
    Compare baseline and optimized scenarios.
    """

    waste_reduction = (
        baseline["predicted_waste"]
        - optimized["predicted_waste"]
    )

    if baseline["predicted_waste"] > 0:
        reduction_percentage = (
            waste_reduction
            / baseline["predicted_waste"]
        ) * 100
    else:
        reduction_percentage = 0

    return {
        "waste_reduction_kg": round(
            waste_reduction,
            2
        ),
        "reduction_percentage": round(
            reduction_percentage,
            1
        )
    }