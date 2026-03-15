import csv
from datetime import datetime
from pathlib import Path

TIME_FIELD = "First container scan to trailer"


def read_csv(path):
    rows = []

    with open(path) as f:
        reader = csv.DictReader(f)

        for row in reader:
            row["datetime"] = datetime.fromisoformat(row[TIME_FIELD])
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