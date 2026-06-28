import streamlit as st

# =========================
# Brand configuration
# =========================
# If you uploaded logo.png to your GitHub repo root, this will load it.
# If not found, it will try the fallback URL below.
FALLBACK_LOGO_URL = "https://media.discordapp.net/attachments/1519907891266719784/1520697995400581230/hylokx.jpg?format=webp&width=894&height=503"

# Set your brand colors here (update these when you have exact hex codes)
BACKGROUND_COLOR = "#0f0f0f"  # dark background
TEXT_COLOR = "#ffffff"        # main text
PRIMARY_COLOR = "#ff6b35"     # buttons/highlights (change to your brand)
ACCENT_COLOR = "#ffa500"      # optional accent

# =========================
# Page config
# =========================
st.set_page_config(page_title="HYLOKX Macro Calculator", page_icon="💪", layout="centered")

# Inject global style (background, buttons, text)
st.markdown(f"""
    <style>
        .stApp {{
            background: {BACKGROUND_COLOR};
            color: {TEXT_COLOR};
        }}
        /* Headings */
        h1, h2, h3, h4, h5, h6 {{
            color: {TEXT_COLOR};
        }}
        /* Buttons */
        div.stButton > button {{
            background-color: {PRIMARY_COLOR};
            color: #ffffff;
            border: 0;
            border-radius: 10px;
            padding: 0.6rem 1rem;
            font-weight: 700;
        }}
        div.stButton > button:hover {{
            filter: brightness(1.05);
        }}
        /* Metrics */
        [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
            color: {TEXT_COLOR} !important;
        }}
        /* Inputs - make labels readable */
        label, .stMarkdown p {{
            color: {TEXT_COLOR};
        }}
        /* Card-style sections */
        .card {{
            background: rgba(255,255,255,0.04);
            padding: 1rem 1.2rem;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.08);
        }}
    </style>
""", unsafe_allow_html=True)

# =========================
# Header with logo
# =========================
def render_header():
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    # Try to load local logo.png first (recommended). If not available, use fallback URL.
    try:
        st.image("logo.png", use_column_width=True)
    except Exception:
        st.image(FALLBACK_LOGO_URL, use_column_width=True)
    st.markdown(
        "<div style='text-align:center; font-weight:800; font-size:22px; margin-top:-6px;'>HYLOKX MACRO CALCULATOR</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

render_header()
st.markdown("---")

# =========================
# Inputs
# =========================
st.subheader("📋 Your Information")
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        weight_kg = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.5)
        height_cm = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0, step=1.0)
    with col2:
        age = st.number_input("Age (years)", min_value=13, max_value=100, value=25, step=1)
        activity_level = st.selectbox(
            "Activity Level",
            [
                "Sedentary (little/no exercise)",
                "Light (1-3 days/week)",
                "Moderate (3-5 days/week)",
                "Active (6-7 days/week)",
                "Very Active (physical job + training)"
            ]
        )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")

st.subheader("🎯 Your Goal")
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col3, col4, col5 = st.columns(3)
    with col3:
        goal_type = st.selectbox("Goal", ["Cut (lose fat)", "Bulk (gain muscle)"])
    with col4:
        weight_change_kg = st.number_input("Weight change (kg)", min_value=0.5, max_value=50.0, value=5.0, step=0.5)
    with col5:
        timeframe = st.selectbox("Timeframe", ["6 weeks", "12 weeks", "18 weeks", "24 weeks"])
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# =========================
# Calculate
# =========================
if st.button("🔥 CALCULATE MY MACROS", use_container_width=True):
    # BMR (Mifflin-St Jeor)
    if gender == "Male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    # Activity multipliers
    activity_multipliers = {
        "Sedentary (little/no exercise)": 1.2,
        "Light (1-3 days/week)": 1.375,
        "Moderate (3-5 days/week)": 1.55,
        "Active (6-7 days/week)": 1.725,
        "Very Active (physical job + training)": 1.9
    }

    # TDEE
    tdee = bmr * activity_multipliers[activity_level]

    # Goal calories
    timeframe_weeks = int(timeframe.split()[0])
    total_calorie_change = weight_change_kg * 7700
    daily_calorie_change = total_calorie_change / (timeframe_weeks * 7)

    if "Cut" in goal_type:
        goal_calories = tdee - daily_calorie_change
        goal_clean = "Cut"
    else:
        goal_calories = tdee + daily_calorie_change
        goal_clean = "Bulk"

    # Macro splits
    if goal_clean == "Cut":
        protein_ratio = 0.35
        carb_ratio = 0.35
        fat_ratio = 0.30
    else:  # Bulk
        protein_ratio = 0.30
        carb_ratio = 0.40
        fat_ratio = 0.30

    # Grams
    protein_grams = round((goal_calories * protein_ratio) / 4)
    carb_grams = round((goal_calories * carb_ratio) / 4)
    fat_grams = round((goal_calories * fat_ratio) / 9)

    # Difficulty/risk
    weekly_change = weight_change_kg / timeframe_weeks
    if weekly_change < 0.5:
        difficulty = "🟢 SUSTAINABLE"
        risk = "Low risk - healthy pace"
    elif weekly_change < 1.0:
        difficulty = "🟡 MODERATE"
        risk = "Medium intensity - manageable"
    else:
        difficulty = "🔴 AGGRESSIVE"
        risk = "High intensity - requires discipline"

    # =========================
    # Output
    # =========================
    st.subheader("📊 Your Results")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("🔥 Maintenance Calories (TDEE)", f"{round(tdee)} cal/day")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col_goal1, col_goal2, col_goal3 = st.columns(3)
        with col_goal1:
            st.metric("🎯 Goal", f"{goal_clean} {weight_change_kg} kg")
        with col_goal2:
            st.metric("📅 Timeframe", f"{timeframe_weeks} weeks")
        with col_goal3:
            st.metric("⚡ Difficulty", difficulty)
        st.info(f"Risk Level: {risk}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🍽️ Daily Calorie Target")
        st.success(f"## {round(goal_calories)} calories/day")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 💪 Daily Macros")
        col_macro1, col_macro2, col_macro3 = st.columns(3)
        with col_macro1:
            st.metric("🥩 Protein", f"{protein_grams} g")
        with col_macro2:
            st.metric("🍚 Carbs", f"{carb_grams} g")
        with col_macro3:
            st.metric("🥑 Fats", f"{fat_grams} g")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("Questions? Drop them in the #macro-calculator channel! 💬")

else:
    st.info("👆 Fill in your info above and click CALCULATE MY MACROS")

st.markdown("---")
st.markdown("🔥 **HYLOKX** | Your transformation starts now")
