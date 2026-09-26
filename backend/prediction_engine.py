import joblib
import pandas as pd


MODEL_PATH = "models/waste_prediction_model.pkl"


# Load trained model once
model = joblib.load(MODEL_PATH)


def predict_waste(
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
    Predict expected food waste in kilograms.
    """

    input_data = pd.DataFrame([{
        "expected_attendance": expected_attendance,
        "meals_prepared": meals_prepared,
        "previous_day_waste": previous_day_waste,
        "avg_7day_waste": avg_7day_waste,
        "temperature": temperature,
        "portion_size": portion_size,
        "event": event,
        "holiday": holiday,
        "day_of_week": day_of_week,
        "meal_type": meal_type,
        "menu_category": menu_category
    }])

    prediction = model.predict(input_data)[0]

    return max(0, float(prediction))


def classify_risk(waste_kg):
    """
    Convert predicted waste into an operational risk level.
    """

    if waste_kg < 5:
        return "LOW"

    elif waste_kg < 8:
        return "MEDIUM"

    else:
        return "HIGH"


def calculate_preparation_gap(
    expected_attendance,
    meals_prepared
):
    """
    Calculate how many meals exceed expected attendance.
    """

    return max(
        0,
        meals_prepared - expected_attendance
    )


def generate_recommendation(
    expected_attendance,
    meals_prepared,
    waste_kg,
    menu_category
):
    """
    Generate an initial rule-based operational recommendation.
    """

    preparation_gap = calculate_preparation_gap(
        expected_attendance,
        meals_prepared
    )

    risk = classify_risk(waste_kg)

    if risk == "HIGH":

        recommended_meals = round(
            expected_attendance * 1.03
        )

        action = (
            f"Reduce preparation from "
            f"{meals_prepared} to approximately "
            f"{recommended_meals} meals."
        )

    elif risk == "MEDIUM":

        recommended_meals = round(
            expected_attendance * 1.05
        )

        action = (
            f"Consider reducing preparation to "
            f"approximately {recommended_meals} meals."
        )

    else:

        recommended_meals = meals_prepared

        action = (
            "Current preparation level appears "
            "reasonable."
        )

    if menu_category == "Rice-Based":

        action += (
            " Monitor rice portions closely because "
            "rice-based meals can contribute "
            "significantly to leftover waste."
        )

    return {
        "risk": risk,
        "preparation_gap": preparation_gap,
        "recommended_meals": recommended_meals,
        "action": action
    }

def optimize_meal_preparation(
    expected_attendance,
    previous_day_waste,
    avg_7day_waste,
    temperature,
    portion_size,
    event,
    holiday,
    day_of_week,
    meal_type,
    menu_category,
    current_meals_prepared
):
    """
    Find a preparation quantity that balances
    expected demand and predicted food waste.
    """

    # Keep a small safety buffer above expected attendance
    minimum_meals = round(expected_attendance * 1.02)

    # Do not recommend more than the current preparation
    maximum_meals = max(
        current_meals_prepared,
        minimum_meals
    )

    scenarios = []

    # Test different preparation quantities
    for meals in range(
        minimum_meals,
        maximum_meals + 1
    ):

        predicted_waste = predict_waste(
            expected_attendance=expected_attendance,
            meals_prepared=meals,
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

        scenarios.append({
            "meals": meals,
            "waste": predicted_waste
        })

    # Find the scenario with the lowest predicted waste
    best_scenario = min(
        scenarios,
        key=lambda x: x["waste"]
    )

    # Predict waste for the current plan
    baseline_waste = predict_waste(
        expected_attendance=expected_attendance,
        meals_prepared=current_meals_prepared,
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

    waste_reduction = (
        baseline_waste -
        best_scenario["waste"]
    )

    if baseline_waste > 0:
        reduction_percentage = (
            waste_reduction /
            baseline_waste
        ) * 100
    else:
        reduction_percentage = 0

    return {
        "current_meals": current_meals_prepared,
        "recommended_meals": best_scenario["meals"],
        "current_waste": round(baseline_waste, 2),
        "optimized_waste": round(
            best_scenario["waste"], 2
        ),
        "waste_reduction": round(
            waste_reduction, 2
        ),
        "reduction_percentage": round(
            reduction_percentage, 1
        )
    }