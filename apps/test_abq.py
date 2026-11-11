
from abq import calculate_abq_scores

# Temporary test responses.
# These are test numbers, NOT actual athlete answers.

test_responses = {
    1: 5,
    2: 4,
    3: 3,
    4: 4,
    5: 3,
    6: 2,
    7: 4,
    8: 5,
    9: 3,
    10: 4,
    11: 2,
    12: 5,
    13: 4,
    14: 5,
    15: 3
}

try:
    scores = calculate_abq_scores(test_responses)

    print("ABQ scoring test successful!")

    for name, score in scores.items():
        print(f"{name}: {score:.2f}")

except Exception as error:
    print("ABQ scoring test failed:")
    print(error)
