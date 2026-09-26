import sys
import base64
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

# ============================================================
# PATH CONFIGURATION
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from prediction_engine import (
    predict_waste,
    classify_risk,
    optimize_meal_preparation
)

from waste_scanner import analyze_waste_image


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="WasteWise AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PROFILE
# ============================================================

if "profile_name" not in st.session_state:
    st.session_state.profile_name = "My Profile"

if "profile_role" not in st.session_state:
    st.session_state.profile_role = "Cafeteria Administrator"

# ============================================================
# THEME DEFINITIONS
# ============================================================

THEMES = {

    "🌊 Ocean": {
        "background": "#0b1120",
        "surface": "#111827",
        "surface2": "#172033",
        "primary": "#06b6d4",
        "secondary": "#0ea5e9",
        "text": "#f8fafc",
        "heading": "#ffffff",
        "muted": "#cbd5e1",
        "hero_start": "#0891b2",
        "hero_end": "#155e75"
    },

    "🌲 Forest": {
        "background": "#071a13",
        "surface": "#0d241b",
        "surface2": "#123326",
        "primary": "#22c55e",
        "secondary": "#10b981",
        "text": "#f7fff9",
        "heading": "#ffffff",
        "muted": "#d1fae5",
        "hero_start": "#047857",
        "hero_end": "#14532d"
    },

    "🌌 Midnight": {
        "background": "#080b14",
        "surface": "#111827",
        "surface2": "#1e293b",
        "primary": "#8b5cf6",
        "secondary": "#6366f1",
        "text": "#f8f7ff",
        "heading": "#ffffff",
        "muted": "#d8d4fe",
        "hero_start": "#4c1d95",
        "hero_end": "#1e1b4b"
    },

    "🌅 Sunset": {
        "background": "#1c1012",
        "surface": "#24151a",
        "surface2": "#321b22",
        "primary": "#f97316",
        "secondary": "#ec4899",
        "text": "#fffaf5",
        "heading": "#ffffff",
        "muted": "#fed7aa",
        "hero_start": "#c2410c",
        "hero_end": "#9d174d"
    },

    "🌿 Eco Green": {
        "background": "#07130d",
        "surface": "#0d1f15",
        "surface2": "#143522",
        "primary": "#84cc16",
        "secondary": "#22c55e",
        "text": "#fbfff5",
        "heading": "#ffffff",
        "muted": "#d9f99d",
        "hero_start": "#15803d",
        "hero_end": "#365314"
    },

    "☀️ Clean Light": {
        "background": "#f4f7f6",
        "surface": "#ffffff",
        "surface2": "#eef4f2",
        "primary": "#047857",
        "secondary": "#0f766e",
        "text": "#17202a",
        "heading": "#0f172a",
        "muted": "#475569",
        "hero_start": "#0f766e",
        "hero_end": "#155e75"
    },

    "⚡ Neon": {
        "background": "#050509",
        "surface": "#101016",
        "surface2": "#181822",
        "primary": "#a3e635",
        "secondary": "#22d3ee",
        "text": "#f8fafc",
        "heading": "#ffffff",
        "muted": "#d9f99d",
        "hero_start": "#365314",
        "hero_end": "#164e63"
    }
}

# ============================================================
# WALLPAPER OPTIONS
# ============================================================

WALLPAPERS = {

    "🌊 Ocean": """
        radial-gradient(
            circle at top right,
            rgba(6,182,212,0.22),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #020617,
            #0f172a,
            #083344
        )
    """,

    "🌲 Forest": """
        radial-gradient(
            circle at top left,
            rgba(34,197,94,0.18),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #020617,
            #052e16,
            #064e3b
        )
    """,

    "🌌 Galaxy": """
        radial-gradient(
            circle at 20% 20%,
            rgba(139,92,246,0.25),
            transparent 25%
        ),
        radial-gradient(
            circle at 80% 70%,
            rgba(59,130,246,0.20),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #020617,
            #111827,
            #1e1b4b
        )
    """,

    "🌅 Sunset": """
        radial-gradient(
            circle at 80% 20%,
            rgba(249,115,22,0.25),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #1c0a0a,
            #431407,
            #4a044e
        )
    """,

    "🌿 Nature": """
        radial-gradient(
            circle at 20% 80%,
            rgba(132,204,22,0.18),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #020617,
            #052e16,
            #172554
        )
    """,

    "⬛ Minimal": """
        linear-gradient(
            135deg,
            #0f1117,
            #111827
        )
    """
}


# ============================================================
# PROFILE
# ============================================================

st.sidebar.subheader("👤 My Profile")

st.sidebar.html(
    f'''
    <div style="
        background: linear-gradient(
            135deg,
            rgba(15,118,110,0.32),
            rgba(6,78,59,0.50)
        );
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 16px;
        padding: 14px;
        margin-bottom: 10px;
    ">
        <div style="
            display:flex;
            align-items:center;
            gap:12px;
        ">
            <div style="
                width:50px;
                height:50px;
                min-width:50px;
                border-radius:50%;
                background:rgba(255,255,255,0.16);
                border:2px solid rgba(255,255,255,0.55);
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:24px;
                line-height:1;
                box-shadow:0 4px 14px rgba(0,0,0,0.20);
            ">👤</div>

            <div style="min-width:0;">
                <div style="
                    color:#ffffff;
                    font-size:1rem;
                    font-weight:800;
                    white-space:nowrap;
                    overflow:hidden;
                    text-overflow:ellipsis;
                ">{st.session_state.profile_name}</div>

                <div style="
                    color:#d1fae5;
                    font-size:0.78rem;
                    margin-top:3px;
                ">{st.session_state.profile_role}</div>

                <div style="
                    color:#86efac;
                    font-size:0.74rem;
                    font-weight:700;
                    margin-top:5px;
                ">🟢 Active</div>
            </div>
        </div>
    </div>
    '''
)

with st.sidebar.expander("⚙️ Profile Settings"):
    profile_name = st.text_input(
        "Name",
        value=st.session_state.profile_name,
        key="profile_name_input"
    )

    profile_role = st.selectbox(
        "Role",
        [
            "Cafeteria Administrator",
            "Cafeteria Manager",
            "Operations Manager",
            "Sustainability Manager",
            "Student / Researcher",
            "Demo User"
        ],
        index=0,
        key="profile_role_input"
    )

    if st.button("💾 Save Profile", use_container_width=True):
        st.session_state.profile_name = profile_name.strip() or "My Profile"
        st.session_state.profile_role = profile_role
        st.rerun()


# ============================================================
# APPEARANCE STUDIO
# ============================================================

st.sidebar.divider()

st.sidebar.subheader("🎨 Appearance")

st.sidebar.caption(
    "Customize the dashboard colors and background."
)

selected_theme = st.sidebar.selectbox(
    "Theme",
    list(THEMES.keys()),
    index=0
)

theme = THEMES[selected_theme]


wallpaper_choice = st.sidebar.selectbox(
    "Background",
    [
        "🎨 Theme Gradient",
        "🌊 Ocean",
        "🌲 Forest",
        "🌌 Galaxy",
        "🌅 Sunset",
        "🌿 Nature",
        "⬛ Minimal",
        "🖼️ Custom Wallpaper"
    ]
)


accent_color = st.sidebar.color_picker(
    "Accent Color",
    theme["primary"]
)


text_color = st.sidebar.color_picker(
    "Text Color",
    theme["text"]
)


overlay_opacity = st.sidebar.slider(
    "Wallpaper Overlay",
    min_value=10,
    max_value=80,
    value=45,
    step=5
)


uploaded_wallpaper = None

if wallpaper_choice == "🖼️ Custom Wallpaper":

    uploaded_wallpaper = st.sidebar.file_uploader(
        "Upload your wallpaper",
        type=[
            "png",
            "jpg",
            "jpeg",
            "webp"
        ]
    )

# ============================================================
# WALLPAPER PROCESSING
# ============================================================

background_css = ""


if wallpaper_choice == "🎨 Theme Gradient":

    background_css = f"""
        linear-gradient(
            135deg,
            {theme["hero_start"]},
            {theme["hero_end"]}
        )
    """

elif wallpaper_choice == "🖼️ Custom Wallpaper":

    if uploaded_wallpaper is not None:

        image_bytes = uploaded_wallpaper.getvalue()

        encoded_image = base64.b64encode(
            image_bytes
        ).decode()

        mime_type = uploaded_wallpaper.type

        background_css = (
            f'url("data:{mime_type};base64,{encoded_image}")'
        )

    else:

        background_css = WALLPAPERS["⬛ Minimal"]

else:

    background_css = WALLPAPERS[wallpaper_choice]


# ============================================================
# DYNAMIC APPLICATION THEME
# ============================================================

overlay_alpha = overlay_opacity / 100


st.html(
    f"""
<style>

:root {{

    --background: {theme["background"]};
    --surface: {theme["surface"]};
    --surface2: {theme["surface2"]};

    --primary: {accent_color};
    --secondary: {theme["secondary"]};

    --text: {text_color};
    --heading: {theme["heading"]};
    --muted: {theme["muted"]};

}}


/* ============================================================
   MAIN APPLICATION
   ============================================================ */

.stApp {{

    background-color: var(--background);

    background-image:
        linear-gradient(
            rgba(0, 0, 0, {overlay_alpha}),
            rgba(0, 0, 0, {overlay_alpha})
        ),
        {background_css};

    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: fixed;

    color: var(--text);
}}

/* ============================================================
   THEME-AWARE TEXT CONTRAST
   ============================================================ */

.stApp,
.stApp p,
.stApp span,
.stApp label,
.stApp div,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp h5,
.stApp h6 {{
    color: var(--text);
}}


/* Main headings */

.stApp h1,
.stApp h2,
.stApp h3 {{
    color: var(--heading) !important;
    font-weight: 800 !important;
}}


/* Normal text */

.stApp p {{
    color: var(--text) !important;
}}


/* Sidebar */

[data-testid="stSidebar"] {{
    color: var(--text) !important;
}}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {{
    color: var(--text) !important;
}}


/* Metric labels */

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {{
    color: var(--muted) !important;
    font-weight: 700 !important;
}}


/* Metric values */

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {{
    color: var(--heading) !important;
    font-weight: 800 !important;
}}


/* Metric delta */

[data-testid="stMetricDelta"] {{
    color: var(--primary) !important;
}}


/* Selectbox / number input labels */

[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p {{
    color: var(--text) !important;
    font-weight: 700 !important;
}}


/* Slider labels */

[data-testid="stSlider"] label,
[data-testid="stSlider"] label p {{
    color: var(--text) !important;
    font-weight: 700 !important;
}}


/* Caption */

.stCaption,
[data-testid="stCaptionContainer"] {{
    color: var(--muted) !important;
}}


/* Input text */

[data-baseweb="input"] input,
[data-baseweb="select"] input,
[data-baseweb="select"] div {{
    color: var(--text) !important;
}}


/* Dropdown menu text */

[data-baseweb="popover"] * {{
    color: var(--text) !important;
}}


/* Streamlit buttons */

.stButton button {{
    color: var(--heading) !important;
    font-weight: 700 !important;
}}


/* Divider */

[data-testid="stDivider"] {{
    border-color: color-mix(in srgb, var(--text) 20%, transparent) !important;
}}


/* ============================================================
   MAIN CONTENT
   ============================================================ */

.block-container {{

    padding-top: 2rem;
    padding-bottom: 3rem;

    max-width: 1400px;

}}


/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {{

    background:
        linear-gradient(
            rgba(0,0,0,0.15),
            rgba(0,0,0,0.15)
        ),
        var(--surface);

    border-right:
        1px solid
        rgba(255,255,255,0.08);

}}


/* ============================================================
   SIDEBAR TEXT
   ============================================================ */

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {{

    color: var(--text) !important;

}}


/* ============================================================
   HERO
   ============================================================ */

.hero-box {{

    background:
        linear-gradient(
            135deg,
            {theme["hero_start"]},
            {theme["hero_end"]}
        );

    padding: 2.5rem;

    border-radius: 24px;

    margin-bottom: 2rem;

    box-shadow:
        0 15px 50px
        rgba(0,0,0,0.25);

    border:
        1px solid
        rgba(255,255,255,0.12);

}}


.hero-title {{

    color: white;

    font-size: 2.8rem;

    font-weight: 800;

    margin-bottom: 0.5rem;

}}


.hero-subtitle {{

    color: white;

    font-size: 1.2rem;

    font-weight: 500;

}}


.hero-description {{

    color: #d1fae5;

    font-size: 0.95rem;

    margin-top: 0.6rem;

}}


/* ============================================================
   RECOMMENDATION
   ============================================================ */

.recommendation-box {{

    background:
        linear-gradient(
            135deg,
            rgba(6, 78, 59, 0.90),
            rgba(15, 118, 110, 0.75)
        );

    border-left:
        6px solid
        var(--primary);

    padding: 1.5rem;

    border-radius: 16px;

    backdrop-filter: blur(10px);

    border-top:
        1px solid
        rgba(255,255,255,0.12);

    border-right:
        1px solid
        rgba(255,255,255,0.12);

    border-bottom:
        1px solid
        rgba(255,255,255,0.12);

}}


.recommendation-title {{

    color: #ffffff !important;

    font-size: 1rem;

    font-weight: 800;

}}


.recommendation-number {{

    color: #ffffff !important;

    font-size: 2.2rem;

    font-weight: 900;

    margin-top: 0.4rem;

    margin-bottom: 0.6rem;

}}


.recommendation-text {{

    color: #ffffff !important;

    font-size: 1rem;

    line-height: 1.7;

    font-weight: 500;

}}


.recommendation-text strong {{

    color: #ffffff !important;

    font-weight: 800;

}}


/* ============================================================
   RISK CARDS
   ============================================================ */

.risk-high {{

    background:
        linear-gradient(
            135deg,
            #451a1a,
            #3f1d1d
        );

    border:
        1px solid
        #ef4444;

    color:
        #fca5a5;

    padding: 1rem;

    border-radius: 14px;

    text-align: center;

    font-weight: 800;

    font-size: 1.1rem;

}}


.risk-medium {{

    background:
        linear-gradient(
            135deg,
            #453b17,
            #3f3417
        );

    border:
        1px solid
        #f59e0b;

    color:
        #fcd34d;

    padding: 1rem;

    border-radius: 14px;

    text-align: center;

    font-weight: 800;

    font-size: 1.1rem;

}}


.risk-low {{

    background:
        linear-gradient(
            135deg,
            #143b2a,
            #123524
        );

    border:
        1px solid
        #22c55e;

    color:
        #86efac;

    padding: 1rem;

    border-radius: 14px;

    text-align: center;

    font-weight: 800;

    font-size: 1.1rem;

}}


/* ============================================================
   INFO BOX
   ============================================================ */

.info-box {{

    background:
        rgba(23,37,84,0.75);

    border:
        1px solid
        rgba(59,130,246,0.5);

    color:
        #bfdbfe;

    padding: 1rem 1.2rem;

    border-radius: 14px;

    backdrop-filter: blur(10px);

}}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {{

    text-align: center;

    color:
        var(--muted);

    padding:
        2rem 0 1rem 0;

}}


.footer-title {{

    font-size: 1.1rem;

    font-weight: 700;

    color:
        var(--primary);

}}

</style>
"""
)


# ============================================================
# HERO
# ============================================================

st.html("""
<div class="hero-box">

    <div class="hero-title">
        🌱 WasteWise AI
    </div>

    <div class="hero-subtitle">
        Predict waste. Optimize preparation. Reduce unnecessary waste.
    </div>

    <div class="hero-description">
        AI-powered decision support for institutional cafeterias.
    </div>

</div>
""")

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Cafeteria Inputs")

st.sidebar.caption(
    "Enter today's operational conditions."
)

st.sidebar.divider()


# ============================================================
# OPERATIONS
# ============================================================

st.sidebar.subheader("📋 Operations")

expected_attendance = st.sidebar.number_input(
    "Expected Attendance",
    min_value=50,
    max_value=2000,
    value=420,
    step=10
)

meals_prepared = st.sidebar.number_input(
    "Meals Prepared",
    min_value=50,
    max_value=2500,
    value=450,
    step=10
)


# ============================================================
# HISTORICAL DATA
# ============================================================

st.sidebar.subheader("📊 Historical Data")

previous_day_waste = st.sidebar.number_input(
    "Previous Day Waste (kg)",
    min_value=0.0,
    max_value=100.0,
    value=7.2,
    step=0.1
)

avg_7day_waste = st.sidebar.number_input(
    "7-Day Average Waste (kg)",
    min_value=0.0,
    max_value=100.0,
    value=6.8,
    step=0.1
)


# ============================================================
# CONDITIONS
# ============================================================

st.sidebar.subheader("🌤️ Conditions")

temperature = st.sidebar.slider(
    "Temperature (°C)",
    min_value=10,
    max_value=45,
    value=28
)

portion_size = st.sidebar.slider(
    "Portion Size (%)",
    min_value=70,
    max_value=130,
    value=100
)

event = st.sidebar.selectbox(
    "Special Event",
    ["No", "Yes"]
)

event_value = 1 if event == "Yes" else 0


holiday = st.sidebar.selectbox(
    "Holiday",
    ["No", "Yes"]
)

holiday_value = 1 if holiday == "Yes" else 0


# ============================================================
# MEAL DETAILS
# ============================================================

st.sidebar.subheader("🍽️ Meal Details")

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

day_of_week = st.sidebar.selectbox(
    "Day of Week",
    days
)

day_number = days.index(day_of_week)


meal_type = st.sidebar.selectbox(
    "Meal Type",
    [
        "Breakfast",
        "Lunch",
        "Dinner"
    ]
)


menu_category = st.sidebar.selectbox(
    "Menu Category",
    [
        "Rice-Based",
        "Roti-Based",
        "Mixed",
        "Light Meal"
    ]
)


# ============================================================
# ML PREDICTION
# ============================================================

predicted_waste = predict_waste(
    expected_attendance=expected_attendance,
    meals_prepared=meals_prepared,
    previous_day_waste=previous_day_waste,
    avg_7day_waste=avg_7day_waste,
    temperature=temperature,
    portion_size=portion_size,
    event=event_value,
    holiday=holiday_value,
    day_of_week=day_number,
    meal_type=meal_type,
    menu_category=menu_category
)


# ============================================================
# RISK
# ============================================================

risk = classify_risk(predicted_waste)


# ============================================================
# OPTIMIZATION
# ============================================================

optimization = optimize_meal_preparation(
    expected_attendance=expected_attendance,
    previous_day_waste=previous_day_waste,
    avg_7day_waste=avg_7day_waste,
    temperature=temperature,
    portion_size=portion_size,
    event=event_value,
    holiday=holiday_value,
    day_of_week=day_number,
    meal_type=meal_type,
    menu_category=menu_category,
    current_meals_prepared=meals_prepared
)


recommended_meals = optimization["recommended_meals"]


# ============================================================
# CURRENT SITUATION
# ============================================================

st.header("📊 Current Situation")

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Predicted Waste",
        f"{predicted_waste:.2f} kg"
    )


with col2:
    st.metric(
        "Meals Prepared",
        f"{meals_prepared}"
    )


with col3:
    st.metric(
        "Expected Attendance",
        f"{expected_attendance}"
    )


with col4:
    st.metric(
        "Potential Reduction",
        f"{optimization['waste_reduction']:.2f} kg"
    )


# ============================================================
# AI ANALYSIS
# ============================================================

st.header("🚦 AI Analysis")

left, right = st.columns([1, 2])


# ============================================================
# RISK CARD
# ============================================================

with left:

    risk_class = risk.lower()

    st.html(
        f"""
        <div class="risk-{risk_class}">
            {risk} WASTE RISK
        </div>
        """
    )

    st.write("")

    st.metric(
        "Predicted Waste",
        f"{predicted_waste:.2f} kg"
    )

    preparation_gap = max(
        0,
        meals_prepared - expected_attendance
    )

    st.metric(
        "Preparation Gap",
        f"{preparation_gap} meals"
    )


# ============================================================
# AI RECOMMENDATION
# ============================================================

with right:

    st.html(
        f"""
        <div class="recommendation-box">

            <div class="recommendation-title">
                🤖 AI RECOMMENDATION
            </div>

            <div class="recommendation-number">
                {recommended_meals} meals
            </div>

            <div class="recommendation-text">

                Current preparation:
                <strong>{meals_prepared} meals</strong>

                <br><br>

                Predicted waste:
                <strong>
                    {optimization["current_waste"]:.2f} kg
                </strong>

                →

                <strong>
                    {optimization["optimized_waste"]:.2f} kg
                </strong>

                <br><br>

                Potential reduction:
                <strong>
                    {optimization["waste_reduction"]:.2f} kg
                </strong>

                (
                {optimization["reduction_percentage"]:.1f}%
                )

            </div>

        </div>
        """
    )


# ============================================================
# WHAT-IF SIMULATOR
# ============================================================

st.header("🎛️ What-If Simulator")

st.write(
    "Change the number of meals prepared and see how "
    "the predicted waste changes."
)


simulation_min = max(
    1,
    expected_attendance
)

simulation_max = max(
    expected_attendance + 200,
    meals_prepared + 100
)


simulation_meals = st.slider(
    "Meals to Prepare",
    min_value=simulation_min,
    max_value=simulation_max,
    value=min(
        meals_prepared,
        simulation_max
    ),
    step=1
)


# ============================================================
# SIMULATED PREDICTION
# ============================================================

simulation_waste = predict_waste(
    expected_attendance=expected_attendance,
    meals_prepared=simulation_meals,
    previous_day_waste=previous_day_waste,
    avg_7day_waste=avg_7day_waste,
    temperature=temperature,
    portion_size=portion_size,
    event=event_value,
    holiday=holiday_value,
    day_of_week=day_number,
    meal_type=meal_type,
    menu_category=menu_category
)


simulation_difference = (
    predicted_waste - simulation_waste
)


# ============================================================
# SIMULATION RESULTS
# ============================================================

sim1, sim2, sim3 = st.columns(3)


with sim1:

    st.metric(
        "Meals",
        simulation_meals
    )


with sim2:

    st.metric(
        "Predicted Waste",
        f"{simulation_waste:.2f} kg"
    )


with sim3:

    st.metric(
        "Waste Difference",
        f"{simulation_difference:+.2f} kg"
    )


# ============================================================
# CHART
# ============================================================

st.header("📈 Waste Comparison")


chart_data = pd.DataFrame(
    {
        "Scenario": [
            "Current Plan",
            "AI Recommendation",
            "Your Scenario"
        ],
        "Waste": [
            optimization["current_waste"],
            optimization["optimized_waste"],
            simulation_waste
        ]
    }
)


fig = go.Figure()


fig.add_trace(
    go.Bar(
        x=chart_data["Scenario"],
        y=chart_data["Waste"],
        text=[
            f"{value:.2f} kg"
            for value in chart_data["Waste"]
        ],
        textposition="auto"
    )
)


fig.update_layout(
    title="Predicted Food Waste by Scenario",
    yaxis_title="Waste (kg)",
    xaxis_title="",
    height=420,
    showlegend=False,
    template=(
        "plotly_white"
        if selected_theme == "☀️ Clean Light"
        else "plotly_dark"
    ),
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# POTENTIAL IMPACT
# ============================================================

st.header("🌱 Potential Impact")


st.html(
    """
    <div class="info-box">

        <strong>Prototype estimate:</strong>

        These figures represent simulated potential reductions.
        Real-world environmental and financial impact requires
        validated cafeteria data and conversion factors.

    </div>
    """
)


impact_reduction = max(
    0,
    optimization["waste_reduction"]
)


monthly_reduction = (
    impact_reduction * 30
)


meals_avoided = max(
    0,
    meals_prepared - recommended_meals
)


impact1, impact2, impact3 = st.columns(3)


with impact1:

    st.metric(
        "Daily Waste Reduction",
        f"{impact_reduction:.2f} kg"
    )


with impact2:

    st.metric(
        "30-Day Potential Reduction",
        f"{monthly_reduction:.1f} kg"
    )


with impact3:

    st.metric(
        "Meals Avoiding Overproduction",
        meals_avoided
    )

# ============================================================
# AI WASTE SCANNER
# ============================================================

st.header("📷 AI Waste Scanner")

st.write(
    "Upload a photo of cafeteria food waste. "
    "WasteWise AI will estimate the dominant visible "
    "food-waste category and generate an actionable insight."
)

scanner_file = st.file_uploader(
    "Upload today's food-waste image",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp"
    ],
    key="waste_scanner_upload"
)


if scanner_file is not None:

    try:

        # ----------------------------------------------------
        # Load uploaded image
        # ----------------------------------------------------

        scanner_image = Image.open(
            scanner_file
        ).convert("RGB")


        scanner_col1, scanner_col2 = st.columns(
            [1, 1.5]
        )


        # ----------------------------------------------------
        # IMAGE PREVIEW
        # ----------------------------------------------------

        with scanner_col1:

            st.image(
                scanner_image,
                caption="Uploaded Waste Image",
                use_container_width=True
            )


        # ----------------------------------------------------
        # AI ANALYSIS
        # ----------------------------------------------------

        with scanner_col2:

            with st.spinner(
                "🤖 AI is analyzing the waste image..."
            ):

                scanner_result = analyze_waste_image(
                    scanner_image
                )


            if scanner_result["success"]:

                st.success(
                    "✅ Waste image analyzed successfully"
                )


                # --------------------------------------------
                # Dominant category
                # --------------------------------------------

                st.subheader(
                    "🔎 Dominant Waste"
                )

                st.metric(
                    "Primary Category",
                    scanner_result[
                        "dominant_category"
                    ]
                )


                st.metric(
                    "AI Confidence",
                    f"{scanner_result['confidence_percent']:.1f}%"
                )


            else:

                st.error(
                    "⚠️ The AI scanner could not analyze "
                    "this image."
                )

                st.write(
                    scanner_result.get(
                        "recommendation",
                        "Try uploading a clearer image."
                    )
                )


    except Exception as e:

        st.error(
            f"Scanner error: {e}"
        )


    # ========================================================
    # SCANNER RESULTS
    # ========================================================

    if scanner_result["success"]:

        st.divider()

        result_col1, result_col2 = st.columns(
            [1.1, 1]
        )


        # ----------------------------------------------------
        # CATEGORY BREAKDOWN
        # ----------------------------------------------------

        with result_col1:

            st.subheader(
                "📊 Waste Category Breakdown"
            )


            categories = scanner_result[
                "categories"
            ]


            category_df = pd.DataFrame(
                {
                    "Category": list(
                        categories.keys()
                    ),
                    "Percentage": list(
                        categories.values()
                    )
                }
            )


            # Keep the strongest visible categories
            category_df = category_df.sort_values(
                "Percentage",
                ascending=False
            ).head(6)


            scanner_fig = go.Figure(
                go.Bar(
                    x=category_df[
                        "Percentage"
                    ],
                    y=category_df[
                        "Category"
                    ],
                    orientation="h",
                    text=[
                        f"{value:.1f}%"
                        for value in category_df[
                            "Percentage"
                        ]
                    ],
                    textposition="auto"
                )
            )


            scanner_fig.update_layout(
                title="AI Visual Category Scores",
                xaxis_title="Model Score (%)",
                yaxis_title="",
                height=400,
                showlegend=False,
                template=(
                    "plotly_white"
                    if selected_theme == "☀️ Clean Light"
                    else "plotly_dark"
                ),
                margin=dict(
                    l=20,
                    r=20,
                    t=60,
                    b=20
                )
            )


            st.plotly_chart(
                scanner_fig,
                use_container_width=True
            )


        # ----------------------------------------------------
        # AI INSIGHT
        # ----------------------------------------------------

        with result_col2:

            st.subheader(
                "🧠 AI Insight"
            )


            st.html(
                f"""
                <div class="info-box">

                    <strong>
                        Dominant Waste:
                    </strong>

                    <br>

                    {scanner_result["dominant_category"]}

                    <br><br>

                    <strong>
                        Confidence:
                    </strong>

                    <br>

                    {scanner_result["confidence_percent"]:.1f}%

                    <br><br>

                    <strong>
                        AI Insight:
                    </strong>

                    <br>

                    {scanner_result["insight"]}

                </div>
                """
            )


            st.write("")


            st.subheader(
                "💡 Recommended Action"
            )


            st.html(
                f"""
                <div class="recommendation-box">

                    <div class="recommendation-title">
                        🤖 SCANNER RECOMMENDATION
                    </div>

                    <div class="recommendation-text">

                        {scanner_result["recommendation"]}

                    </div>

                </div>
                """
            )


        # ====================================================
        # CONNECT SCANNER TO PREDICTIVE AI
        # ====================================================

        st.divider()

        st.subheader(
            "🔗 Combined AI Decision"
        )


        combined_col1, combined_col2, combined_col3 = st.columns(
            3
        )


        with combined_col1:

            st.metric(
                "Predicted Daily Waste",
                f"{predicted_waste:.2f} kg"
            )


        with combined_col2:

            st.metric(
                "Waste Risk",
                risk
            )


        with combined_col3:

            st.metric(
                "Recommended Preparation",
                f"{recommended_meals} meals"
            )


        st.info(
            f"""
            **WasteWise AI is combining two signals:**

            • Predictive ML estimates approximately
            **{predicted_waste:.2f} kg** of waste.

            • Computer Vision identifies
            **{scanner_result["dominant_category"]}**
            as the dominant visible waste category.

            • The operational optimizer recommends preparing
            **{recommended_meals} meals** instead of
            **{meals_prepared} meals**.

            Together, these signals can help cafeteria staff
            understand both **how much waste may occur** and
            **what type of food is contributing to it**.
            """
        )

# ============================================================
# WASTE INTELLIGENCE DASHBOARD
# ============================================================

if scanner_file is not None and scanner_result["success"]:

    st.header("🧠 Waste Intelligence")

    st.write(
        "WasteWise AI combines operational prediction with "
        "visual waste analysis to support a practical cafeteria decision."
    )

    # --------------------------------------------------------
    # INTELLIGENCE METRICS
    # --------------------------------------------------------

    intelligence_col1, intelligence_col2, intelligence_col3, intelligence_col4 = st.columns(4)

    with intelligence_col1:

        st.metric(
            "Predicted Waste",
            f"{predicted_waste:.2f} kg"
        )

    with intelligence_col2:

        st.metric(
            "Recommended Meals",
            f"{recommended_meals}"
        )

    with intelligence_col3:

        st.metric(
            "Potential Reduction",
            f"{optimization['waste_reduction']:.2f} kg"
        )

    with intelligence_col4:

        st.metric(
            "Visual Confidence",
            f"{scanner_result['confidence_percent']:.1f}%"
        )

    st.write("")

    # --------------------------------------------------------
    # DECISION SUMMARY
    # --------------------------------------------------------

    intelligence_left, intelligence_right = st.columns(
        [1, 1]
    )

    with intelligence_left:

        st.subheader("🔎 What AI Observed")

        st.html(
            f"""
            <div class="info-box">

                <strong>Dominant visible category</strong>

                <br><br>

                <span style="
                    font-size:1.6rem;
                    font-weight:800;
                ">
                    {scanner_result["dominant_category"]}
                </span>

                <br><br>

                AI confidence:
                <strong>
                    {scanner_result["confidence_percent"]:.1f}%
                </strong>

                <br><br>

                {scanner_result["insight"]}

            </div>
            """
        )

    with intelligence_right:

        st.subheader("🎯 What AI Recommends")

        st.html(
            f"""
            <div class="recommendation-box">

                <div class="recommendation-title">
                    OPERATIONAL ACTION
                </div>

                <div class="recommendation-number">
                    {recommended_meals} meals
                </div>

                <div class="recommendation-text">

                    Prepare approximately
                    <strong>{recommended_meals} meals</strong>
                    instead of
                    <strong>{meals_prepared} meals</strong>.

                    <br><br>

                    Expected attendance:
                    <strong>{expected_attendance}</strong>

                    <br><br>

                    Potential waste reduction:
                    <strong>
                        {optimization["waste_reduction"]:.2f} kg/day
                    </strong>

                    <br><br>

                    Visual observation:
                    <strong>
                        {scanner_result["dominant_category"]}
                    </strong>

                </div>

            </div>
            """
        )

    # --------------------------------------------------------
    # AI ACTION PLAN
    # --------------------------------------------------------

    st.subheader("💡 AI Action Plan")

    dominant_category = scanner_result["dominant_category"]

    if dominant_category == "Rice-Based Food":

        action = (
            "Review rice preparation quantities and portion sizes. "
            "Use the predicted attendance and previous waste levels "
            "to avoid preparing significantly more rice than required."
        )

    elif dominant_category == "Vegetables":

        action = (
            "Review vegetable preparation quantities and consider "
            "smaller preparation batches with replenishment based "
            "on actual demand."
        )

    elif dominant_category == "Bread & Bakery":

        action = (
            "Review bread and bakery preparation quantities. "
            "Consider smaller batches and replenish based on demand."
        )

    elif dominant_category == "Fruits":

        action = (
            "Review fruit purchasing and serving quantities. "
            "Smaller replenishment batches may help reduce leftovers."
        )

    elif dominant_category == "Meat & Protein":

        action = (
            "Compare protein preparation with actual attendance "
            "and consider smaller preparation batches."
        )

    elif dominant_category == "Desserts":

        action = (
            "Review dessert demand and preparation quantities. "
            "Prepare smaller batches where operationally practical."
        )

    elif dominant_category == "Mixed Food":

        action = (
            "Mixed food waste is currently the dominant visible "
            "category. Improve waste segregation and monitor "
            "portion sizes and preparation quantities to identify "
            "which food components contribute most to leftovers."
        )

    else:

        action = (
            "Improve waste segregation and continue collecting "
            "images to identify recurring waste categories."
        )

    st.html(
        f"""
        <div class="recommendation-box">

            <div class="recommendation-title">
                🤖 WASTEWISE AI ACTION PLAN
            </div>

            <div class="recommendation-text">

                <strong>1. Prepare:</strong>
                Target approximately
                <strong>{recommended_meals} meals</strong>.

                <br><br>

                <strong>2. Monitor:</strong>
                Track today's visible
                <strong>{dominant_category}</strong>
                waste.

                <br><br>

                <strong>3. Adjust:</strong>
                {action}

                <br><br>

                <strong>4. Measure:</strong>
                Compare actual end-of-day waste with the predicted
                <strong>{predicted_waste:.2f} kg</strong>
                and evaluate whether preparation can be adjusted
                further.

            </div>

        </div>
        """
    )

    # --------------------------------------------------------
    # DECISION FLOW
    # --------------------------------------------------------

    st.header("🔄 WasteWise AI Decision Flow")

    flow1, flow2, flow3, flow4, flow5 = st.columns(5)

    with flow1:
        st.success("📊 Predict")
        st.caption(
            f"{predicted_waste:.2f} kg expected"
        )

    with flow2:
        st.success("🚦 Assess")
        st.caption(
            f"{risk} risk"
        )

    with flow3:
        st.success("⚙️ Optimize")
        st.caption(
            f"{recommended_meals} meals"
        )

    with flow4:
        st.success("📷 Observe")
        st.caption(
            dominant_category
        )

    with flow5:
        st.success("🎯 Act")
        st.caption(
            f"{optimization['waste_reduction']:.2f} kg potential reduction"
        )       

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.html(
    """
    <div class="footer">

        <div class="footer-title">
            🌱 WasteWise AI
        </div>

        <br>

        Predict • Prevent • Optimize

        <br><br>

        AI-powered decision support for smarter cafeteria operations.

    </div>
    """
)