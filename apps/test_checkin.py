from datetime import date
from checkin import save_daily_checkin


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