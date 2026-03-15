from datetime import time, timedelta

DAY_START = time(6, 30)
DAY_END = time(17, 0)

NIGHT_START = time(18, 0)
NIGHT_END = time(4, 30)


def get_period(t):
    """
    Определяет период смены: DAY или NIGHT
    """
    if DAY_START <= t <= DAY_END:
        return "DAY"

    if t >= NIGHT_START or t <= NIGHT_END:
        return "NIGHT"

    return "NONE"


def toggle_type(shift_type):
    """
    Переключает NRT <-> STH
    """
    return "STH" if shift_type == "NRT" else "NRT"


def get_team(dt, wednesday_team):
    """
    Определяет FRONT / BACK
    """
    if dt.time() <= NIGHT_END:
        date = (dt - timedelta(days=1)).date()
    else:
        date = dt.date()

    weekday = date.weekday()

    if weekday in (6, 0, 1):
        return "FRONT"

    if weekday in (3, 4, 5):
        return "BACK"

    return wednesday_team


def assign_shifts(rows, state):
    """
    Основная логика назначения смен
    """

    prev_period = None
    current_type = None

    for row in rows:
        dt = row["datetime"]
        t = dt.time()

        period = get_period(t)

        if period == "NONE":
            row["shift"] = ""
            continue

        if current_type is None:
            current_type = state["first_day_type"]
        else:
            if prev_period and period != prev_period:
                current_type = toggle_type(current_type)

        team = get_team(dt, state["wednesday_team"])

        row["shift"] = f"{team} {current_type}"

        prev_period = period


def assign_shift(rows, state):
    assign_shifts(rows, state)