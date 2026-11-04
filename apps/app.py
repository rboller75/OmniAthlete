import streamlit as st
import pandas as pd

from datetime import date
from psycopg.errors import UniqueViolation
from checkin import (save_daily_checkin, get_daily_checkins, get_burnout_assessments)
from risk import (evaluate_wellness_risk, get_latest_checkin, save_risk_alert)

st.set_page_config(
    page_title="OmniAthlete",
    page_icon="🏅",
    layout="centered"
)

st.title("🏅 OmniAthlete")
st.subheader("Daily Athlete Wellness Check-in")

st.write(
    "Record how you're feeling today and review "
    "your recent wellness history."
)

st.caption(
    f"Check-in date: {date.today().strftime('%B %d, %Y')}"
)

st.info(
    "Rate each area from 1 to 10. Higher sleep scores "
    "mean better sleep. Higher stress, fatigue, and "
    "soreness scores mean more difficulty in those areas."
)

# Temporary test athlete.
# Replace this with the authenticated athlete's ID later.
user_id = 1

# -----------------------------
# DAILY CHECK-IN FORM
# -----------------------------

with st.form("daily_checkin_form"):

    st.markdown("### Sleep Quality")

    sleep_quality = st.slider(
        "How would you rate your sleep?",
        min_value=1,
        max_value=10,
        value=5,
        help="1 = Very poor sleep; 10 = Excellent sleep"
    )

    st.markdown("### Stress Level")

    stress_level = st.slider(
        "How stressed do you feel?",
        min_value=1,
        max_value=10,
        value=5,
        help="1 = Very low stress; 10 = Very high stress"
    )

    st.markdown("### Fatigue Level")

    fatigue_level = st.slider(
        "How tired do you feel?",
        min_value=1,
        max_value=10,
        value=5,
        help="1 = Very little fatigue; 10 = Extreme fatigue"
    )

    st.markdown("### Muscle Soreness")

    muscle_soreness = st.slider(
        "How sore are your muscles?",
        min_value=1,
        max_value=10,
        value=5,
        help="1 = No soreness; 10 = Severe soreness"
    )

    submitted = st.form_submit_button(
        "Submit Daily Check-in",
        use_container_width=True
    )

if submitted:

    try:
        checkin_id = save_daily_checkin(
            user_id=user_id,
            checkin_date=date.today(),
            sleep_quality=sleep_quality,
            stress_level=stress_level,
            fatigue_level=fatigue_level,
            muscle_soreness=muscle_soreness
        )

        st.success("Your check-in was saved successfully!")
        st.write(f"Check-in reference: {checkin_id}")

    except UniqueViolation:
        st.warning(
            "A check-in has already been submitted "
            "for this athlete today."
        )

    except Exception as error:
        st.error("The check-in could not be saved.")
        st.caption(f"Technical details: {error}")

# -----------------------------
# CURRENT WELLNESS RISK STATUS
# -----------------------------

st.divider()

st.header("Athlete Wellness Risk Status")

try:
    latest_checkin = get_latest_checkin(user_id)

    if latest_checkin is None:

        st.info(
            "No daily check-in is available to evaluate."
        )

    else:
        (
            checkin_id,
            checkin_date,
            sleep_quality,
            stress_level,
            fatigue_level,
            muscle_soreness
        ) = latest_checkin

        risk_level, reason = evaluate_wellness_risk(
            sleep_quality,
            stress_level,
            fatigue_level,
            muscle_soreness
        )

        save_risk_alert(
            user_id=user_id,
            checkin_id=checkin_id,
            alert_date=checkin_date,
            risk_level=risk_level,
            reason=reason
        )

        if risk_level == "green":

            st.success("GREEN — Low Wellness Concern")

        elif risk_level == "yellow":

            st.warning("YELLOW — Moderate Wellness Concern")

        else:

            st.error("RED — Elevated Wellness Concern")

        st.write(f"**Assessment date:** {checkin_date}")
        st.write(f"**Reason:** {reason}")

        st.caption(
            "This preliminary wellness alert is based on "
            "daily check-in thresholds. It is not a medical "
            "diagnosis or a validated burnout prediction."
        )

except Exception as error:

    st.error("Unable to calculate the wellness risk status.")
    st.caption(f"Technical details: {error}")

# -----------------------------
# WELLNESS HISTORY DASHBOARD
# -----------------------------

st.divider()

st.header("Wellness History")

st.write(
    "Review recent check-ins and look for changes "
    "in your wellness ratings."
)

try:
    records = get_daily_checkins(user_id=user_id, limit=30)

    if records:

        columns = [
            "Check-in Date",
            "Sleep Quality",
            "Stress Level",
            "Fatigue Level",
            "Muscle Soreness"
        ]

        history = pd.DataFrame(
            records,
            columns=columns
        )

        # Show the newest check-ins first.
        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Wellness Trends")

        # Charts display dates from oldest to newest.
        chart_data = history.sort_values("Check-in Date")

        chart_data = chart_data.set_index("Check-in Date")

        st.line_chart(
            chart_data[
                [
                    "Sleep Quality",
                    "Stress Level",
                    "Fatigue Level",
                    "Muscle Soreness"
                ]
            ]
        )

        st.caption(
            "Interpret the ratings separately: higher sleep "
            "scores are favorable, while higher stress, fatigue, "
            "and soreness scores indicate greater difficulty. "
            "These are wellness trends, not a medical diagnosis."
        )

    else:
        st.info(
            "No check-in history is available for this athlete yet."
        )

except Exception as error:
    st.error("Unable to load wellness history.")
    st.caption(f"Technical details: {error}")


# -----------------------------
# BURNOUT ASSESSMENT HISTORY
# -----------------------------

st.divider()

st.header("Athlete Burnout Questionnaire (ABQ)")

st.write(
    "Review previously recorded burnout assessments. "
    "These results are separate from daily wellness ratings."
)

try:
    assessments = get_burnout_assessments(
        user_id=user_id,
        limit=10
    )

    if assessments:
        abq_columns = [
            "Assessment Date",
            "Exhaustion Score",
            "Reduced Accomplishment Score",
            "Sport Devaluation Score",
            "Overall Burnout Score"
        ]

        abq_history = pd.DataFrame(
            assessments,
            columns=abq_columns
        )

        st.dataframe(
            abq_history,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info(
            "No burnout assessments have been recorded "
            "for this athlete yet."
        )

except Exception as error:
    st.error("Unable to load burnout assessment history.")
    st.caption(f"Technical details: {error}")
