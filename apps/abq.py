
from database import get_connection


def validate_abq_responses(responses, minimum, maximum):
    """
    Validate ABQ responses against the response scale
    specified by the selected questionnaire version.
    """

    if not responses:
        raise ValueError("No ABQ responses were provided.")

    for item_number, response_value in responses.items():

        if not isinstance(item_number, int) or isinstance(item_number, bool):
            raise ValueError("Question numbers must be integers.")

        if not isinstance(response_value, int) or isinstance(response_value, bool):
            raise ValueError(
                f"Response for item {item_number} must be an integer."
            )

        if not minimum <= response_value <= maximum:
            raise ValueError(
                f"Response for item {item_number} must be "
                f"between {minimum} and {maximum}."
            )


def save_burnout_assessment(
    user_id,
    assessment_date,
    responses,
    exhaustion_score,
    reduced_accomplishment_score,
    sport_devaluation_score,
    overall_burnout_score
):
    """Save ABQ scores and individual responses together."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO burnout_assessments (
                    user_id,
                    assessment_date,
                    exhaustion_score,
                    reduced_accomplishment_score,
                    sport_devaluation_score,
                    overall_burnout_score
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING assessment_id;
                """,
                (
                    user_id,
                    assessment_date,
                    exhaustion_score,
                    reduced_accomplishment_score,
                    sport_devaluation_score,
                    overall_burnout_score
                )
            )

            assessment_id = cursor.fetchone()[0]

            for item_number, response_value in responses.items():

                cursor.execute(
                    """
                    INSERT INTO burnout_assessment_responses (
                        assessment_id,
                        item_number,
                        response_value
                    )
                    VALUES (%s, %s, %s);
                    """,
                    (
                        assessment_id,
                        item_number,
                        response_value
                    )
                )

        connection.commit()
        return assessment_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

def calculate_abq_scores(responses):
    """
    Calculate the three ABQ dimension means
    and overall mean.

    Responses must contain all 15 items, scored 1-5.
    Items 1 and 14 are reverse-scored.
    """

    validate_abq_responses(
        responses,
        minimum=1,
        maximum=5
    )

    if set(responses.keys()) != set(range(1, 16)):
        raise ValueError(
            "All 15 ABQ questions must be answered."
        )

    scored_responses = responses.copy()

    # Reverse-score items 1 and 14.
    for item_number in [1, 14]:
        scored_responses[item_number] = (
            6 - scored_responses[item_number]
        )

    # ABQ subscale item groupings.
    exhaustion_items = [2, 4, 8, 10, 12]

    accomplishment_items = [1, 5, 7, 13, 14]

    devaluation_items = [3, 6, 9, 11, 15]

    exhaustion_score = sum(
        scored_responses[i] for i in exhaustion_items
    ) / 5

    reduced_accomplishment_score = sum(
        scored_responses[i] for i in accomplishment_items
    ) / 5

    sport_devaluation_score = sum(
        scored_responses[i] for i in devaluation_items
    ) / 5

    overall_burnout_score = sum(
        scored_responses.values()
    ) / 15

    return {
        "exhaustion_score": exhaustion_score,
        "reduced_accomplishment_score":
            reduced_accomplishment_score,
        "sport_devaluation_score":
            sport_devaluation_score,
        "overall_burnout_score":
            overall_burnout_score
    }
