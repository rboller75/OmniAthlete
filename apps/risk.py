
from database import get_connection


def evaluate_wellness_risk(
    sleep_quality,
    stress_level,
    fatigue_level,
    muscle_soreness
):
    """
    Evaluate daily wellness ratings using preliminary
    OmniAthlete risk thresholds.
    """

    concerns = []

    if sleep_quality <= 3:
        concerns.append("Low sleep quality")

    if stress_level >= 8:
        concerns.append("High stress")

    if fatigue_level >= 8:
        concerns.append("High fatigue")

    if muscle_soreness >= 8:
        concerns.append("High muscle soreness")

    concern_count = len(concerns)

    if concern_count == 0:
        risk_level = "green"

    elif concern_count <= 2:
        risk_level = "yellow"

    else:
        risk_level = "red"

    if concerns:
        reason = "; ".join(concerns)
    else:
        reason = "No wellness indicators reached concern thresholds."

    return risk_level, reason


def get_latest_checkin(user_id):
    """Retrieve the latest daily check-in for an athlete."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT
                    checkin_id,
                    checkin_date,
                    sleep_quality,
                    stress_level,
                    fatigue_level,
                    muscle_soreness
                FROM daily_checkins
                WHERE user_id = %s
                ORDER BY checkin_date DESC
                LIMIT 1;
            """

            cursor.execute(query, (user_id,))
            return cursor.fetchone()

    finally:
        connection.close()


def save_risk_alert(user_id, checkin_id, alert_date,
                    risk_level, reason):
    """Save or update the risk alert for a daily check-in."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # Check whether an alert already exists for this check-in.
            cursor.execute(
                """
                SELECT alert_id
                FROM risk_alerts
                WHERE checkin_id = %s;
                """,
                (checkin_id,)
            )

            existing_alert = cursor.fetchone()

            if existing_alert:

                cursor.execute(
                    """
                    UPDATE risk_alerts
                    SET
                        risk_level = %s,
                        reason = %s,
                        is_active = TRUE
                    WHERE checkin_id = %s;
                    """,
                    (risk_level, reason, checkin_id)
                )

            else:

                cursor.execute(
                    """
                    INSERT INTO risk_alerts
                    (
                        user_id,
                        checkin_id,
                        assessment_id,
                        alert_date,
                        risk_level,
                        reason,
                        is_active
                    )
                    VALUES (%s, %s, NULL, %s, %s, %s, TRUE);
                    """,
                    (
                        user_id,
                        checkin_id,
                        alert_date,
                        risk_level,
                        reason
                    )
                )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
