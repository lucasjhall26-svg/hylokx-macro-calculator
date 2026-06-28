import streamlit as st
from pathlib import Path

# =========================
# Brand configuration
# =========================
# After you upload logo.png to your GitHub repo, get the raw URL and paste it here
FALLBACK_LOGO_URL = "PUT_YOUR_RAW_GITHUB_LOGO_URL_HERE"

BACKGROUND_COLOR = "#0f0f0f"  # dark background
TEXT_COLOR = "#ffffff"        # main text
PRIMARY_COLOR = "#ff6b35"     # buttons/highlights (update to match your brand)
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
        h1, h2, h3, h4, h5, h6 {{
            color: {TEXT_COLOR};
        }}
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
        [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
            color: {TEXT_COLOR} !important;
        }}
        label, .stMarkdown p {{
            color: {TEXT_COLOR};
        }}
        .card {{
            background: rgba(255,255,255,0.04);
            padding: 1rem 1.2rem;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.08);
        }}
        .hint {{
            font-size: 0.9rem; opacity: 0.85;
        }}
    </style>
""", unsafe_allow_html=True)

# =========================
# Header with logo
# =========================
def render_header():
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    
    # Try multiple local paths first
    candidates = ["logo.png", "assets/logo.png", "static/logo.png"]
    shown = False
    for p in candidates:
        if Path(p).exists():
            st.image(p, use_column_width=True)
            shown = True
            break
    
    # If no local file, try permanent raw GitHub URL
    if not shown and FALLBACK_LOGO_URL != "PUT_YOUR_RAW_GITHUB_LOGO_URL_HERE":
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
    
    col0, col1, col2 = st.columns([1, 2, 2])
    
    with col0:
        weight_unit = st.radio("Weight units", ["kg", "lb"], horizontal=True)
    
    with col1:
        if weight_unit == "kg":
            weight_input = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, value=80.0, step=0.5)
        else:
            weight_input = st.number_input("Weight (lb)", min_value=70.0, max_value=660.0, value=176.0, step=1.0)
        height_cm = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=178.0, step=1.0)
    
    with col2:
        age = st.number_input("Age (years)", min_value=13, max_value=100, value=25, step=1)
        gender = st.selectbox("Gender", ["Male", "Female"])
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
    
    col3a, col3b, col4, col5 = st.columns([1.2, 1, 1.5, 1.5])
    
    with col3a:
        goal_type = st.selectbox("Goal", ["Cut (lose fat)", "Bulk (gain muscle)"])
    
    with col3b:
        goal_unit = st.radio("Goal units", ["kg", "lb"], horizontal=True)
    
    with col4:
        if goal_unit == "kg":
            weight_change_input = st.number_input("Weight change (kg)", min_value=0.5, max_value=50.0, value=5.0, step=0.5)
        else:
            weight_change_input = st.number_input("Weight change (lb)", min_value=1.0, max_value=110.0, value=11.0, step=1.0)
    
    with col5:
        timeframe = st.selectbox("Timeframe", ["6 weeks", "12 weeks", "18 weeks", "24 weeks"])
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")

st.subheader("⚙️ Macro Preferences")
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col_protein, col_fat = st.columns(2)
    
    with col_protein:
        st.markdown("**Protein:** Exactly 1.0 g per lb bodyweight")
        st.markdown("<div class='hint'>Standard for muscle building/preservation</div>", unsafe_allow_html=True)
    
    with col_fat:
        fat_pref = st.selectbox("Fat preference", ["Balanced (30%)", "Lower fat (25%)", "Higher fat (35%)"])
        fat_percent = {"Lower fat (25%)": 0.25, "Balanced (30%)": 0.30, "Higher fat (35%)": 0.35}[fat_pref]
        st.markdown("<div class='hint'>Carbs fill remaining calories</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# =========================
# Calculate
# =========================
if st.button("🔥 CALCULATE MY MACROS", use_container_width=True):
    
    # Convert weight to both kg and lb
    if weight_unit == "kg":
        weight_kg = weight_input
        weight_lb = weight_input * 2.20462
    else:
        weight_lb = weight_input
        weight_kg = weight_input / 2.20462
    
    # Convert weight change goal to kg
    if goal_unit == "kg":
        weight_change_kg = weight_change_input
        weight_change_lb = weight_change_input * 2.20462
    else:
        weight_change_lb = weight_change_input
        weight_change_kg = weight_change_input / 2.20462
    
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
    
    # TDEE (maintenance calories)
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
    
    # PROTEIN: exactly 1.0 g per lb
    protein_grams = round(weight_lb * 1.0)
    protein_cal = protein_grams * 4
    
    # FAT: % of goal calories
    fat_cal = goal_calories * fat_percent
    fat_grams = round(fat_cal / 9)
    
    # CARBS: remaining calories
    remaining_cal = goal_calories - (protein_cal + fat_cal)
    carb_grams = max(0, round(remaining_cal / 4))
    
    # Difficulty/risk assessment
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
    
    # Warning if macros don't fit
    warning_note = None
    if remaining_cal < 0:
        warning_note = (
            "Your target calories are too low for the selected protein and fat settings. "
            "Consider selecting a lower fat %, choosing a longer timeframe, or reducing your weekly weight change goal."
        )
    
    # =========================
    # Display Results
    # =========================
    st.subheader("📊 Your Results")
    
    # Maintenance calories
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("🔥 Maintenance Calories (TDEE)", f"{round(tdee)} cal/day")
        st.metric("🎯 Daily Target Calories", f"{round(goal_calories)} cal/day")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("")
    
    # Goal summary
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col_goal1, col_goal2, col_goal3 = st.columns(3)
        
        with col_goal1:
            st.metric("🎯 Goal", f"{goal_clean} {round(weight_change_kg, 1)} kg")
            st.caption(f"({round(weight_change_lb, 1)} lb)")
        
        with col_goal2:
            st.metric("📅 Timeframe", f"{timeframe_weeks} weeks")
            st.caption(f"{round(weekly_change, 2)} kg/week")
        
        with col_goal3:
            st.metric("⚡ Difficulty", difficulty)
        
        st.info(f"**Risk Level:** {risk}")
        
        if warning_note:
            st.warning(warning_note)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("")
    
    # Daily macros
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
        
        st.caption(f"Protein: 1.0 g/lb • Fat: {int(fat_percent*100)}% of calories • Carbs: remaining calories")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.success("✅ **Track these daily to reach your goal!**")
    st.markdown("Questions? Drop them in the **#macro-calculator** channel! 💬")

else:
    st.info("👆 Fill in your info above and click **CALCULATE MY MACROS**")

# Footer
st.markdown("---")
st.markdown("🔥 **HYLOKX** | Your transformation starts now")
