from datetime import time, timedelta, date

DAY_START = time(6, 30)
DAY_END = time(17, 0)
NIGHT_START = time(18, 0)
NIGHT_END = time(4, 30)

BASE_DATE = date(2026, 3, 8)        # старт 28-дневного цикла
BASE_WEDNESDAY = date(2026, 3, 11)  # первая Wednesday → FRONT


def get_period(t):
    if DAY_START <= t <= DAY_END:
        return "DAY"
    if t >= NIGHT_START or t <= NIGHT_END:
        return "NIGHT"
    return None


def get_wednesday_team(dt):
    weeks = (dt.date() - BASE_WEDNESDAY).days // 7
    return "FRONT" if weeks % 2 == 0 else "BACK"


def get_team(dt):
    if dt.time() <= NIGHT_END:
        date_value = (dt - timedelta(days=1)).date()
    else:
        date_value = dt.date()
    weekday = date_value.weekday()
    if weekday in (6, 0, 1):
        return "FRONT"
    if weekday in (3, 4, 5):
        return "BACK"
    return get_wednesday_team(dt)


def get_shift_type(dt):
    days = (dt.date() - BASE_DATE).days
    rotation = (days // 28) % 2
    if rotation == 0:
        return {"STH": "DAY", "NRT": "NIGHT"}
    return {"STH": "NIGHT", "NRT": "DAY"}


def assign_shifts(rows):
    for row in rows:
        dt = row["datetime"]
        period = get_period(dt.time())
        if not period:
            row["shift"] = ""
            continue
        team = get_team(dt)
        mapping = get_shift_type(dt)
        if mapping["STH"] == period:
            shift_type = "STH"
        else:
            shift_type = "NRT"
        row["shift"] = f"{team} {shift_type}"