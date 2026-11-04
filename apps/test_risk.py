
from risk import (evaluate_wellness_risk, get_latest_checkin, save_risk_alert)


print("TEST 1: Green Risk")

result = evaluate_wellness_risk(
    sleep_quality=8,
    stress_level=3,
    fatigue_level=4,
    muscle_soreness=2
)

print(result)


print("\nTEST 2: Yellow Risk")

result = evaluate_wellness_risk(
    sleep_quality=3,
    stress_level=5,
    fatigue_level=4,
    muscle_soreness=2
)

print(result)


print("\nTEST 3: Red Risk")

result = evaluate_wellness_risk(
    sleep_quality=2,
    stress_level=9,
    fatigue_level=8,
    muscle_soreness=9
)

print(result)


from risk import get_latest_checkin, save_risk_alert

# Temporary test athlete
user_id = 1

print("\nTEST 4: Save Risk Alert")

try:
    latest_checkin = get_latest_checkin(user_id)

    if latest_checkin is None:
        print("No daily check-in found for this athlete.")

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

        print("Risk alert saved successfully!")
        print(f"Risk level: {risk_level}")
        print(f"Reason: {reason}")

except Exception as error:
    print("Risk alert could not be saved:")
    print(error)
