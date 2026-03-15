import csv
from datetime import datetime
from pathlib import Path

TIME_FIELDS = (
    "First container scan to trailer",
    "first_container_scan_to_trailer_time_local",
)


def resolve_time_field(fieldnames):
    for field in TIME_FIELDS:
        if field in fieldnames:
            return field

    supported_fields = ", ".join(TIME_FIELDS)
    raise KeyError(f"CSV must contain one of these columns: {supported_fields}")

def read_csv(path):
    rows = []

    with open(path) as f:
        reader = csv.DictReader(f)
        time_field = resolve_time_field(reader.fieldnames or [])

        for row in reader:
            row["datetime"] = datetime.fromisoformat(row[time_field])
            rows.append(row)

    return rows


def write_csv(rows, path):
    Path("data").mkdir(exist_ok=True)

    with open(path, "w", newline="") as f:
        fieldnames = list(rows[0].keys())

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            r = row.copy()
            r["datetime"] = r["datetime"].isoformat(sep=" ")
            writer.writerow(r)