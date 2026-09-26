"""
WasteWise AI - Computer Vision Waste Scanner

Analyzes uploaded cafeteria waste images and identifies
likely waste categories using a pretrained vision model.
"""

from PIL import Image
from transformers import pipeline


# ---------------------------------------------------------
# Model configuration
# ---------------------------------------------------------

MODEL_NAME = "openai/clip-vit-base-patch32"

WASTE_CATEGORIES = [
    "rice and cooked grains",
    "vegetables and salad",
    "bread and bakery food",
    "fruits",
    "meat and protein food",
    "dessert and sweets",
    "mixed food waste",
    "other waste"
]

DISPLAY_NAMES = {
    "rice and cooked grains": "Rice-Based Food",
    "vegetables and salad": "Vegetables",
    "bread and bakery food": "Bread & Bakery",
    "fruits": "Fruits",
    "meat and protein food": "Meat & Protein",
    "dessert and sweets": "Desserts",
    "mixed food waste": "Mixed Food",
    "other waste": "Other"
}


# ---------------------------------------------------------
# Load model lazily
# ---------------------------------------------------------

_classifier = None


def get_classifier():
    """
    Load the vision model only when it is actually needed.
    This prevents Streamlit from loading the model on every rerun.
    """

    global _classifier

    if _classifier is None:
        _classifier = pipeline(
            "zero-shot-image-classification",
            model=MODEL_NAME
        )

    return _classifier


# ---------------------------------------------------------
# Recommendation engine
# ---------------------------------------------------------

def generate_scanner_recommendation(category, confidence):
    """
    Generate a practical cafeteria recommendation
    based on the dominant waste category.
    """

    recommendations = {
        "rice and cooked grains": (
            "Reduce rice preparation slightly, review serving portions, "
            "and monitor leftover rice after each meal."
        ),

        "vegetables and salad": (
            "Review vegetable demand and preparation quantities. "
            "Consider preparing vegetables in smaller batches."
        ),

        "bread and bakery food": (
            "Reduce excess bread preparation and consider smaller "
            "serving quantities or made-to-order replenishment."
        ),

        "fruits": (
            "Review fruit purchasing and serving quantities. "
            "Prioritize smaller batches and replenish based on demand."
        ),

        "meat and protein food": (
            "Compare protein preparation with actual attendance and "
            "consider smaller preparation batches."
        ),

        "dessert and sweets": (
            "Review dessert demand and reduce overproduction while "
            "maintaining sufficient availability."
        ),

        "mixed food waste": (
            "Separate waste by food type during collection to identify "
            "the biggest contributors and improve preparation planning."
        ),

        "other waste": (
            "Improve waste segregation so the system can identify "
            "specific food categories contributing to waste."
        )
    }

    recommendation = recommendations.get(
        category,
        "Review preparation quantities and monitor food waste trends."
    )

    if confidence < 0.45:
        recommendation += (
            " The image confidence is relatively low, so use this "
            "result as an indication rather than an exact measurement."
        )

    return recommendation


# ---------------------------------------------------------
# Insight engine
# ---------------------------------------------------------

def generate_scanner_insight(category, confidence):
    """
    Generate a human-readable AI insight.
    """

    display_name = DISPLAY_NAMES.get(category, category)

    if confidence >= 0.75:
        confidence_text = "high confidence"
    elif confidence >= 0.50:
        confidence_text = "moderate confidence"
    else:
        confidence_text = "lower confidence"

    return (
        f"{display_name} appears to be the dominant visible waste category "
        f"with {confidence_text}. This can help cafeteria staff identify "
        f"where preparation or portion planning may need adjustment."
    )


# ---------------------------------------------------------
# Main scanner function
# ---------------------------------------------------------

def analyze_waste_image(image):
    """
    Analyze a cafeteria waste image.

    Parameters
    ----------
    image : PIL.Image.Image
        Uploaded image.

    Returns
    -------
    dict
        Structured waste analysis.
    """

    if image is None:
        raise ValueError("No image was provided.")

    # Make sure the image is RGB
    if image.mode != "RGB":
        image = image.convert("RGB")

    try:
        classifier = get_classifier()

        results = classifier(
            image,
            candidate_labels=WASTE_CATEGORIES
        )

        # Sort highest confidence first
        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        # Convert model scores into percentages
        categories = {}

        for result in results:
            category = result["label"]
            score = float(result["score"])

            categories[
                DISPLAY_NAMES.get(category, category)
            ] = round(score * 100, 1)

        # Dominant category
        dominant = results[0]

        dominant_category = dominant["label"]
        confidence = float(dominant["score"])

        display_category = DISPLAY_NAMES.get(
            dominant_category,
            dominant_category
        )

        insight = generate_scanner_insight(
            dominant_category,
            confidence
        )

        recommendation = generate_scanner_recommendation(
            dominant_category,
            confidence
        )

        return {
            "success": True,
            "dominant_category": display_category,
            "confidence": round(confidence, 3),
            "confidence_percent": round(confidence * 100, 1),
            "categories": categories,
            "insight": insight,
            "recommendation": recommendation
        }

    except Exception as e:

        # -------------------------------------------------
        # Graceful fallback
        # -------------------------------------------------

        return {
            "success": False,
            "dominant_category": "Unable to classify",
            "confidence": 0,
            "confidence_percent": 0,
            "categories": {},
            "insight": (
                "The AI vision model could not analyze this image. "
                "Please try again with a clearer image of the food waste."
            ),
            "recommendation": (
                "Use a well-lit image containing visible food waste "
                "and avoid heavily blurred or obstructed images."
            ),
            "error": str(e)
        }