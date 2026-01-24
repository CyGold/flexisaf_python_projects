# Global variable
PASSING_SCORE = 50


def calculate_score(*scores, **kwargs):
    """
    Calculate total score with flexible arguments.
    - *scores: accepts any number of scores
    - **kwargs: optional settings like 'bonus' or 'weight'
    """
    total = sum(scores)

    # Apply optional bonus
    bonus = kwargs.get("bonus", 0)
    total += bonus

    # Apply optional weight
    weight = kwargs.get("weight", 1)
    total *= weight

    return total


def report_student(name, *scores, **kwargs):
    """
    Report student performance.
    Demonstrates unpacking and variable scopes.
    """

    total = calculate_score(*scores, **kwargs)

    # Local scope variable
    status = "PASS" if total >= PASSING_SCORE else "FAIL"

    print(f"Student: {name}")
    print(f"Scores: {scores}")
    print(f"Options: {kwargs}")
    print(f"Total: {total}")
    print(f"Status: {status}")
    print("-" * 40)

# Define student data with unpacking
students = [
    ("Anita", (70, 80, 90), {"bonus": 5}),
    ("John", [40, 45, 50], {"bonus": 10, "weight": 1.1}),
    ("Precious", (30, 20, 25), {"bonus": 0}),
    ("Carlos", (10, 5, 10), {"bonus": 10}),
]

# Loop through students and unpack arguments
for name, scores, options in students:
    report_student(name, *scores, **options)
