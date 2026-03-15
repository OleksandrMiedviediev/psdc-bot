# PSDC Shift Calculator

A simple desktop app (Tkinter) that reads a CSV with timestamps and adds a `shift` column in the format:

- `FRONT NRT`
- `BACK STH`

Supports **Windows** and **macOS**.

---

## Features

- Select input CSV via GUI
- Choose the initial shift type: `NRT` or `STH`
- Choose the Wednesday team: `FRONT` or `BACK`
- Automatic day/night period detection
- Automatic `NRT ↔ STH` switching when the period changes
- Save the result to a new CSV

---

## Shift Assignment Rules

### 1) Period

- **DAY**: `06:30` – `17:00`
- **NIGHT**: `18:00` – `04:30`
- Time outside these ranges gets an empty `shift` value

### 2) Team (FRONT/BACK)

- **FRONT**: Sunday, Monday, Tuesday
- **BACK**: Thursday, Friday, Saturday
- **Wednesday**: selected by the user in the GUI

For night records up to `04:30`, the previous calendar date is used (night-shift logic).

### 3) Shift Type (NRT/STH)

- The first valid record gets the user-selected starting type
- On every `DAY` ↔ `NIGHT` transition, the type switches automatically: `NRT ↔ STH`

---

## Input CSV Format

The CSV must contain one of these time columns:

- `First container scan to trailer`
- `first_container_scan_to_trailer_time_local`

Date/time format:

`YYYY-MM-DD HH:MM:SS`

Example:

```csv
first_container_scan_to_trailer_time_local
2026-03-06 19:19:00
2026-03-06 23:51:00
2026-03-07 00:00:00
```

---

## Run

### Windows

1. Double-click `run_windows.bat`
2. In the GUI, select the input CSV
3. Choose the starting type (`NRT`/`STH`) and Wednesday team (`FRONT`/`BACK`)
4. Click **Generate CSV** and choose the output path

### macOS

1. Make the script executable once:

   ```bash
   chmod +x run_mac.command
   ```

2. Double-click `run_mac.command`
3. Repeat the same steps in the GUI

### Manual Run

```bash
python main.py
# or
python3 main.py
```

---

## Project Structure

| File | Purpose |
| --- | --- |
| `main.py` | Entry point (starts GUI) |
| `gui.py` | GUI and user action handling |
| `csv_reader.py` | CSV read/write logic |
| `shift_logic.py` | Shift assignment logic |
| `run_windows.bat` | Quick launch on Windows |
| `run_mac.command` | Quick launch on macOS |
| `source.csv` | Example input file |
| `data/` | Output data folder |

---

## Requirements

- Python `3.10+`

Version check:

```bash
python --version
# or
python3 --version
```

---

## Notes

- If the output CSV is open in Excel, writing may fail with a permission error
- The `data` folder is created automatically (if it does not exist)

## Author

Mode by: [@miedolek](https://github.com/OleksandrMiedviediev)