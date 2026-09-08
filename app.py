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
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        padding: 2rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        justify-content: center;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
    }

    .app-header h1 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .app-header p {
        color: #dbe4ff;
        font-size: 1.05rem;
        margin: 0;
    }

    div[class*="st-key-input_card"],
    div[class*="st-key-result_card"] {
        border-radius: 16px;
        padding: 1.8rem 1.8rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.2rem;
        min-height: 850px;
        display: flex;
        flex-direction: column;
    }

    div[class*="st-key-input_card"] {
        background-color: #ffffff;
        border: 1px solid #eef0f4;
    }

    div[class*="st-key-result_card"] {
        background-color: #ffffff;
        border: 1px solid #eef0f4;
    }

    div[class*="st-key-input_card"] h2,
    div[class*="st-key-result_card"] h2 {
        font-size: 1.4rem;
        font-weight: 700;
        color: #182848;
        margin-bottom: 1rem;
        border-bottom: 2px solid #f0f2f6;
        padding-bottom: 0.6rem;
    }

    .section-label {
        font-size: 1.0rem;
        font-weight: 600;
        color: #4b6cb7;
        margin-top: 1.0rem;
        margin-bottom: 0.4rem;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
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

    .result-placeholder {
        text-align: center;
        color: #6b7280;
        font-size: 1.05rem;
        padding: 3rem 1rem;
    }

    .score-card {
        text-align: center;
        padding: 1.5rem 1rem 2rem 1rem;
    }

    .score-label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #4b5563;
        margin-bottom: 0.5rem;
    }

    .score-value {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .interpretation-box {
        background-color: #f0f4ff;
        border-left: 5px solid #4b6cb7;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        color: #1f2937;
        font-size: 1.0rem;
        margin-top: 1rem;
        text-align: left;
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

    with st.spinner("Analyzing student data and generating prediction..."):
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

# ---------------------------------------------------------
# RIGHT CONTAINER — RESULT
# ---------------------------------------------------------
with right_col:
    with st.container(key="result_card"):
        st.markdown("<h2>📊 Prediction Result</h2>", unsafe_allow_html=True)

        if st.session_state.prediction_error:
            st.error(st.session_state.prediction_error)

        elif st.session_state.prediction_result is not None:
            score = st.session_state.prediction_result

            if score < 4.0:
                interpretation = (
                    "Low mental health score. Consider paying more attention to "
                    "stress, sleep, and overall lifestyle."
                )
                emoji = "🔴"
            elif 4.0 <= score <= 7.0:
                interpretation = (
                    "Moderate mental health score. There may be room for "
                    "improvement in lifestyle balance."
                )
                emoji = "🟡"
            else:
                interpretation = (
                    "Good mental health score based on the provided lifestyle "
                    "and social media habits."
                )
                emoji = "🟢"

            st.markdown(
                f"""
                <div class="score-card">
                    <div class="score-label">Predicted Mental Health Score</div>
                    <div class="score-value">{score:.2f}</div>
                    <div style="font-size: 2rem;">{emoji}</div>
                    <div class="interpretation-box">{interpretation}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.markdown(
                """
                <div class="result-placeholder">
                    👈 Enter your information and click the prediction button
                    to see the result.
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
