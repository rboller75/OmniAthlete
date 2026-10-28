from datetime import date
from checkin import save_daily_checkin
from checkin import get_daily_checkins
from checkin import get_burnout_assessments

try:
    checkin_id = save_daily_checkin(
        user_id=1,
        checkin_date=date.today(),
        sleep_quality=6,
        stress_level=3,
        fatigue_level=4,
        muscle_soreness=2
    )

    print("Daily check-in saved successfully!")
    print(f"Check-in ID: {checkin_id}")

except Exception as error:
    print("Daily check-in failed:")
    print(error)

print("\nTesting check-in history:")

try:
    records = get_daily_checkins(user_id=1)

    print(f"Records found: {len(records)}")

    for record in records:
        print(record)

except Exception as error:
    print("Could not retrieve check-in history:")
    print(error)

print("\nTesting burnout assessment history:")

try:
    assessments = get_burnout_assessments(user_id=1)

    print(f"Assessments found: {len(assessments)}")

    for assessment in assessments:
        print(assessment)

except Exception as error:
    print("Could not retrieve burnout assessments:")
    print(error)