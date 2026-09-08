import streamlit as st
import requests

# ----------------------------------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Student Mental Health Predictor",
    page_icon="🧠",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/predict"

# ----------------------------------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------------------------------
st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
        }

        .app-header {
            text-align: center;
            padding: 1.5rem 1rem 1rem 1rem;
        }

        .app-header h1 {
            font-size: 2.4rem;
            font-weight: 800;
            color: #1f2937;
            margin-bottom: 0.2rem;
        }

        .app-header p {
            font-size: 1.05rem;
            color: #6b7280;
            margin-top: 0;
        }

        .section-card {
            background-color: #ffffff;
            border-radius: 16px;
            padding: 1.6rem 1.8rem;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
            margin-bottom: 1.2rem;
            border: 1px solid #eef0f3;
        }

        .section-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #111827;
            margin-bottom: 0.6rem;
        }

        .sub-heading {
            font-size: 1.02rem;
            font-weight: 600;
            color: #374151;
            margin-top: 1rem;
            margin-bottom: 0.4rem;
            border-left: 4px solid #6366f1;
            padding-left: 0.5rem;
        }

        div.stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
            color: white;
            font-weight: 700;
            font-size: 1.05rem;
            padding: 0.75rem 0;
            border-radius: 12px;
            border: none;
            margin-top: 1.2rem;
            transition: all 0.2s ease-in-out;
        }

        div.stButton > button:hover {
            opacity: 0.9;
            transform: translateY(-1px);
        }

        .result-placeholder {
            text-align: center;
            color: #6b7280;
            font-size: 1.05rem;
            padding: 3rem 1rem;
        }

        .result-card {
            text-align: center;
            padding: 2rem 1.5rem;
            border-radius: 16px;
            background: linear-gradient(135deg, #eef2ff, #f5f3ff);
            border: 1px solid #e0e7ff;
            margin-top: 0.5rem;
        }

        .result-label {
            font-size: 1.1rem;
            font-weight: 600;
            color: #4b5563;
            margin-bottom: 0.4rem;
        }

        .result-score {
            font-size: 3.2rem;
            font-weight: 800;
            color: #4f46e5;
            margin: 0.2rem 0 0.8rem 0;
        }

        .interpretation-box {
            font-size: 1rem;
            color: #374151;
            background-color: #ffffff;
            border-radius: 10px;
            padding: 0.9rem 1.1rem;
            margin-top: 0.8rem;
            text-align: left;
            border: 1px solid #eef0f3;
        }

        .disclaimer {
            font-size: 0.85rem;
            color: #9ca3af;
            text-align: center;
            margin-top: 1.5rem;
            padding-top: 0.8rem;
            border-top: 1px solid #eef0f3;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown("""
    <div class="app-header">
        <h1>🧠 Student Mental Health Predictor</h1>
        <p>Analyze student lifestyle and social media habits to predict a mental health score.</p>
    </div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------------
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None
if "prediction_error" not in st.session_state:
    st.session_state.prediction_error = None

# ----------------------------------------------------------------------------
# MAIN LAYOUT — TWO COLUMNS
# ----------------------------------------------------------------------------
left_col, right_col = st.columns([1.1, 1], gap="large")

# ============================================================================
# LEFT CONTAINER — USER INPUT
# ============================================================================
with left_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📝 Student Information</div>', unsafe_allow_html=True)

    # ---- Personal Information ----
    st.markdown('<div class="sub-heading">Personal Information</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    with p1:
        age = st.number_input("Age", min_value=10, max_value=100, value=21, step=1)
    with p2:
        gender = st.selectbox("Gender", ["Male", "Female"])

    country = st.text_input("Country", value="Pakistan")

    academic_level = st.selectbox(
        "Academic Level",
        ["Undergraduate", "Graduate", "High School"]
    )

    # ---- Social Media Usage ----
    st.markdown('<div class="sub-heading">Social Media Usage</div>', unsafe_allow_html=True)
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

    s1, s2 = st.columns(2)
    with s1:
        avg_daily_usage_hours = st.number_input(
            "Average Daily Usage (hours)", min_value=0.0, max_value=24.0, value=4.5, step=0.5
        )
    with s2:
        daily_unlocks = st.number_input(
            "Daily Unlocks", min_value=0, value=60, step=1
        )

    # ---- Lifestyle Information ----
    st.markdown('<div class="sub-heading">Lifestyle Information</div>', unsafe_allow_html=True)
    l1, l2 = st.columns(2)
    with l1:
        study_hours = st.number_input(
            "Study Hours Per Day", min_value=0.0, max_value=24.0, value=3.0, step=0.5
        )
    with l2:
        physical_activity_hours = st.number_input(
            "Physical Activity (hours)", min_value=0.0, max_value=24.0, value=1.0, step=0.5
        )

    l3, l4 = st.columns(2)
    with l3:
        sleep_hours_per_night = st.number_input(
            "Sleep Hours Per Night", min_value=0.0, max_value=24.0, value=7.5, step=0.5
        )
    with l4:
        stress_level = st.selectbox(
            "Stress Level", ["Low", "Medium", "High", "Very High"]
        )

    predict_clicked = st.button("🔮 Predict Mental Health Score")

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# HANDLE PREDICTION REQUEST
# ----------------------------------------------------------------------------
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

    with st.spinner("Contacting prediction model..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=10)

            if response.status_code == 200:
                data = response.json()
                score = data.get("predicted_mental_health_score")
                if score is not None:
                    st.session_state.prediction_result = score
                else:
                    st.session_state.prediction_error = (
                        "The API response did not contain a 'predicted_mental_health_score' field."
                    )
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

# ============================================================================
# RIGHT CONTAINER — RESULT
# ============================================================================
with right_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Prediction Result</div>', unsafe_allow_html=True)

    if st.session_state.prediction_error:
        st.error(st.session_state.prediction_error)

    elif st.session_state.prediction_result is not None:
        score = st.session_state.prediction_result

        if score < 40:
            interpretation = (
                "Low mental health score. Consider paying more attention to stress, "
                "sleep, and overall lifestyle."
            )
        elif score <= 70:
            interpretation = (
                "Moderate mental health score. There may be room for improvement "
                "in lifestyle balance."
            )
        else:
            interpretation = (
                "Good mental health score based on the provided lifestyle and "
                "social media habits."
            )

        st.markdown(f"""
            <div class="result-card">
                <div class="result-label">Predicted Mental Health Score</div>
                <div class="result-score">{score:.2f}</div>
                <div class="interpretation-box">{interpretation}</div>
            </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
            <div class="result-placeholder">
                👈 Enter your information and click the prediction button
                to see the result.
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class="disclaimer">
            ⚠️ This prediction is generated by a machine learning model and is for
            educational purposes only. It should not be considered a professional
            medical diagnosis.
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
