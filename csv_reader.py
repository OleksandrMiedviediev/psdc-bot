import csv
import importlib
from datetime import datetime
from pathlib import Path
from datetime import timedelta

TIME_FIELDS = (
    "Departure time (UTC)",
)

KNOWN_DATETIME_FORMATS = (
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y/%m/%d %H:%M:%S",
    "%Y/%m/%d %H:%M",
    "%d.%m.%Y %H:%M:%S",
    "%d.%m.%Y %H:%M",
    "%d-%m-%Y %H:%M:%S",
    "%d-%m-%Y %H:%M",
    "%m/%d/%Y %H:%M:%S",
    "%m/%d/%Y %H:%M",
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y %H:%M",
    "%m/%d/%Y %I:%M:%S %p",
    "%m/%d/%Y %I:%M %p",
    "%d/%m/%Y %I:%M:%S %p",
    "%d/%m/%Y %I:%M %p",
    "%Y-%m-%d",
    "%d.%m.%Y",
    "%d-%m-%Y",
    "%m/%d/%Y",
    "%d/%m/%Y",
)

EXCEL_EPOCH = datetime(1899, 12, 30)


def resolve_time_field(fieldnames):
    for field in TIME_FIELDS:
        if field in fieldnames:
            return field


def parse_datetime(value):
    if value is None:
        raise ValueError("datetime value is empty")

    raw = str(value).strip()
    if not raw:
        raise ValueError("datetime value is empty")

    try:
        number = float(raw)
        if 20000 <= number <= 70000:
            return EXCEL_EPOCH + timedelta(days=number)
        if number > 1_000_000_000_000:
            return datetime.fromtimestamp(number / 1000)
        if number > 1_000_000_000:
            return datetime.fromtimestamp(number)
    except ValueError:
        pass

    normalized = raw.replace("T", " ")
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(normalized)
        return parsed.replace(tzinfo=None) if parsed.tzinfo else parsed
    except ValueError:
        pass

    for fmt in KNOWN_DATETIME_FORMATS:
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue

    try:
        dateutil_parser = importlib.import_module("dateutil.parser")
        parsed = dateutil_parser.parse(raw)
        return parsed.replace(tzinfo=None) if parsed.tzinfo else parsed
    except Exception as error:
        raise ValueError(f"unsupported datetime format: {raw}") from error


def detect_time_field(fieldnames, raw_rows):
    preferred = resolve_time_field(fieldnames)
    if preferred:
        return preferred

    best_field = None
    best_score = -1

    for field in fieldnames:
        tested = 0
        parsed_ok = 0

        for row in raw_rows:
            value = row.get(field)
            if value is None or str(value).strip() == "":
                continue

            tested += 1
            try:
                parse_datetime(value)
                parsed_ok += 1
            except ValueError:
                pass

            if tested >= 25:
                break

        if tested == 0:
            continue

        if parsed_ok > best_score:
            best_score = parsed_ok
            best_field = field

    if best_field and best_score > 0:
        return best_field

    supported = ", ".join(TIME_FIELDS)
    raise KeyError(
        "CSV must contain a supported time column or any column with parseable date/time values. "
        f"Preferred columns: {supported}"
    )


def read_csv(path):
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        raw_rows = list(reader)
        fieldnames = reader.fieldnames or []
        time_field = detect_time_field(fieldnames, raw_rows)

        for row in raw_rows:
            row["datetime"] = parse_datetime(row.get(time_field))
            rows.append(row)
    return rows


def write_csv(rows, path):
    Path(path).parent.mkdir(exist_ok=True)
    with open(path, "w", newline="") as f:
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            r = row.copy()
            r["datetime"] = r["datetime"].isoformat(sep=" ")
            writer.writerow(r)