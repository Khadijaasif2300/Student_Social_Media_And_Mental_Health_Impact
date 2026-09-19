import streamlit as st
import requests

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Student Mental Health Predictor",
    page_icon="🧠",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/predict"

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f7fa;
    }

    .app-header {
        background: #fff;
        margin-bottom: 5rem;
        justify-content: center;
        text-align: center;
    }

    .app-header h1 {
        color: #1f4438;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .app-header p {
        color: #1f4438;
        font-size: 1.05rem;
        margin: 0;
    }

    div[class*="st-key-input_card"] {
        border-radius: 16px;
        padding: 1.8rem 1.8rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.2rem;
        min-height: 850px;
        display: flex;
        flex-direction: column;
        background-color: #ffffff;
        border: 1px solid #eef0f4;
    }

    div[class*="st-key-input_card"] h2 {
        font-size: 1.4rem;
        font-weight: 700;
        color: #182848;
        margin-bottom: 1rem;
        border-bottom: 2px solid #f0f2f6;
        padding-bottom: 0.6rem;
    }

    /* ---- Result card: dark "signal" gauge theme ---- */
    div[class*="st-key-result_card"] {
        border-radius: 20px;
        padding: 0;
        box-shadow: 0 8px 24px rgba(10, 25, 20, 0.35);
        margin-bottom: 1.2rem;
        min-height: 850px;
        display: flex;
        flex-direction: column;
        background: radial-gradient(120% 120% at 50% 0%, #1f4438 0%, #142e26 45%, #0b1c17 100%);
        border: 1px solid rgba(255, 255, 255, 0.06);
        overflow: hidden;
        position: relative;
    }

    .signal-inner {
        padding: 2rem 2rem 1.5rem 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        flex: 1;
        color: #e9e7dc;
    }

    .signal-title {
        font-family: Georgia, 'Times New Roman', serif;
        font-style: italic;
        font-size: 2.1rem;
        font-weight: 400;
        color: #f4f1e6;
        margin-bottom: 0.4rem;
        letter-spacing: 0.5px;
    }

    .signal-subtitle {
        font-size: 0.92rem;
        color: #b7c8bf;
        max-width: 320px;
        line-height: 1.4;
        margin-bottom: 1.5rem;
    }

    .gauge-wrap {
        position: relative;
        width: 280px;
        height: 200px;
        margin: 0.5rem auto 1rem auto;
    }

    .gauge-caption {
        font-size: 0.85rem;
        color: #cfe0d7;
        margin-top: -0.3rem;
        margin-bottom: 0.2rem;
    }

    .gauge-subcaption {
        font-size: 0.8rem;
        color: #8fa79b;
        margin-bottom: 1.2rem;
    }

    .gauge-score-text {
        font-family: Georgia, 'Times New Roman', serif;
        font-size: 2.6rem;
        font-weight: 700;
        fill: #f4f1e6;
    }

    .gauge-score-max {
        font-size: 1rem;
        fill: #8fa79b;
    }

    .section-label {
        font-size: 1.0rem;
        font-weight: 600;
        color: #1f4438;
        margin-top: 1.0rem;
        margin-bottom: 0.4rem;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #1f4438 100%, #142e26 0%);
        color: white;
        font-size: 1.1rem;
        font-weight: 700;
        padding: 0.8rem 0.8rem;
        border-radius: 12px;
        border: none;
        margin-top: 1.5rem;
        transition: all 0.2s ease-in-out;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(24, 40, 72, 0.35);
        color: white;
    }

    .signal-interpretation {
        background-color: rgba(255, 255, 255, 0.06);
        border-left: 4px solid #8fd6b4;
        padding: 0.9rem 1.1rem;
        border-radius: 10px;
        color: #eef2ee;
        font-size: 0.95rem;
        margin-top: 0.5rem;
        text-align: left;
        max-width: 340px;
    }

    .disclaimer {
        font-size: 0.85rem;
        color: #9ca3af;
        text-align: center;
        margin-top: 2rem;
        padding: 0.8rem;
        border-top: 1px solid #e5e7eb;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HEADER
# =========================================================
st.markdown(
    """
    <div class="app-header">
        <h1>🧠 Student Mental Health Predictor</h1>
        <p>Analyze student lifestyle and social media habits to predict a mental health score.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SESSION STATE
# =========================================================
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None
if "prediction_error" not in st.session_state:
    st.session_state.prediction_error = None


# =========================================================
# GAUGE HELPER
# =========================================================
def render_gauge_svg(score, max_score=10.0):
    """
    Renders a semicircle 'dial' gauge (0 to max_score) as inline SVG,
    styled to match the dark signal-card theme.
    score = None -> empty/zero gauge (placeholder state)
    """
    import math

    clamped = 0.0 if score is None else max(0.0, min(float(score), max_score))
    pct = clamped / max_score

    cx, cy, r = 140, 150, 100
    start_angle = 180  # left
    end_angle = 0       # right (going over the top)

    def polar_to_xy(angle_deg):
        angle_rad = math.radians(angle_deg)
        x = cx + r * math.cos(angle_rad)
        y = cy - r * math.sin(angle_rad)
        return x, y

    # Track (full arc, left to right over the top)
    x1, y1 = polar_to_xy(start_angle)
    x2, y2 = polar_to_xy(end_angle)
    track_path = f"M {x1:.2f},{y1:.2f} A {r},{r} 0 0 1 {x2:.2f},{y2:.2f}"

    # Progress arc
    progress_angle = start_angle - (start_angle - end_angle) * pct
    xp, yp = polar_to_xy(progress_angle)
    large_arc = 1 if (start_angle - progress_angle) > 180 else 0
    progress_path = f"M {x1:.2f},{y1:.2f} A {r},{r} 0 {large_arc} 1 {xp:.2f},{yp:.2f}"

    circumference = math.pi * r
    score_display = "0.0" if score is None else f"{clamped:.1f}"
    needle_color = "#8fd6b4" if score is not None else "#33564a"

    svg = f"""
    <svg viewBox="0 0 280 190" width="280" height="190" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#4f8f76"/>
                <stop offset="100%" stop-color="#a9e4c6"/>
            </linearGradient>
        </defs>
        <path d="{track_path}" fill="none" stroke="#2a4a3f" stroke-width="10" stroke-linecap="round"/>
        <path d="{progress_path}" fill="none" stroke="url(#gaugeGrad)" stroke-width="10" stroke-linecap="round"/>
        <circle cx="{xp:.2f}" cy="{yp:.2f}" r="7" fill="{needle_color}" stroke="#0b1c17" stroke-width="2"/>
        <text x="140" y="140" text-anchor="middle" class="gauge-score-text" font-family="Georgia, 'Times New Roman', serif">{score_display}</text>
        <text x="140" y="165" text-anchor="middle" class="gauge-score-max" font-family="Georgia, 'Times New Roman', serif">/ {int(max_score)}</text>
    </svg>
    """
    return svg


# =========================================================
# MAIN LAYOUT — TWO COLUMNS
# =========================================================
left_col, right_col = st.columns([1.2, 1], gap="large")

# ---------------------------------------------------------
# LEFT CONTAINER — USER INPUT
# ---------------------------------------------------------
with left_col:
    with st.container(key="input_card"):
        st.markdown("<h2>📝 Student Information</h2>", unsafe_allow_html=True)

        # ---- Personal Information ----
        st.markdown('<div class="section-label">Personal Information</div>', unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1:
            age = st.number_input("Age", min_value=10, max_value=100, value=21, step=1)
            gender = st.selectbox("Gender", ["Male", "Female"])
        with p2:
            country = st.text_input("Country", value="India")
            academic_level = st.selectbox("Academic Level", ["Undergraduate", "Graduate", "High School"])

        # ---- Social Media Usage ----
        st.markdown('<div class="section-label">Social Media Usage</div>', unsafe_allow_html=True)
        s1, s2 = st.columns(2)
        with s1:
            most_used_platform = st.selectbox(
                "Most Used Social Media Platform",
                [
                    "Facebook", "LinkedIn", "Instagram", "Snapchat", "Twitter",
                    "YouTube", "TikTok", "LINE", "KakaoTalk", "VKontakte",
                    "WhatsApp", "WeChat"
                ]
            )
            purpose_of_use = st.selectbox(
                "Purpose of Social Media Use",
                ["Networking", "Education", "Entertainment", "News"]
            )
        with s2:
            avg_daily_usage_hours = st.number_input(
                "Average Daily Social Media Usage (hours)",
                min_value=0.0, max_value=24.0, value=4.5, step=0.5
            )
            daily_unlocks = st.number_input(
                "Daily Phone Unlocks", min_value=0, value=62, step=1
            )

        # ---- Lifestyle Information ----
        st.markdown('<div class="section-label">Lifestyle Information</div>', unsafe_allow_html=True)
        l1, l2, l3 = st.columns(3)
        with l1:
            study_hours = st.number_input(
                "Study Hours Per Day", min_value=0.0, max_value=24.0, value=3.0, step=0.5
            )
        with l2:
            physical_activity_hours = st.number_input(
                "Physical Activity (hours)", min_value=0.0, max_value=24.0, value=1.0, step=0.5
            )
        with l3:
            sleep_hours_per_night = st.number_input(
                "Sleep Hours Per Night", min_value=0.0, max_value=24.0, value=7.5, step=0.5
            )

        stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High", "Very High"])

        predict_clicked = st.button("🔮 Predict Mental Health Score")

# ---------------------------------------------------------
# HANDLE PREDICTION REQUEST
# ---------------------------------------------------------
if predict_clicked:
    payload = {
        "age": age,
        "gender": gender,
        "country": country,
        "academic_level": academic_level,
        "most_used_platform": most_used_platform,
        "purpose_of_use": purpose_of_use,
        "avg_daily_usage_hours": avg_daily_usage_hours,
        "daily_unlocks": daily_unlocks,
        "study_hours": study_hours,
        "physical_activity_hours": physical_activity_hours,
        "sleep_hours_per_night": sleep_hours_per_night,
        "stress_level": stress_level
    }

    st.session_state.prediction_result = None
    st.session_state.prediction_error = None

    with st.spinner("Reading the signal... running your habits through the model."):
        try:
            response = requests.post(API_URL, json=payload, timeout=10)

            if response.status_code == 200:
                data = response.json()
                score = data.get("predicted_mental_health_score")
                if score is None:
                    st.session_state.prediction_error = (
                        "The API response did not contain 'predicted_mental_health_score'."
                    )
                else:
                    st.session_state.prediction_result = score
            else:
                st.session_state.prediction_error = (
                    f"API returned an error (status code {response.status_code}): {response.text}"
                )

        except requests.exceptions.ConnectionError:
            st.session_state.prediction_error = (
                "Unable to connect to the prediction API. "
                "Please make sure the FastAPI backend is running at "
                "http://127.0.0.1:8000."
            )
        except requests.exceptions.Timeout:
            st.session_state.prediction_error = (
                "The request to the prediction API timed out. Please try again."
            )
        except Exception as e:
            st.session_state.prediction_error = f"An unexpected error occurred: {e}"


# RIGHT CONTAINER — RESULT (dark "Mental Health Signal" gauge card)


with right_col:
    with st.container(key="result_card"):

        if st.session_state.prediction_error:
            st.markdown('<div class="signal-inner">', unsafe_allow_html=True)
            st.markdown('<div class="signal-title">Mental Health Signal</div>', unsafe_allow_html=True)
            st.error(st.session_state.prediction_error)
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.prediction_result is not None:
            score = st.session_state.prediction_result

            # score is assumed to be on a 0-10 scale; adjust max_score if your
            # model actually outputs a different range.
            if score < 4.0:
                interpretation = (
                    "Low mental health score. Consider paying more attention to "
                    "stress, sleep, and overall lifestyle."
                )
            elif 4.0 <= score <= 7.0:
                interpretation = (
                    "Moderate mental health score. There may be room for "
                    "improvement in lifestyle balance."
                )
            else:
                interpretation = (
                    "Good mental health score based on the provided lifestyle "
                    "and social media habits."
                )

            gauge_svg = render_gauge_svg(score, max_score=10.0)

            st.markdown(
                f"""
                <div class="signal-inner">
                    <div class="signal-title">Mental Health Signal</div>
                    <div class="signal-subtitle">
                        A quick read on how habits, screen time, and stress are
                        trending — modeled from your daily rhythm, not a diagnosis.
                    </div>
                    <div class="gauge-wrap">{gauge_svg}</div>
                    <div class="gauge-caption">Your predicted score</div>
                    <div class="signal-interpretation">{interpretation}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            gauge_svg = render_gauge_svg(None, max_score=10.0)
            st.markdown(
                f"""
                <div class="signal-inner">
                    <div class="signal-title">Mental Health Signal</div>
                    <div class="signal-subtitle">
                        A quick read on how habits, screen time, and stress are
                        trending — modeled from your daily rhythm, not a diagnosis.
                    </div>
                    <div class="gauge-wrap">{gauge_svg}</div>
                    <div class="gauge-caption">Your score will appear here</div>
                    <div class="gauge-subcaption">
                        Fill in the form and submit to generate a predicted
                        mental health score from 0–10.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================================================
# DISCLAIMER
# =========================================================
st.markdown(
    """
    <div class="disclaimer">
        ⚠️ This prediction is generated by a machine learning model and is intended
        for educational purposes only. It should not be considered a professional
        medical diagnosis. If you are struggling with your mental health, please
        reach out to a qualified professional.
    </div>
    """,
    unsafe_allow_html=True
)