import streamlit as st
from datetime import date
from psycopg.errors import UniqueViolation

from checkin import save_daily_checkin


st.set_page_config(
    page_title="OmniAthlete Daily Check-in",
    page_icon="🏅",
    layout="centered"
)

st.title("🏅 OmniAthlete")
st.subheader("Daily Athlete Wellness Check-in")

st.write(
    "Record how you're feeling today. "
    "Your responses will be saved to the OmniAthlete database."
)

st.caption(f"Check-in date: {date.today().strftime('%B %d, %Y')}")

st.info(
    "Rate each area from 1 to 7. "
    "Higher scores indicate better sleep quality, "
    "but higher stress, fatigue, and soreness."
)

with st.form("daily_checkin_form"):

    st.markdown("### Sleep Quality")
    sleep_quality = st.slider(
        "How would you rate your sleep?",
        min_value=1,
        max_value=7,
        value=4,
        help="1 = Very poor sleep; 7 = Excellent sleep"
    )

    st.markdown("### Stress Level")
    stress_level = st.slider(
        "How stressed do you feel?",
        min_value=1,
        max_value=7,
        value=4,
        help="1 = Very low stress; 7 = Very high stress"
    )

    st.markdown("### Fatigue Level")
    fatigue_level = st.slider(
        "How physically or mentally tired do you feel?",
        min_value=1,
        max_value=7,
        value=4,
        help="1 = Very little fatigue; 7 = Extreme fatigue"
    )

    st.markdown("### Muscle Soreness")
    muscle_soreness = st.slider(
        "How sore are your muscles?",
        min_value=1,
        max_value=7,
        value=4,
        help="1 = No soreness; 7 = Severe soreness"
    )

    submitted = st.form_submit_button(
        "Submit Daily Check-in",
        use_container_width=True
    )

if submitted:
    # Temporary test athlete.
    # Replace this with the authenticated athlete's ID when login is built.
    user_id = 3

    try:
        checkin_id = save_daily_checkin(
            user_id=user_id,
            checkin_date=date.today(),
            sleep_quality=sleep_quality,
            stress_level=stress_level,
            fatigue_level=fatigue_level,
            muscle_soreness=muscle_soreness
        )

        st.success("Your daily check-in was saved successfully!")
        st.write(f"Check-in reference: {checkin_id}")

    except UniqueViolation:
        st.warning(
            "A check-in has already been submitted for this athlete today."
        )

    except Exception as error:
        st.error("The check-in could not be saved.")
        st.caption(f"Technical details: {error}")