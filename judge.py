EPSILON = 1e-9

def judge(score_a: float, score_b: float) -> str:
    """
    Compare two MAC scores. Returns 'a' if score_a wins, 'b' if score_b wins,
    tied if within epsilon (1e-9). Labels are positional, caller maps to domain names.
    """

    if abs(score_a - score_b) < EPSILON:
        return "tied"
    elif score_a > score_b:
        return "a"
    else:
        return "b"
