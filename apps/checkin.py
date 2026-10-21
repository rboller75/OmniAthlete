from database import get_connection


def validate_checkin_value(value, field_name):
    """Make sure a check-in value is an integer from 1 to 10."""

    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an integer.")

    if value < 1 or value > 10:
        raise ValueError(f"{field_name} must be between 1 and 10.")


def save_daily_checkin(
    user_id,
    checkin_date,
    sleep_quality,
    stress_level,
    fatigue_level,
    muscle_soreness
):
    """Save an athlete's daily check-in to PostgreSQL."""

    validate_checkin_value(sleep_quality, "Sleep quality")
    validate_checkin_value(stress_level, "Stress level")
    validate_checkin_value(fatigue_level, "Fatigue level")
    validate_checkin_value(muscle_soreness, "Muscle soreness")

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            query = """
                INSERT INTO daily_checkins
                (
                    user_id,
                    checkin_date,
                    sleep_quality,
                    stress_level,
                    fatigue_level,
                    muscle_soreness
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING checkin_id;
            """

            cursor.execute(
                query,
                (
                    user_id,
                    checkin_date,
                    sleep_quality,
                    stress_level,
                    fatigue_level,
                    muscle_soreness
                )
            )

            checkin_id = cursor.fetchone()[0]

        connection.commit()

        return checkin_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_daily_checkins(user_id, limit=30):
    """Retrieve recent wellness check-ins for one athlete."""
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT
                    checkin_date,
                    sleep_quality,
                    stress_level,
                    fatigue_level,
                    muscle_soreness
                FROM daily_checkins
                WHERE user_id = %s
                ORDER BY checkin_date DESC
                LIMIT %s;
            """

            cursor.execute(query, (user_id, limit))
            records = cursor.fetchall()

        return records

    finally:
        connection.close()
