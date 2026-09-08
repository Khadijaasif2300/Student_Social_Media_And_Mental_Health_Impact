import streamlit as st
import requests


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Student Mental Health Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# FASTAPI URL
# =========================================================

API_URL = "http://127.0.0.1:8000/predict"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* =====================================================
   MAIN PAGE
   ===================================================== */

.stApp {
    background: #f8fafc;
}

.main .block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* =====================================================
   HEADER
   ===================================================== */

.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: 750;
    margin-bottom: 5px;
    color: #1e293b;
}

.main-subtitle {
    text-align: center;
    font-size: 16px;
    color: #64748b;
    margin-bottom: 30px;
}


/* =====================================================
   COLUMN SPACING & EQUAL-HEIGHT AUTO-MATCH
   ===================================================== */

/* 1. Make the row stretch its two columns to equal height */
div[data-testid="stHorizontalBlock"] {
    align-items: stretch !important;
    gap: 1.5rem !important;
}

/* 2. Make each column a flex column so ITS child can grow to fill it */
div[data-testid="stColumn"] {
    display: flex;
    flex-direction: column;
}

/* 3. Propagate that flex-fill down through Streamlit's wrapper divs */
div[data-testid="stColumn"] > div,
div[data-testid="stColumn"] [data-testid="stVerticalBlockBorderWrapper"] {
    flex: 1;
    display: flex;
    flex-direction: column;
}


/* =====================================================
   INPUT AND RESULT CARDS
   ===================================================== */

/* 4. Your cards — now flex:1 actually has an ancestor to grow inside */
.st-key-input_card,
.st-key-result_card {
    flex: 1;
    display: flex;
    flex-direction: column;
    box-sizing: border-box !important;
    border-radius: 18px !important;
    padding: 1.2rem 1.3rem !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow:
        0 4px 12px rgba(0, 0, 0, 0.04),
        0 10px 30px rgba(0, 0, 0, 0.05) !important;
    overflow-y: auto !important;
}


/* =====================================================
   LEFT CARD
   ===================================================== */

.st-key-input_card {
    background: #ffffff !important;
}


/* =====================================================
   RIGHT CARD
   ===================================================== */

.st-key-result_card {
    background: linear-gradient(
        135deg,
        #eef2ff 0%,
        #f5f3ff 100%
    ) !important;
    justify-content: center; /* centers the result content vertically */
    overflow: hidden !important;
}


/* =====================================================
   SECTION HEADINGS
   ===================================================== */

.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #334155;
    border-left: 5px solid #6366f1;
    padding-left: 12px;
    margin-top: 10px;
    margin-bottom: 18px;
}


/* =====================================================
   RESULT CONTENT
   ===================================================== */

.result-content {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    box-sizing: border-box;
    padding: 2rem;
}

.result-icon {
    font-size: 58px;
    margin-bottom: 12px;
}

.result-title {
    font-size: 27px;
    font-weight: 700;
    color: #334155;
    margin-bottom: 10px;
}

.result-score {
    font-size: 64px;
    font-weight: 800;
    color: #6366f1;
    line-height: 1;
    margin: 15px 0;
}

.result-label {
    font-size: 16px;
    color: #64748b;
    margin-bottom: 20px;
}

.result-description {
    max-width: 430px;
    font-size: 16px;
    line-height: 1.6;
    color: #475569;
}


/* =====================================================
   DISCLAIMER
   ===================================================== */

.disclaimer {
    margin-top: 30px;
    padding: 12px 16px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.7);
    border: 1px solid #e2e8f0;
    color: #64748b;
    font-size: 13px;
    line-height: 1.5;
    max-width: 500px;
}


/* =====================================================
   BUTTON
   ===================================================== */

div.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(
        90deg,
        #6366f1,
        #8b5cf6
    );
    color: white;
    font-size: 17px;
    font-weight: 650;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 8px 20px rgba(99, 102, 241, 0.25);
}


/* =====================================================
   INPUT LABELS
   ===================================================== */

label {
    color: #475569 !important;
    font-weight: 500 !important;
}


/* =====================================================
   SUCCESS MESSAGE
   ===================================================== */

.success-box {
    padding: 12px 18px;
    border-radius: 10px;
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    color: #047857;
    font-size: 15px;
    margin-top: 15px;
}


/* =====================================================
   RESPONSIVE DESIGN
   ===================================================== */

@media (max-width: 900px) {

    .main-title {
        font-size: 30px;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="main-title">
🧠 Student Mental Health Predictor
</div>
<div class="main-subtitle">
Predict a student's mental health score based on
social media usage, academic lifestyle, and daily habits.
</div>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "prediction_status" not in st.session_state:
    st.session_state.prediction_status = None


# =========================================================
# TWO COLUMNS
# =========================================================

col1, col2 = st.columns(
    2,
    gap="large"
)


# =========================================================
# LEFT COLUMN — INPUTS
# =========================================================

with col1:

    with st.container(
        border=True,
        key="input_card"
    ):

        # -------------------------------------------------
        # PERSONAL INFORMATION
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">Personal Information</div>',
            unsafe_allow_html=True
        )

        age = st.number_input(
            "Age",
            min_value=10,
            max_value=100,
            value=21,
            step=1
        )

        gender = st.selectbox(
            "Gender",
            [
                "Female",
                "Male"
            ]
        )

        country = st.selectbox(
            "Country",
            [
                "Other",
                "India",
                "USA",
                "Canada",
                "Australia",
                "UK",
                "Germany",
                "Mexico",
                "Turkey",
                "France"
            ]
        )


        # -------------------------------------------------
        # ACADEMIC & SOCIAL MEDIA INFORMATION
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">Academic &amp; Social Media</div>',
            unsafe_allow_html=True
        )

        academic_level = st.selectbox(
            "Academic Level",
            [
                "Undergraduate",
                "Graduate",
                "High School"
            ]
        )

        most_used_platform = st.selectbox(
            "Most Used Social Media Platform",
            [
                "Facebook",
                "LinkedIn",
                "Instagram",
                "Snapchat",
                "Twitter",
                "YouTube",
                "TikTok",
                "LINE",
                "KakaoTalk",
                "VKontakte",
                "WhatsApp",
                "WeChat"
            ]
        )

        purpose_of_use = st.selectbox(
            "Purpose of Social Media Use",
            [
                "Networking",
                "Education",
                "Entertainment",
                "News"
            ]
        )


        # -------------------------------------------------
        # SOCIAL MEDIA USAGE
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">Social Media Usage</div>',
            unsafe_allow_html=True
        )

        usage_col1, usage_col2 = st.columns(2)

        with usage_col1:

            avg_daily_usage_hours = st.number_input(
                "Average Daily Usage (hours)",
                min_value=0.0,
                max_value=24.0,
                value=4.5,
                step=0.5,
                format="%.2f"
            )

        with usage_col2:

            daily_unlocks = st.number_input(
                "Daily Unlocks",
                min_value=0,
                max_value=1000,
                value=60,
                step=1
            )


        # -------------------------------------------------
        # LIFESTYLE INFORMATION
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">Lifestyle Information</div>',
            unsafe_allow_html=True
        )

        lifestyle_col1, lifestyle_col2 = st.columns(2)

        with lifestyle_col1:

            study_hours = st.number_input(
                "Study Hours Per Day",
                min_value=0.0,
                max_value=24.0,
                value=3.0,
                step=0.5,
                format="%.2f"
            )

            sleep_hours_per_night = st.number_input(
                "Sleep Hours Per Night",
                min_value=0.0,
                max_value=24.0,
                value=7.5,
                step=0.5,
                format="%.2f"
            )

        with lifestyle_col2:

            physical_activity_hours = st.number_input(
                "Physical Activity (hours)",
                min_value=0.0,
                max_value=24.0,
                value=1.0,
                step=0.5,
                format="%.2f"
            )

            stress_level = st.selectbox(
                "Stress Level",
                [
                    "Low",
                    "Medium",
                    "High",
                    "Very High"
                ]
            )


        # -------------------------------------------------
        # PREDICT BUTTON
        # -------------------------------------------------

        st.write("")

        predict_button = st.button(
            "🔮 Predict Mental Health Score",
            use_container_width=True
        )


        # -------------------------------------------------
        # SEND DATA TO FASTAPI
        # -------------------------------------------------

        if predict_button:

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

            try:

                with st.spinner("Analyzing student information..."):

                    response = requests.post(
                        API_URL,
                        json=payload,
                        timeout=30
                    )

                if response.status_code == 200:

                    result = response.json()
                    score = result["predicted_mental_health_score"]

                    st.session_state.prediction = score
                    st.session_state.prediction_status = "success"

                else:

                    st.session_state.prediction = None
                    st.session_state.prediction_status = (
                        f"API Error: {response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                st.session_state.prediction = None
                st.session_state.prediction_status = (
                    "Could not connect to FastAPI."
                )

            except requests.exceptions.Timeout:

                st.session_state.prediction = None
                st.session_state.prediction_status = (
                    "The API request timed out."
                )

            except Exception as e:

                st.session_state.prediction = None
                st.session_state.prediction_status = f"Error: {str(e)}"


# =========================================================
# RIGHT COLUMN — RESULT
# =========================================================

with col2:

    with st.container(
        border=True,
        key="result_card"
    ):

        # -------------------------------------------------
        # NO PREDICTION YET
        # -------------------------------------------------

        if st.session_state.prediction is None:

            st.markdown("""
<div class="result-content">
<div class="result-icon">🧠</div>
<div class="result-title">Mental Health Score</div>
<div class="result-score">—</div>
<div class="result-label">Your prediction will appear here</div>
<div class="result-description">
Enter the student's information on the left and click
<b>Predict Mental Health Score</b> to generate a prediction.
</div>
<div class="disclaimer">
<b>Note:</b> This prediction is for educational and informational
purposes only. It is not a medical diagnosis or a substitute for
professional mental health advice.
</div>
</div>
""", unsafe_allow_html=True)


        # -------------------------------------------------
        # PREDICTION AVAILABLE
        # -------------------------------------------------

        else:

            score = float(st.session_state.prediction)

            # ---------------------------------------------
            # SCORE INTERPRETATION
            # ---------------------------------------------

            if score < 40:
                interpretation = "Low Mental Health Score"
                description = (
                    "The predicted score indicates a lower "
                    "mental health score based on the provided "
                    "student information."
                )
            elif score <= 70:
                interpretation = "Moderate Mental Health Score"
                description = (
                    "The predicted score indicates a moderate "
                    "mental health score based on the provided "
                    "student information."
                )
            else:
                interpretation = "Good Mental Health Score"
                description = (
                    "The predicted score indicates a relatively "
                    "good mental health score based on the "
                    "provided student information."
                )

            # ---------------------------------------------
            # RESULT DISPLAY
            # ---------------------------------------------

            st.markdown(f"""
<div class="result-content">
<div class="result-icon">🧠</div>
<div class="result-title">Mental Health Score</div>
<div class="result-score">{score:.2f}</div>
<div class="result-label">out of 100</div>
<div class="result-description">
<strong>{interpretation}</strong><br><br>
{description}
</div>
<div class="disclaimer">
<b>Important:</b> This prediction is for educational and
informational purposes only. It is not a professional medical
diagnosis.
</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# ERROR MESSAGE
# =========================================================

if st.session_state.prediction_status not in [None, "success"]:
    st.error(st.session_state.prediction_status)