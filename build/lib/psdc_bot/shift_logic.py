from datetime import time, timedelta

DAY_START = time(6,30)
DAY_END = time(17,0)
NIGHT_START = time(18,0)

def get_team(dt, wednesday_team):
    day = dt.weekday()
    if day in [6,0,1]:  # Niedziela, poniedziałek, wtorek
        return "FRONT"
    if day in [3,4,5]:  # Czwartek, piątek, sobota
        return "BACK"
    return wednesday_team  # Środa

def assign_shift_for_row(row, state):
    dt = row["datetime"]
    t = dt.time()

    # Zmiana dzienna
    if DAY_START <= t <= DAY_END:
        if state["first_day_type"] is None:
            state["first_day_type"] = "NRT"  # można zmienić zgodnie z dowolną zasadą
        shift_type = state["first_day_type"]
        team = get_team(dt, state["wednesday_team"])

        # Przygotowanie do zmiany nocnej
        state["night_team"] = team
        state["night_type"] = "STH" if shift_type.endswith("NRT") else "NRT"
        state["night_end"] = dt.replace(hour=4, minute=30) + timedelta(days=1)

    # Zmiana nocna
    else:
        if state["night_team"] and dt <= state["night_end"]:
            team = state["night_team"]
            shift_type = state["night_type"]
        else:
            team = get_team(dt, state["wednesday_team"])
            shift_type = "NRT"
            state["night_team"] = team
            state["night_type"] = "STH"
            state["night_end"] = dt.replace(hour=4, minute=30) + timedelta(days=1)

    row["shift"] = f"{team} {shift_type}"